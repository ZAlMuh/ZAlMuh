from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.database.models import Student


class ArabicKeyboards:
    """Arabic inline keyboards for the bot"""
    
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Main menu with search options"""
        keyboard = [
            [
                InlineKeyboardButton("🔎 الاسم", callback_data="search_name"),
                InlineKeyboardButton("🆔 الرقم الامتحاني", callback_data="search_examno")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def governorates_keyboard(governorates: List[str]) -> InlineKeyboardMarkup:
        """Governorates selection keyboard"""
        keyboard = []
        
        # Add governorates in rows of 2
        for i in range(0, len(governorates), 2):
            row = []
            for j in range(i, min(i + 2, len(governorates))):
                gov = governorates[j]
                row.append(InlineKeyboardButton(gov, callback_data=f"gov_{gov}"))
            keyboard.append(row)
        
        # Add back button
        keyboard.append([InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def student_results_keyboard(students: List[Student]) -> InlineKeyboardMarkup:
        """Keyboard for selecting from multiple student results"""
        keyboard = []
        
        for i, student in enumerate(students):
            button_text = f"{student.aname} - {student.sch_name}"
            # Truncate if too long
            if len(button_text) > 30:
                button_text = button_text[:27] + "..."
            
            keyboard.append([
                InlineKeyboardButton(
                    button_text, 
                    callback_data=f"select_student_{student.examno}"
                )
            ])
        
        # Add back button
        keyboard.append([InlineKeyboardButton("🔙 بحث جديد", callback_data="search_name")])
        keyboard.append([InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def result_actions_keyboard(examno: str) -> InlineKeyboardMarkup:
        """Actions keyboard after showing result"""
        keyboard = [
            [
                InlineKeyboardButton("📤 مشاركة النتيجة", callback_data=f"share_{examno}"),
                InlineKeyboardButton("🔍 بحث آخر", callback_data="main_menu")
            ],
            [
                InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_to_main_keyboard() -> InlineKeyboardMarkup:
        """Simple back to main menu keyboard"""
        keyboard = [
            [InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def pagination_keyboard(
        current_page: int, 
        total_pages: int, 
        prefix: str = "page"
    ) -> InlineKeyboardMarkup:
        """Pagination keyboard for search results"""
        keyboard = []
        
        if total_pages > 1:
            row = []
            
            # Previous page
            if current_page > 1:
                row.append(InlineKeyboardButton("◀️ السابق", callback_data=f"{prefix}_{current_page-1}"))
            
            # Page indicator
            row.append(InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="noop"))
            
            # Next page
            if current_page < total_pages:
                row.append(InlineKeyboardButton("التالي ▶️", callback_data=f"{prefix}_{current_page+1}"))
            
            keyboard.append(row)
        
        # Back to main
        keyboard.append([InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirm_keyboard(action: str, data: str) -> InlineKeyboardMarkup:
        """Confirmation keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("✅ نعم", callback_data=f"confirm_{action}_{data}"),
                InlineKeyboardButton("❌ لا", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def error_keyboard() -> InlineKeyboardMarkup:
        """Error keyboard with retry option"""
        keyboard = [
            [
                InlineKeyboardButton("🔄 إعادة المحاولة", callback_data="main_menu"),
                InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)