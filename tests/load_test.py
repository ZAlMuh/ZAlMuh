#!/usr/bin/env python3
"""
Load testing script for Arabic Telegram Bot
Simulates high-traffic scenarios up to 100K concurrent users
"""

import asyncio
import aiohttp
import time
import random
import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any
import argparse
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TestConfig:
    """Test configuration"""
    base_url: str = "http://localhost"
    concurrent_users: int = 1000
    requests_per_user: int = 10
    test_duration: int = 300  # seconds
    ramp_up_time: int = 60   # seconds
    webhook_endpoints: List[str] = None
    
    def __post_init__(self):
        if self.webhook_endpoints is None:
            self.webhook_endpoints = [f"/webhook/{i}" for i in range(5)]


@dataclass
class TestResult:
    """Test result metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0
    max_response_time: float = 0.0
    min_response_time: float = float('inf')
    errors: Dict[str, int] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = {}


class TelegramUpdateGenerator:
    """Generate realistic Telegram update payloads"""
    
    def __init__(self):
        self.user_id_counter = 10000
        self.message_id_counter = 1000
        
        self.arabic_names = [
            "عبدالله أحمد", "فاطمة الزهراء", "محمد حسن",
            "زينب علي", "علي حسين", "مريم محمد",
            "حسن عبدالله", "خديجة أحمد", "يوسف علي"
        ]
        
        self.exam_numbers = [
            "272591110430082", "272591110430083", "272591110430084",
            "272591110430085", "272591110430086", "272591110430087"
        ]
    
    def generate_start_command(self) -> Dict[str, Any]:
        """Generate /start command update"""
        user_id = self.user_id_counter
        self.user_id_counter += 1
        message_id = self.message_id_counter
        self.message_id_counter += 1
        
        return {
            "update_id": random.randint(100000, 999999),
            "message": {
                "message_id": message_id,
                "from": {
                    "id": user_id,
                    "is_bot": False,
                    "first_name": random.choice(self.arabic_names).split()[0],
                    "username": f"user{user_id}",
                    "language_code": "ar"
                },
                "chat": {
                    "id": user_id,
                    "first_name": random.choice(self.arabic_names).split()[0],
                    "type": "private"
                },
                "date": int(time.time()),
                "text": "/start",
                "entities": [
                    {
                        "offset": 0,
                        "length": 6,
                        "type": "bot_command"
                    }
                ]
            }
        }
    
    def generate_name_search(self, user_id: int) -> Dict[str, Any]:
        """Generate name search message"""
        message_id = self.message_id_counter
        self.message_id_counter += 1
        
        return {
            "update_id": random.randint(100000, 999999),
            "message": {
                "message_id": message_id,
                "from": {
                    "id": user_id,
                    "is_bot": False,
                    "first_name": "User",
                    "language_code": "ar"
                },
                "chat": {
                    "id": user_id,
                    "type": "private"
                },
                "date": int(time.time()),
                "text": random.choice(self.arabic_names)
            }
        }
    
    def generate_examno_search(self, user_id: int) -> Dict[str, Any]:
        """Generate exam number search message"""
        message_id = self.message_id_counter
        self.message_id_counter += 1
        
        return {
            "update_id": random.randint(100000, 999999),
            "message": {
                "message_id": message_id,
                "from": {
                    "id": user_id,
                    "is_bot": False,
                    "first_name": "User",
                    "language_code": "ar"
                },
                "chat": {
                    "id": user_id,
                    "type": "private"
                },
                "date": int(time.time()),
                "text": random.choice(self.exam_numbers)
            }
        }
    
    def generate_callback_query(self, user_id: int, callback_data: str) -> Dict[str, Any]:
        """Generate callback query update"""
        return {
            "update_id": random.randint(100000, 999999),
            "callback_query": {
                "id": str(random.randint(100000000000000000, 999999999999999999)),
                "from": {
                    "id": user_id,
                    "is_bot": False,
                    "first_name": "User",
                    "language_code": "ar"
                },
                "message": {
                    "message_id": self.message_id_counter,
                    "from": {
                        "id": 123456789,  # Bot ID
                        "is_bot": True,
                        "first_name": "ExamBot",
                        "username": "exam_results_bot"
                    },
                    "chat": {
                        "id": user_id,
                        "type": "private"
                    },
                    "date": int(time.time()),
                    "text": "أهلاً بك في بوت نتائج الطلبة!"
                },
                "data": callback_data
            }
        }


class LoadTester:
    """Main load testing class"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.update_generator = TelegramUpdateGenerator()
        self.results = TestResult()
        self.response_times = []
        
    async def simulate_user_session(self, session: aiohttp.ClientSession, user_id: int) -> None:
        """Simulate a complete user session"""
        try:
            # 1. Start command
            await self.send_update(session, self.update_generator.generate_start_command())
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            # 2. Random search type
            if random.choice([True, False]):
                # Name search flow
                await self.send_update(session, self.update_generator.generate_callback_query(user_id, "search_name"))
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
                await self.send_update(session, self.update_generator.generate_name_search(user_id))
                await asyncio.sleep(random.uniform(1.0, 3.0))
                
                # Select governorate
                await self.send_update(session, self.update_generator.generate_callback_query(user_id, "gov_كربلاء"))
                await asyncio.sleep(random.uniform(1.0, 2.0))
            else:
                # Exam number search flow
                await self.send_update(session, self.update_generator.generate_callback_query(user_id, "search_examno"))
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
                await self.send_update(session, self.update_generator.generate_examno_search(user_id))
                await asyncio.sleep(random.uniform(2.0, 4.0))  # Longer for API call
            
        except Exception as e:
            logger.error(f"Error in user session {user_id}: {e}")
    
    async def send_update(self, session: aiohttp.ClientSession, update_data: Dict[str, Any]) -> None:
        """Send a single update to the bot"""
        start_time = time.time()
        
        try:
            # Choose random shard based on user ID
            user_id = update_data.get("message", {}).get("from", {}).get("id") or \
                     update_data.get("callback_query", {}).get("from", {}).get("id", 0)
            
            shard_id = user_id % len(self.config.webhook_endpoints)
            endpoint = self.config.webhook_endpoints[shard_id]
            url = f"{self.config.base_url}{endpoint}"
            
            async with session.post(
                url,
                json=update_data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                response_time = time.time() - start_time
                self.response_times.append(response_time)
                
                if response.status == 200:
                    self.results.successful_requests += 1
                else:
                    self.results.failed_requests += 1
                    error_key = f"HTTP_{response.status}"
                    self.results.errors[error_key] = self.results.errors.get(error_key, 0) + 1
                
                self.results.total_requests += 1
                
        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            self.results.failed_requests += 1
            self.results.errors["TIMEOUT"] = self.results.errors.get("TIMEOUT", 0) + 1
            self.results.total_requests += 1
            
        except Exception as e:
            response_time = time.time() - start_time
            self.results.failed_requests += 1
            error_key = f"ERROR_{type(e).__name__}"
            self.results.errors[error_key] = self.results.errors.get(error_key, 0) + 1
            self.results.total_requests += 1
    
    async def run_load_test(self) -> TestResult:
        """Run the complete load test"""
        logger.info(f"Starting load test with {self.config.concurrent_users} concurrent users")
        logger.info(f"Test duration: {self.config.test_duration} seconds")
        logger.info(f"Ramp-up time: {self.config.ramp_up_time} seconds")
        
        # Create connector with appropriate limits
        connector = aiohttp.TCPConnector(
            limit=self.config.concurrent_users * 2,
            limit_per_host=self.config.concurrent_users * 2,
            keepalive_timeout=30
        )
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            
            # Ramp up users gradually
            users_per_interval = self.config.concurrent_users // 10
            interval = self.config.ramp_up_time / 10
            
            for batch in range(10):
                batch_start_user_id = batch * users_per_interval + 10000
                
                # Create tasks for this batch
                for i in range(users_per_interval):
                    user_id = batch_start_user_id + i
                    task = asyncio.create_task(
                        self.simulate_user_session(session, user_id)
                    )
                    tasks.append(task)
                
                logger.info(f"Started batch {batch + 1}/10 ({len(tasks)} total users)")
                
                if batch < 9:  # Don't sleep after the last batch
                    await asyncio.sleep(interval)
            
            # Wait for all tasks to complete or timeout
            try:
                await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=self.config.test_duration
                )
            except asyncio.TimeoutError:
                logger.warning("Test timed out, cancelling remaining tasks")
                for task in tasks:
                    if not task.done():
                        task.cancel()
        
        # Calculate final metrics
        if self.response_times:
            self.results.avg_response_time = sum(self.response_times) / len(self.response_times)
            self.results.max_response_time = max(self.response_times)
            self.results.min_response_time = min(self.response_times)
        
        return self.results
    
    def print_results(self) -> None:
        """Print test results"""
        print("\n" + "="*60)
        print("LOAD TEST RESULTS")
        print("="*60)
        print(f"Total Requests: {self.results.total_requests}")
        print(f"Successful Requests: {self.results.successful_requests}")
        print(f"Failed Requests: {self.results.failed_requests}")
        print(f"Success Rate: {(self.results.successful_requests / max(self.results.total_requests, 1)) * 100:.2f}%")
        print(f"Average Response Time: {self.results.avg_response_time:.3f}s")
        print(f"Max Response Time: {self.results.max_response_time:.3f}s")
        print(f"Min Response Time: {self.results.min_response_time:.3f}s")
        
        if self.results.errors:
            print("\nERRORS:")
            for error, count in self.results.errors.items():
                print(f"  {error}: {count}")
        
        # Performance metrics
        total_time = self.config.test_duration
        requests_per_second = self.results.total_requests / total_time
        print(f"\nRequests per second: {requests_per_second:.2f}")
        
        print("="*60)


