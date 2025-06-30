import asyncio
import logging
from typing import Optional, Dict, Any
import httpx
from app.config import settings
from app.external.cache import redis_cache
from app.database.models import ExamResultResponse

logger = logging.getLogger(__name__)


class NajahAPIClient:
    def __init__(self):
        self.base_url = settings.najah_api_base_url
        self.timeout = 30.0
        self.max_retries = 3
        
    async def get_exam_result(self, exam_id: str) -> ExamResultResponse:
        """Get exam result from external API with caching"""
        
        # Check cache first
        cache_key = redis_cache.get_cache_key("exam_result", exam_id)
        cached_result = await redis_cache.get(cache_key)
        
        if cached_result:
            logger.info(f"Cache hit for exam result: {exam_id}")
            return ExamResultResponse(success=True, data=cached_result)
        
        # Fetch from API
        logger.info(f"Fetching exam result from API: {exam_id}")
        
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    url = f"{self.base_url}/exam-result/{exam_id}"
                    response = await client.get(url)
                    
                    if response.status_code == 200:
                        result_data = response.json()
                        
                        # Cache the successful result
                        await redis_cache.set(cache_key, result_data)
                        
                        logger.info(f"Successfully fetched exam result: {exam_id}")
                        return ExamResultResponse(success=True, data=result_data)
                    
                    elif response.status_code == 404:
                        logger.warning(f"Exam result not found: {exam_id}")
                        return ExamResultResponse(
                            success=False, 
                            error="لم يتم العثور على نتيجة لهذا الرقم الامتحاني"
                        )
                    
                    else:
                        logger.error(f"API returned status {response.status_code} for exam_id: {exam_id}")
                        if attempt == self.max_retries - 1:
                            return ExamResultResponse(
                                success=False,
                                error="خطأ في خدمة النتائج"
                            )
                        
            except httpx.TimeoutException:
                logger.error(f"Timeout fetching exam result (attempt {attempt + 1}): {exam_id}")
                if attempt == self.max_retries - 1:
                    return ExamResultResponse(
                        success=False,
                        error="انتهت مهلة الاتصال بخدمة النتائج"
                    )
            
            except httpx.RequestError as e:
                logger.error(f"Request error fetching exam result (attempt {attempt + 1}): {exam_id}, error: {e}")
                if attempt == self.max_retries - 1:
                    return ExamResultResponse(
                        success=False,
                        error="خطأ في الاتصال بخدمة النتائج"
                    )
            
            except Exception as e:
                logger.error(f"Unexpected error fetching exam result (attempt {attempt + 1}): {exam_id}, error: {e}")
                if attempt == self.max_retries - 1:
                    return ExamResultResponse(
                        success=False,
                        error="حدث خطأ غير متوقع"
                    )
            
            # Wait before retry
            if attempt < self.max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return ExamResultResponse(
            success=False,
            error="فشل في الحصول على النتيجة بعد عدة محاولات"
        )
    
    async def health_check(self) -> bool:
        """Check if the API is healthy"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Try to hit a health endpoint or just check connectivity
                response = await client.get(f"{self.base_url}/health", follow_redirects=True)
                return response.status_code == 200
        except Exception as e:
            logger.error(f"API health check failed: {e}")
            return False


# Global API client instance
najah_api = NajahAPIClient()