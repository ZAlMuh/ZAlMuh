import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ValidationUtils:
    """Validation utilities for user inputs"""
    
    @staticmethod
    def validate_exam_number(examno: str) -> bool:
        """Validate exam number format (15 digits)"""
        if not examno:
            return False
        
        # Remove any whitespace
        examno = examno.strip()
        
        # Check if it's exactly 15 digits
        if len(examno) != 15:
            return False
        
        # Check if all characters are digits
        if not examno.isdigit():
            return False
        
        return True
    
    @staticmethod
    def clean_exam_number(examno: str) -> Optional[str]:
        """Clean and validate exam number"""
        if not examno:
            return None
        
        # Remove all non-digit characters
        cleaned = re.sub(r'\D', '', examno.strip())
        
        if ValidationUtils.validate_exam_number(cleaned):
            return cleaned
        
        return None
    
    @staticmethod
    def validate_arabic_name(name: str) -> bool:
        """Validate Arabic name input"""
        if not name or len(name.strip()) < 2:
            return False
        
        name = name.strip()
        
        # Check if name contains Arabic characters
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\s]+')
        
        if not arabic_pattern.match(name):
            return False
        
        # Name should be between 2 and 50 characters
        if len(name) < 2 or len(name) > 50:
            return False
        
        return True
    
    @staticmethod
    def clean_arabic_name(name: str) -> Optional[str]:
        """Clean Arabic name input"""
        if not name:
            return None
        
        # Remove extra whitespace and normalize
        cleaned = ' '.join(name.strip().split())
        
        if ValidationUtils.validate_arabic_name(cleaned):
            return cleaned
        
        return None
    
    @staticmethod
    def validate_governorate(gov_name: str, valid_governorates: list) -> bool:
        """Validate governorate selection"""
        if not gov_name or not valid_governorates:
            return False
        
        return gov_name.strip() in valid_governorates
    
    @staticmethod
    def is_spam_input(text: str) -> bool:
        """Check if input looks like spam"""
        if not text:
            return False
        
        text = text.strip()
        
        # Check for repeated characters (more than 5 in a row)
        if re.search(r'(.)\1{5,}', text):
            return True
        
        # Check for excessive length
        if len(text) > 100:
            return True
        
        # Check for too many numbers in a name search
        if len(re.findall(r'\d', text)) > len(text) * 0.7:
            return True
        
        return False
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        if not text:
            return ""
        
        # Remove potentially harmful characters but keep Arabic
        # Remove HTML/XML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Truncate if too long
        if len(text) > 100:
            text = text[:100]
        
        return text.strip()


class RateLimitUtils:
    """Rate limiting utilities"""
    
    @staticmethod
    def is_rate_limited(current_count: int, max_requests: int = None) -> bool:
        """Check if user has exceeded rate limit"""
        max_requests = max_requests or 3  # Default from settings
        return current_count >= max_requests
    
    @staticmethod
    def get_remaining_requests(current_count: int, max_requests: int = None) -> int:
        """Get remaining requests for user"""
        max_requests = max_requests or 3
        remaining = max_requests - current_count
        return max(0, remaining)
    
    @staticmethod
    def format_rate_limit_message(remaining: int, window_seconds: int = 60) -> str:
        """Format rate limit message in Arabic"""
        if remaining <= 0:
            return f"⏰ تم تجاوز الحد المسموح\nيرجى الانتظار {window_seconds} ثانية"
        else:
            return f"⚠️ تبقى لديك {remaining} طلبات في هذه الدقيقة"