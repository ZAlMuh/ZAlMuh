from typing import Dict, Any, List
from app.database.models import Student


class ArabicMessages:
    """Arabic message templates for the bot"""
    
    # Welcome and menu messages
    WELCOME_MESSAGE = """أهلاً بك في بوت نتائج الطلبة! 📊
اختر طريقة البحث:"""

    SUBSCRIPTION_REQUIRED = """📢 للاستفادة من خدمات البوت، يجب عليك الاشتراك في قناتنا أولاً:

📺 قناة: {channel_title}
🆔 {channel_username}

👈 اضغط على "اشتراك في القناة" ثم ارجع واضغط "تم الاشتراك - تحقق" """

    SUBSCRIPTION_SUCCESS = """✅ شكراً لك! تم التحقق من اشتراكك بنجاح
يمكنك الآن استخدام جميع خدمات البوت 🎉"""

    SUBSCRIPTION_FAILED = """❌ لم يتم العثور على اشتراكك في القناة
يرجى التأكد من الاشتراك في القناة أولاً ثم المحاولة مرة أخرى"""

    MAIN_MENU_HELP = """يمكنك استخدام الأزرار التالية:
🔎 البحث بالاسم - للبحث عن الطالب باستخدام الاسم
🆔 البحث بالرقم الامتحاني - للبحث باستخدام الرقم الامتحاني مباشرة"""

    # Search messages
    NAME_SEARCH_PROMPT = """أدخل اسم الطالب للبحث:
مثال: عبدالله أحمد"""

    GOVERNORATE_SELECT_PROMPT = """اختر المحافظة:"""

    EXAMNO_SEARCH_PROMPT = """أدخل الرقم الامتحاني (15 رقم):
مثال: 272591110430082"""

    # Validation messages
    INVALID_EXAMNO = """❌ رقم امتحاني غير صحيح
يجب أن يكون الرقم 15 رقماً فقط
مثال: 272591110430082"""

    INVALID_NAME = """❌ اسم غير صحيح
يرجى إدخال اسم صحيح باللغة العربية"""

    # Search results
    NO_RESULTS_FOUND = """❌ لم يتم العثور على نتائج
تأكد من صحة البيانات المدخلة"""

    MULTIPLE_RESULTS_FOUND = """تم العثور على عدة نتائج:
اختر الطالب المطلوب:"""

    # Rate limiting
    RATE_LIMIT_EXCEEDED = """⏰ تم تجاوز الحد المسموح
يرجى الانتظار قبل إجراء بحث جديد
الحد المسموح: 3 طلبات في الدقيقة"""

    # Error messages
    SYSTEM_ERROR = """❌ حدث خطأ في النظام
يرجى المحاولة مرة أخرى لاحقاً"""

    API_ERROR = """❌ خطأ في الاتصال بخدمة النتائج
يرجى المحاولة مرة أخرى"""

    DATABASE_ERROR = """❌ خطأ في قاعدة البيانات
يرجى المحاولة مرة أخرى"""

    # Success messages
    RESULT_FETCHED = """✅ تم العثور على النتيجة"""

    @staticmethod
    def format_student_info(student: Student) -> str:
        """Format student information for display"""
        name = student.aname or "غير متوفر"
        school = student.sch_name or "غير متوفر"
        governorate = student.gov_name or "غير متوفر"
        
        return f"""👤 {name}
🏫 {school}
🆔 {student.examno}
📍 {governorate}"""

    @staticmethod
    def format_search_results(students: List[Student]) -> str:
        """Format multiple search results"""
        if not students:
            return ArabicMessages.NO_RESULTS_FOUND
        
        results = [ArabicMessages.MULTIPLE_RESULTS_FOUND]
        for i, student in enumerate(students, 1):
            results.append(f"\n{i}. {ArabicMessages.format_student_info(student)}")
        
        return "\n".join(results)

    @staticmethod
    def format_exam_result(student: Student, exam_result: 'ExamResult') -> str:
        """Format exam result from database data"""
        try:
            from app.database.models import ExamResult
            
            # Student information
            name = student.aname or "غير متوفر"
            examno = student.examno
            school = student.sch_name or "غير متوفر"
            governorate = student.gov_name or "غير متوفر"
            
            # Gender mapping
            gender_map = {"M": "ذكر", "F": "أنثى", "1": "ذكر", "2": "أنثى"}
            gender = gender_map.get(student.sexcode, student.sexcode or "غير متوفر")
            
            # Build result text
            result_text = f"""👤 الاسم: {name}
🆔 الرقم الامتحاني: {examno}
🏫 المدرسة: {school}
🏛️ المحافظة: {governorate}
👨‍🎓 الجنس: {gender}"""
            
            if exam_result:
                # Format subject scores
                subjects = exam_result.get_subjects_dict()
                if subjects:
                    result_text += "\n\n📚 الدرجات:"
                    for subject_name, score in subjects.items():
                        result_text += f"\n• {subject_name}: {score}"
                
                # Final grade and rate
                if exam_result.finalgrd:
                    result_text += f"\n\n📈 الدرجة النهائية: {exam_result.finalgrd}"
                
                if exam_result.finalrate:
                    result_text += f"\n٪ المعدل النهائي: {exam_result.finalrate}"
                
                # Status
                status = exam_result.stucases or "غير متوفر"
                result_text += f"\n📋 الحالة: {status}"
            else:
                result_text += "\n\n❌ لا توجد نتائج متوفرة لهذا الطالب"
            
            return result_text
        
        except Exception as e:
            return f"❌ خطأ في تنسيق النتيجة: {str(e)}"
    
    @staticmethod
    def format_exam_result_from_api(result_data: Dict[str, Any]) -> str:
        """Format exam result from external API response (fallback)"""
        try:
            # Extract data from API response
            name = result_data.get("name", "غير متوفر")
            examno = result_data.get("examno", "غير متوفر")
            school = result_data.get("school", "غير متوفر")
            governorate = result_data.get("governorate", "غير متوفر")
            gender = result_data.get("gender", "غير متوفر")
            
            # Format subject scores
            subjects = result_data.get("subjects", {})
            scores_text = []
            for subject, score in subjects.items():
                scores_text.append(f"• {subject}: {score}")
            
            total = result_data.get("total", 0)
            average = result_data.get("average", 0)
            status = result_data.get("status", "غير متوفر")
            
            return f"""👤 الاسم: {name}
🆔 الرقم الامتحاني: {examno}
🏫 المدرسة: {school}
🏛️ المحافظة: {governorate}
👨‍🎓 الجنس: {gender}

📚 الدرجات:
{chr(10).join(scores_text)}

📈 المجموع: {total}
٪ المعدل: {average}
📋 الحالة: {status}"""
        
        except Exception:
            return "❌ خطأ في تنسيق النتيجة"

    @staticmethod
    def get_sharing_message(student_name: str, examno: str) -> str:
        """Generate sharing message"""
        return f"""🎉 تهانينا {student_name}!
🆔 رقم الامتحان: {examno}

📊 تم الحصول على النتيجة عبر بوت نتائج الطلبة
🤖 @exam_results_bot"""