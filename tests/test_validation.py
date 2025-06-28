import pytest
from app.utils.validation import ValidationUtils, RateLimitUtils


class TestValidationUtils:
    """Test validation utility functions"""
    
    def test_validate_exam_number_valid(self):
        """Test valid exam numbers"""
        valid_numbers = [
            "272591110430082",
            "123456789012345",
            "000000000000001"
        ]
        
        for number in valid_numbers:
            assert ValidationUtils.validate_exam_number(number) == True
    
    def test_validate_exam_number_invalid(self):
        """Test invalid exam numbers"""
        invalid_numbers = [
            "",
            "12345",  # Too short
            "1234567890123456",  # Too long
            "27259111043008a",  # Contains letter
            "272591110430082 ",  # Contains space
            "272-591-110-430-082",  # Contains dashes
            None
        ]
        
        for number in invalid_numbers:
            assert ValidationUtils.validate_exam_number(number) == False
    
    def test_clean_exam_number(self):
        """Test exam number cleaning"""
        test_cases = [
            ("272591110430082", "272591110430082"),
            ("272-591-110-430-082", "272591110430082"),
            ("272 591 110 430 082", "272591110430082"),
            ("272/591/110/430/082", "272591110430082"),
            ("abc272591110430082def", "272591110430082"),
            ("12345", None),  # Too short after cleaning
            ("", None),
            (None, None)
        ]
        
        for input_val, expected in test_cases:
            result = ValidationUtils.clean_exam_number(input_val)
            assert result == expected
    
    def test_validate_arabic_name_valid(self):
        """Test valid Arabic names"""
        valid_names = [
            "عبدالله أحمد",
            "فاطمة الزهراء",
            "محمد حسن علي",
            "زينب محمد كاظم الموسوي",
            "علي حسين"
        ]
        
        for name in valid_names:
            assert ValidationUtils.validate_arabic_name(name) == True
    
    def test_validate_arabic_name_invalid(self):
        """Test invalid Arabic names"""
        invalid_names = [
            "",
            "a",  # Too short
            "Ahmed",  # English
            "123",  # Numbers only
            "عبدالله" + "ا" * 50,  # Too long
            None,
            "   ",  # Only spaces
        ]
        
        for name in invalid_names:
            assert ValidationUtils.validate_arabic_name(name) == False
    
    def test_clean_arabic_name(self):
        """Test Arabic name cleaning"""
        test_cases = [
            ("  عبدالله أحمد  ", "عبدالله أحمد"),
            ("عبدالله    أحمد", "عبدالله أحمد"),
            ("فاطمة\nالزهراء", "فاطمة الزهراء"),
            ("", None),
            ("a", None),
            (None, None)
        ]
        
        for input_val, expected in test_cases:
            result = ValidationUtils.clean_arabic_name(input_val)
            assert result == expected
    
    def test_is_spam_input(self):
        """Test spam detection"""
        spam_inputs = [
            "aaaaaaaaaa",  # Repeated characters
            "a" * 101,  # Too long
            "1234567890",  # Too many numbers
        ]
        
        normal_inputs = [
            "عبدالله أحمد",
            "272591110430082",
            "test input",
        ]
        
        for spam in spam_inputs:
            assert ValidationUtils.is_spam_input(spam) == True
        
        for normal in normal_inputs:
            assert ValidationUtils.is_spam_input(normal) == False
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        test_cases = [
            ("<script>alert('test')</script>", ""),
            ("عبدالله <b>أحمد</b>", "عبدالله أحمد"),
            ("  test  input  ", "test input"),
            ("a" * 200, "a" * 100),  # Truncation
        ]
        
        for input_val, expected in test_cases:
            result = ValidationUtils.sanitize_input(input_val)
            assert result == expected


class TestRateLimitUtils:
    """Test rate limiting utility functions"""
    
    def test_is_rate_limited(self):
        """Test rate limit checking"""
        assert RateLimitUtils.is_rate_limited(2, 3) == False
        assert RateLimitUtils.is_rate_limited(3, 3) == True
        assert RateLimitUtils.is_rate_limited(5, 3) == True
        assert RateLimitUtils.is_rate_limited(0, 3) == False
    
    def test_get_remaining_requests(self):
        """Test remaining requests calculation"""
        assert RateLimitUtils.get_remaining_requests(0, 3) == 3
        assert RateLimitUtils.get_remaining_requests(2, 3) == 1
        assert RateLimitUtils.get_remaining_requests(3, 3) == 0
        assert RateLimitUtils.get_remaining_requests(5, 3) == 0
    
    def test_format_rate_limit_message(self):
        """Test rate limit message formatting"""
        message_exceeded = RateLimitUtils.format_rate_limit_message(0)
        assert "تجاوز الحد المسموح" in message_exceeded
        
        message_remaining = RateLimitUtils.format_rate_limit_message(2)
        assert "تبقى لديك 2 طلبات" in message_remaining


if __name__ == "__main__":
    pytest.main([__file__])