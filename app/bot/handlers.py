import logging
import asyncio
from typing import Dict, List, Optional
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from app.config import settings
from app.bot.messages import ArabicMessages
from app.bot.keyboards import ArabicKeyboards
from app.database.supabase_client import supabase_client
from app.external.najah_api import najah_api
from app.external.cache import redis_cache
from app.utils.validation import ValidationUtils, RateLimitUtils
from app.database.models import UserSession
from datetime import datetime

logger = logging.getLogger(__name__)


class BotHandlers:
    """Bot command and callback handlers"""
    
    def __init__(self, shard_id: int, bot_manager=None):
        self.shard_id = shard_id
        self.messages = ArabicMessages()
        self.keyboards = ArabicKeyboards()
        self.bot_manager = bot_manager  # For single interface mode
    
    async def start_command(self, update: Update, context) -> None:
        """Handle /start command"""
        try:
            user = update.effective_user
            logger.info(f"Start command from user {user.id} on shard {self.shard_id}")
            
            # Check channel subscription first
            if not await self._check_channel_subscription(user.id):
                await self._send_subscription_message(update)
                return
            
            # Save user session
            self._save_user_session(user.id, "main_menu")
            
            await update.message.reply_text(
                self.messages.WELCOME_MESSAGE,
                reply_markup=self.keyboards.main_menu()
            )
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await self._send_error_message(update)
    
    async def button_callback(self, update: Update, context) -> None:
        """Handle inline keyboard button callbacks"""
        try:
            query = update.callback_query
            user = query.from_user
            data = query.data
            
            logger.info(f"Callback from user {user.id}: {data}")
            
            # Only check rate limit for actual searches, not menu navigation
            if data in ["search_name", "search_examno"] or data.startswith("select_student_"):
                if not await self._check_rate_limit(user.id):
                    await query.answer(self.messages.RATE_LIMIT_EXCEEDED, show_alert=True)
                    return
            
            await query.answer()
            
            # Route callback based on data
            if data == "main_menu":
                await self._show_main_menu(query)
            elif data == "search_name":
                await self._start_name_search(query)
            elif data == "search_examno":
                await self._start_examno_search(query)
            elif data.startswith("gov_"):
                gov_name = data[4:]
                await self._handle_governorate_selection(query, gov_name)
            elif data.startswith("select_student_"):
                examno = data[15:]
                await self._show_student_result(query, examno)
            elif data.startswith("share_"):
                examno = data[6:]
                await self._share_result(query, examno)
            elif data == "check_subscription":
                await self._handle_subscription_check(query)
            else:
                await query.edit_message_text(
                    "خيار غير صحيح",
                    reply_markup=self.keyboards.main_menu()
                )
                
        except Exception as e:
            logger.error(f"Error in button callback: {e}")
            await self._send_callback_error(update.callback_query)
    
    async def text_message(self, update: Update, context) -> None:
        """Handle text messages"""
        try:
            user = update.effective_user
            text = update.message.text
            
            logger.info(f"Text message from user {user.id}: {text[:50]}...")
            
            # Get user session to determine current state
            session = supabase_client.get_user_session(user.id)
            current_state = session.current_state if session else "main_menu"
            
            # Only check rate limit for actual search inputs, not menu navigation
            if current_state in ["waiting_name", "waiting_examno"]:
                if not await self._check_rate_limit(user.id):
                    await update.message.reply_text(
                        self.messages.RATE_LIMIT_EXCEEDED,
                        reply_markup=self.keyboards.back_to_main_keyboard()
                    )
                    return
            
            # Handle based on current state
            if current_state == "waiting_name":
                await self._handle_name_input(update, text)
            elif current_state == "waiting_examno":
                await self._handle_examno_input(update, text)
            else:
                # Default: show main menu
                await update.message.reply_text(
                    self.messages.WELCOME_MESSAGE,
                    reply_markup=self.keyboards.main_menu()
                )
                
        except Exception as e:
            logger.error(f"Error in text message handler: {e}")
            await self._send_error_message(update)
    
    async def _show_main_menu(self, query) -> None:
        """Show main menu"""
        self._save_user_session(query.from_user.id, "main_menu")
        await query.edit_message_text(
            self.messages.WELCOME_MESSAGE,
            reply_markup=self.keyboards.main_menu()
        )
    
    async def _start_name_search(self, query) -> None:
        """Start name search process - first show governorates"""
        # Check subscription
        if not await self._check_channel_subscription(query.from_user.id):
            await self._send_subscription_message(query)
            return
            
        # Set state to waiting for governorate selection
        self._save_user_session(query.from_user.id, "waiting_governorate")
        
        await query.edit_message_text(
            "🏛️ اختر المحافظة أولاً لتقليل النتائج المكررة:",
            reply_markup=self.keyboards.governorates_keyboard()
        )
    
    async def _start_examno_search(self, query) -> None:
        """Start exam number search process"""
        # Check subscription
        if not await self._check_channel_subscription(query.from_user.id):
            await self._send_subscription_message(query)
            return
            
        self._save_user_session(query.from_user.id, "waiting_examno")
        await query.edit_message_text(
            self.messages.EXAMNO_SEARCH_PROMPT,
            reply_markup=self.keyboards.back_to_main_keyboard()
        )
    
    async def _handle_name_input(self, update: Update, name: str) -> None:
        """Handle name search input"""
        # Validate and clean name
        clean_name = ValidationUtils.clean_arabic_name(name)
        if not clean_name:
            await update.message.reply_text(
                self.messages.INVALID_NAME,
                reply_markup=self.keyboards.back_to_main_keyboard()
            )
            return
        
        # Check for spam
        if ValidationUtils.is_spam_input(clean_name):
            await update.message.reply_text(
                "❌ مدخل غير صحيح",
                reply_markup=self.keyboards.back_to_main_keyboard()
            )
            return
        
        # Get selected governorate from session
        user_id = update.effective_user.id
        session = supabase_client.get_user_session(user_id)
        
        logger.info(f"Name search for user {user_id}: session={session}, history={session.search_history if session else None}")
        
        if not session or not session.search_history or not session.search_history.get("selected_governorate"):
            await update.message.reply_text(
                "❌ لم يتم اختيار المحافظة. يرجى البدء من جديد",
                reply_markup=self.keyboards.main_menu()
            )
            return
        
        selected_governorate = session.search_history["selected_governorate"]
        
        # Search for students in the selected governorate
        logger.info(f"Searching for name='{clean_name}' in governorate='{selected_governorate}'")
        search_result = supabase_client.search_students_by_name(
            clean_name, selected_governorate, limit=5
        )
        
        logger.info(f"Search result: {len(search_result.students)} students found")
        
        if not search_result.students:
            await update.message.reply_text(
                f"❌ لم يتم العثور على طلاب بالاسم '{clean_name}' في محافظة {selected_governorate}",
                reply_markup=self.keyboards.back_to_main_keyboard()
            )
            return
        
        if len(search_result.students) == 1:
            # Single result: show directly
            student = search_result.students[0]
            # For direct message response, we need a different approach
            # Show student result via message instead of callback
            await self._show_student_result_message(update, student.examno)
        else:
            # Multiple results: show selection
            result_text = f"🔍 نتائج البحث عن '{clean_name}' في {selected_governorate}:\n\n"
            
            for i, student in enumerate(search_result.students, 1):
                result_text += f"{i}. {student.aname}\n"
                result_text += f"   📚 المدرسة: {student.sch_name or 'غير محدد'}\n"
                result_text += f"   🆔 رقم الجلوس: {student.examno}\n\n"
            
            if search_result.has_more:
                result_text += f"📝 يوجد المزيد من النتائج ({search_result.total_count} إجمالي)"
            
            await update.message.reply_text(
                result_text,
                reply_markup=self.keyboards.student_results_keyboard(search_result.students)
            )
        
        # Reset session state
        self._save_user_session(update.effective_user.id, "main_menu")
    
    async def _handle_governorate_selection(self, query, gov_name: str) -> None:
        """Handle governorate selection for name search"""
        user_id = query.from_user.id
        
        # Get session to check current state
        session = supabase_client.get_user_session(user_id)
        current_state = session.current_state if session else "main_menu"
        
        if current_state == "waiting_governorate":
            # Save selected governorate and prompt for name
            self._save_user_session(
                user_id, 
                "waiting_name", 
                {"selected_governorate": gov_name}
            )
            
            await query.edit_message_text(
                f"🏛️ تم اختيار محافظة: {gov_name}\n\n"
                f"✍️ الآن أدخل الاسم الذي تريد البحث عنه:",
                reply_markup=self.keyboards.back_to_main_keyboard()
            )
            return
        
        # Legacy flow - if we have search_name already
        if not session or not session.search_history:
            await query.edit_message_text(
                "❌ انتهت جلسة البحث. يرجى البدء من جديد",
                reply_markup=self.keyboards.main_menu()
            )
            return
        
        search_name = session.search_history.get("search_name")
        if not search_name:
            await query.edit_message_text(
                "❌ خطأ في البحث. يرجى البدء من جديد",
                reply_markup=self.keyboards.main_menu()
            )
            return
        
        # Search for students
        search_result = supabase_client.search_students_by_name(
            search_name, gov_name, limit=5
        )
        
        if not search_result.students:
            await query.edit_message_text(
                self.messages.NO_RESULTS_FOUND,
                reply_markup=self.keyboards.back_to_main_keyboard()
            )
            return
        
        if len(search_result.students) == 1:
            # Single result: show directly
            student = search_result.students[0]
            await self._show_student_result(query, student.examno)
        else:
            # Multiple results: show selection
            await query.edit_message_text(
                self.messages.MULTIPLE_RESULTS_FOUND,
                reply_markup=self.keyboards.student_results_keyboard(search_result.students)
            )
    
    async def _handle_examno_input(self, update: Update, examno: str) -> None:
        """Handle exam number input"""
        # Validate and clean exam number
        clean_examno = ValidationUtils.clean_exam_number(examno)
        if not clean_examno:
            await update.message.reply_text(
                self.messages.INVALID_EXAMNO,
                reply_markup=self.keyboards.back_to_main_keyboard()
            )
            return
        
        await self._show_student_result_from_message(update, clean_examno)
    
    async def _show_student_result(self, query, examno: str) -> None:
        """Show student result from callback query"""
        # Show loading message
        await query.edit_message_text("🔍 جاري البحث عن النتيجة...")
        
        # Get student and result from database first
        student_data = supabase_client.get_student_with_result(examno)
        
        if not student_data or not student_data["student"]:
            await query.edit_message_text(
                "❌ لم يتم العثور على بيانات الطالب",
                reply_markup=self.keyboards.back_to_main_keyboard()
            )
            return
        
        student = student_data["student"]
        exam_result = student_data["exam_result"]
        
        # If no result in database, try external API as fallback
        if not exam_result:
            result_response = await najah_api.get_exam_result(examno)
            if result_response.success:
                result_text = self.messages.format_exam_result_from_api(result_response.data)
            else:
                result_text = self.messages.format_exam_result(student, None)
        else:
            # Format result from database
            result_text = self.messages.format_exam_result(student, exam_result)
        
        await query.edit_message_text(
            result_text,
            reply_markup=self.keyboards.result_actions_keyboard(examno)
        )
        
        # Reset user session
        self._save_user_session(query.from_user.id, "main_menu")
    
    async def _show_student_result_from_message(self, update: Update, examno: str) -> None:
        """Show student result from text message"""
        # Show loading message
        loading_msg = await update.message.reply_text("🔍 جاري البحث عن النتيجة...")
        
        # Get student and result from database first
        student_data = supabase_client.get_student_with_result(examno)
        
        if not student_data or not student_data["student"]:
            await loading_msg.edit_text(
                "❌ لم يتم العثور على بيانات الطالب",
                reply_markup=self.keyboards.back_to_main_keyboard()
            )
            return
        
        student = student_data["student"]
        exam_result = student_data["exam_result"]
        
        # If no result in database, try external API as fallback
        if not exam_result:
            result_response = await najah_api.get_exam_result(examno)
            if result_response.success:
                result_text = self.messages.format_exam_result_from_api(result_response.data)
            else:
                result_text = self.messages.format_exam_result(student, None)
        else:
            # Format result from database
            result_text = self.messages.format_exam_result(student, exam_result)
        
        await loading_msg.edit_text(
            result_text,
            reply_markup=self.keyboards.result_actions_keyboard(examno)
        )
        
        # Reset user session
        self._save_user_session(update.effective_user.id, "main_menu")
    
    async def _share_result(self, query, examno: str) -> None:
        """Handle result sharing"""
        # Get student info for sharing
        student = supabase_client.get_student_by_examno(examno)
        if not student:
            await query.answer("❌ خطأ في مشاركة النتيجة", show_alert=True)
            return
        
        share_text = self.messages.get_sharing_message(student.aname, examno)
        
        try:
            # Send share message
            await query.message.reply_text(share_text)
            await query.answer("✅ تم تحضير رسالة المشاركة")
        except Exception as e:
            logger.error(f"Error sharing result: {e}")
            await query.answer("❌ خطأ في المشاركة", show_alert=True)
    
    async def _check_rate_limit(self, user_id: int) -> bool:
        """Check if user has exceeded rate limit"""
        try:
            current_count = await redis_cache.increment_rate_limit(user_id)
            return not RateLimitUtils.is_rate_limited(current_count, settings.max_requests_per_minute)
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True  # Allow on error
    
    async def _show_student_result_message(self, update: Update, examno: str) -> None:
        """Show student result via message (not callback)"""
        try:
            # This is a copy of _show_student_result but for message responses
            student_data = supabase_client.get_student_with_result(examno)
            
            if not student_data:
                await update.message.reply_text(
                    self.messages.NO_RESULTS_FOUND,
                    reply_markup=self.keyboards.back_to_main_keyboard()
                )
                return
            
            student = student_data['student']
            exam_result = student_data.get('exam_result')
            
            # Format result message
            result_text = self.messages.format_exam_result(student, exam_result)
            
            await update.message.reply_text(
                result_text,
                reply_markup=self.keyboards.result_actions_keyboard(examno)
            )
            
        except Exception as e:
            logger.error(f"Error showing student result message: {e}")
            await update.message.reply_text(
                self.messages.SYSTEM_ERROR,
                reply_markup=self.keyboards.back_to_main_keyboard()
            )

    def _save_user_session(self, user_id: int, state: str, history: dict = None) -> None:
        """Save user session state"""
        try:
            session = UserSession(
                user_id=user_id,
                current_state=state,
                search_history=history,
                created_at=datetime.now()
            )
            supabase_client.save_user_session(session)
        except Exception as e:
            logger.error(f"Error saving user session: {e}")
    
    async def _send_error_message(self, update: Update) -> None:
        """Send error message to user"""
        try:
            await update.message.reply_text(
                self.messages.SYSTEM_ERROR,
                reply_markup=self.keyboards.error_keyboard()
            )
        except Exception:
            pass
    
    async def _send_callback_error(self, query) -> None:
        """Send error message for callback query"""
        try:
            await query.edit_message_text(
                self.messages.SYSTEM_ERROR,
                reply_markup=self.keyboards.error_keyboard()
            )
        except Exception:
            pass

    async def _check_channel_subscription(self, user_id: int) -> bool:
        """Check if user is subscribed to required channel"""
        # Temporarily disabled - bot needs to be added as admin to channel first
        logger.info(f"Subscription check disabled for user {user_id} - allowing access")
        return True

    async def _handle_subscription_check(self, query) -> None:
        """Handle subscription check callback"""
        try:
            user_id = query.from_user.id
            
            if await self._check_channel_subscription(user_id):
                await query.edit_message_text(
                    self.messages.SUBSCRIPTION_SUCCESS,
                    reply_markup=self.keyboards.main_menu()
                )
            else:
                await self._send_subscription_message(query)
                await query.answer(self.messages.SUBSCRIPTION_FAILED, show_alert=True)
        except Exception as e:
            logger.error(f"Error handling subscription check: {e}")
            await query.answer("❌ خطأ في التحقق من الاشتراك", show_alert=True)

    async def _send_subscription_message(self, update_or_query) -> bool:
        """Send subscription requirement message with inline buttons."""
        try:
            message_text = f"""🔒 عذراً، يجب الاشتراك في القناة التالية لاستخدام البوت:

📢 قناة: {settings.required_channel_title}
🆔 {settings.required_channel_username}

💡 بعد الاشتراك، اضغط على 'تحقق من الاشتراك'"""
            
            keyboard = [
                [InlineKeyboardButton(
                    f"📢 اشترك في {settings.required_channel_title}", 
                    url=f"https://t.me/{settings.required_channel_username.replace('@', '')}"
                )],
                [InlineKeyboardButton(
                    "✅ تحقق من الاشتراك", 
                    callback_data="check_subscription"
                )]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Handle both Update (message) and CallbackQuery objects
            if hasattr(update_or_query, 'callback_query') and update_or_query.callback_query:
                # This is an Update with callback_query
                await update_or_query.callback_query.edit_message_text(
                    message_text, 
                    reply_markup=reply_markup
                )
            elif hasattr(update_or_query, 'edit_message_text'):
                # This is a CallbackQuery object directly
                await update_or_query.edit_message_text(
                    message_text, 
                    reply_markup=reply_markup
                )
            elif hasattr(update_or_query, 'message'):
                # This is an Update object with a message
                await update_or_query.message.reply_text(
                    message_text, 
                    reply_markup=reply_markup
                )
            else:
                logger.error(f"❌ Unknown update type in send_subscription_message: {type(update_or_query)}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending subscription message: {e}")
            return False


class TelegramBotManager:
    """Manages bot instances - single bot mode with failover capability"""
    
    def __init__(self):
        self.applications: Dict[int, Application] = {}
        self.active_bots: List[Bot] = []
        self.handlers: Dict[int, BotHandlers] = {}
        self.primary_bot_id = 0  # Primary bot is always at index 0
        self.is_single_bot_mode = settings.use_single_bot
    
    async def initialize(self) -> None:
        """Initialize bot instance(s)"""
        active_tokens = settings.active_bot_tokens
        
        if not active_tokens:
            raise ValueError("No bot tokens configured")
        
        if self.is_single_bot_mode:
            logger.info("Initializing in SINGLE BOT mode...")
            logger.info(f"Primary bot token: {active_tokens[0][:10]}...")
            logger.info(f"Backup tokens available: {len(settings.backup_tokens)}")
            
            # Initialize only the primary bot
            await self._create_bot_instance(0, active_tokens[0])
        else:
            logger.info(f"Initializing in MULTI-BOT mode with {len(active_tokens)} bot instances...")
            
            for i, token in enumerate(active_tokens):
                await self._create_bot_instance(i, token)
        
        logger.info(f"Successfully initialized {len(self.applications)} bot instance(s)")
    
    async def _create_bot_instance(self, shard_id: int, token: str) -> None:
        """Create a single bot instance"""
        try:
            # Create application
            application = Application.builder().token(token).build()
            
            # Create handlers for this shard
            handlers = BotHandlers(shard_id)
            
            # Add handlers
            application.add_handler(CommandHandler("start", handlers.start_command))
            application.add_handler(CallbackQueryHandler(handlers.button_callback))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.text_message))
            
            # Initialize application
            await application.initialize()
            
            # Store instances
            self.applications[shard_id] = application
            self.active_bots.append(application.bot)
            self.handlers[shard_id] = handlers
            
            logger.info(f"Bot shard {shard_id} initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to create bot instance {shard_id}: {e}")
            raise
    
    async def process_update(self, shard_id: int, update_data: dict) -> None:
        """Process incoming update for specific shard"""
        try:
            if self.is_single_bot_mode:
                # In single bot mode, all updates go to the primary bot (shard 0)
                target_shard = self.primary_bot_id
            else:
                # In multi-bot mode, use the specified shard
                target_shard = shard_id
            
            if target_shard not in self.applications:
                logger.error(f"Target shard {target_shard} not available")
                return
            
            application = self.applications[target_shard]
            update = Update.de_json(update_data, application.bot)
            
            if update:
                await application.process_update(update)
            
        except Exception as e:
            logger.error(f"Error processing update for shard {shard_id} (target: {target_shard if 'target_shard' in locals() else 'unknown'}): {e}")
    
    async def get_stats(self) -> dict:
        """Get bot statistics"""
        return {
            "mode": "single_bot" if self.is_single_bot_mode else "multi_bot",
            "active_shards": len(self.applications),
            "total_bots": len(self.active_bots),
            "shard_ids": list(self.applications.keys()),
            "primary_bot_id": self.primary_bot_id if self.is_single_bot_mode else None,
            "backup_tokens_available": len(settings.backup_tokens) if self.is_single_bot_mode else None
        }
    
    async def shutdown(self) -> None:
        """Shutdown all bot instances"""
        logger.info("Shutting down bot instances...")
        
        for application in self.applications.values():
            try:
                await application.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down application: {e}")
        
        self.applications.clear()
        self.active_bots.clear()
        self.handlers.clear()
        
        logger.info("All bot instances shut down")