async def run_health_check(base_url: str) -> bool:
    """Check if the service is healthy before testing"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/health", timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    health_data = await response.json()
                    logger.info(f"Health check passed: {health_data}")
                    return True
                else:
                    logger.error(f"Health check failed with status {response.status}")
                    return False
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Load test Arabic Telegram Bot")
    parser.add_argument("--url", default="http://localhost", help="Base URL of the service")
    parser.add_argument("--users", type=int, default=1000, help="Number of concurrent users")
    parser.add_argument("--duration", type=int, default=300, help="Test duration in seconds")
    parser.add_argument("--rampup", type=int, default=60, help="Ramp-up time in seconds")
    parser.add_argument("--skip-health", action="store_true", help="Skip health check")
    
    args = parser.parse_args()
    
    config = TestConfig(
        base_url=args.url,
        concurrent_users=args.users,
        test_duration=args.duration,
        ramp_up_time=args.rampup
    )
    
    async def run_test():
        # Health check
        if not args.skip_health:
            logger.info("Performing health check...")
            if not await run_health_check(config.base_url):
                logger.error("Health check failed. Exiting.")
                return
            logger.info("Health check passed. Starting load test...")
        
        # Run load test
        tester = LoadTester(config)
        await tester.run_load_test()
        tester.print_results()
    
    # Run the test
    asyncio.run(run_test())


if __name__ == "__main__":
    main()