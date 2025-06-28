import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from app.external.najah_api import NajahAPIClient
from app.external.cache import RedisCache
from app.database.models import ExamResultResponse


class TestNajahAPIClient:
    """Test external API client"""
    
    @pytest.fixture
    def api_client(self):
        """Create API client instance"""
        return NajahAPIClient()
    
    @pytest.fixture
    def mock_redis(self):
        """Mock Redis cache"""
        with patch('app.external.najah_api.redis_cache') as mock:
            mock.get = AsyncMock(return_value=None)
            mock.set = AsyncMock(return_value=True)
            mock.get_cache_key = MagicMock(return_value="exam_result:123")
            yield mock
    
    @pytest.mark.asyncio
    async def test_get_exam_result_success(self, api_client, mock_redis):
        """Test successful API call"""
        mock_response_data = {
            "name": "عبدالله أحمد",
            "examno": "272591110430082",
            "school": "متوسطة الكوثر",
            "governorate": "كربلاء",
            "subjects": {"الرياضيات": 85, "العربية": 78},
            "total": 163,
            "average": 81.5,
            "status": "ناجح"
        }
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )
            
            result = await api_client.get_exam_result("272591110430082")
            
            assert result.success == True
            assert result.data == mock_response_data
            assert result.error is None
            
            # Verify cache was called
            mock_redis.set.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_exam_result_cached(self, api_client, mock_redis):
        """Test cached result retrieval"""
        cached_data = {
            "name": "عبدالله أحمد",
            "examno": "272591110430082",
            "total": 163
        }
        
        mock_redis.get.return_value = cached_data
        
        result = await api_client.get_exam_result("272591110430082")
        
        assert result.success == True
        assert result.data == cached_data
        mock_redis.get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_exam_result_not_found(self, api_client, mock_redis):
        """Test 404 response"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 404
            
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )
            
            result = await api_client.get_exam_result("000000000000000")
            
            assert result.success == False
            assert "لم يتم العثور على نتيجة" in result.error
    
    @pytest.mark.asyncio
    async def test_get_exam_result_timeout(self, api_client, mock_redis):
        """Test timeout handling"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=httpx.TimeoutException("Timeout")
            )
            
            result = await api_client.get_exam_result("272591110430082")
            
            assert result.success == False
            assert "انتهت مهلة الاتصال" in result.error
    
    @pytest.mark.asyncio
    async def test_get_exam_result_retry_logic(self, api_client, mock_redis):
        """Test retry logic on failures"""
        with patch('httpx.AsyncClient') as mock_client:
            # First two calls fail, third succeeds
            mock_responses = [
                httpx.RequestError("Connection failed"),
                httpx.RequestError("Connection failed"),
                MagicMock(status_code=200, json=lambda: {"success": True})
            ]
            
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=mock_responses
            )
            
            result = await api_client.get_exam_result("272591110430082")
            
            assert result.success == True
            # Should have made 3 attempts
            assert mock_client.return_value.__aenter__.return_value.get.call_count == 3


class TestRedisCache:
    """Test Redis cache functionality"""
    
    @pytest.fixture
    def cache(self):
        """Create cache instance"""
        return RedisCache()
    
    @pytest.mark.asyncio
    async def test_cache_operations(self, cache):
        """Test basic cache operations"""
        with patch('aioredis.from_url') as mock_redis_client:
            mock_redis = AsyncMock()
            mock_redis_client.return_value = mock_redis
            
            # Test connection
            await cache.connect()
            mock_redis.ping.assert_called_once()
            
            # Test set operation
            test_data = {"key": "value"}
            mock_redis.setex = AsyncMock()
            result = await cache.set("test_key", test_data, 300)
            assert result == True
            mock_redis.setex.assert_called_once()
            
            # Test get operation
            mock_redis.get = AsyncMock(return_value='{"key": "value"}')
            result = await cache.get("test_key")
            assert result == test_data
            
            # Test delete operation
            mock_redis.delete = AsyncMock()
            result = await cache.delete("test_key")
            assert result == True
            mock_redis.delete.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self, cache):
        """Test rate limiting functionality"""
        with patch('aioredis.from_url') as mock_redis_client:
            mock_redis = AsyncMock()
            mock_redis_client.return_value = mock_redis
            
            await cache.connect()
            
            # Test rate limit increment
            mock_pipeline = AsyncMock()
            mock_pipeline.execute = AsyncMock(return_value=[3])  # 3rd request
            mock_redis.pipeline.return_value = mock_pipeline
            
            count = await cache.increment_rate_limit(12345)
            assert count == 3
            
            # Test rate limit count retrieval
            mock_redis.get = AsyncMock(return_value="2")
            count = await cache.get_rate_limit_count(12345)
            assert count == 2
    
    def test_cache_key_generation(self, cache):
        """Test cache key generation"""
        key = cache.get_cache_key("exam_result", "272591110430082")
        assert key == "exam_result:272591110430082"


if __name__ == "__main__":
    pytest.main([__file__])