import asyncio
from typing import List, Optional, Dict, Any
from supabase import create_client, Client
from app.config import settings
from app.database.models import Student, SearchResult, UserSession, RateLimit
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )

    async def search_students_by_name(
        self, 
        name: str, 
        governorate: Optional[str] = None,
        limit: int = 5,
        offset: int = 0
    ) -> SearchResult:
        """Search students by name with optional governorate filter"""
        try:
            query = self.client.table("students").select("*")
            
            # Case-insensitive name search using aname field
            query = query.ilike("aname", f"%{name}%")
            
            if governorate:
                query = query.eq("gov_name", governorate)
            
            # Get total count first
            count_result = query.execute()
            total_count = len(count_result.data) if count_result.data else 0
            
            # Get paginated results
            result = query.range(offset, offset + limit - 1).execute()
            
            students = [Student(**student) for student in result.data] if result.data else []
            
            return SearchResult(
                students=students,
                total_count=total_count,
                has_more=total_count > offset + limit
            )
            
        except Exception as e:
            logger.error(f"Error searching students: {e}")
            return SearchResult(students=[], total_count=0, has_more=False)

    async def get_student_by_examno(self, examno: str) -> Optional[Student]:
        """Get student by exam number"""
        try:
            result = self.client.table("students").select("*").eq("examno", examno).execute()
            
            if result.data:
                return Student(**result.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error getting student by examno: {e}")
            return None

    async def get_governorates(self) -> List[str]:
        """Get list of unique governorates"""
        try:
            result = self.client.table("students").select("gov_name").execute()
            
            governorates = list(set([row["gov_name"] for row in result.data if row["gov_name"]]))
            return sorted(governorates)
            
        except Exception as e:
            logger.error(f"Error getting governorates: {e}")
            return []

    async def save_user_session(self, user_session: UserSession) -> bool:
        """Save or update user session"""
        try:
            result = self.client.table("user_sessions").upsert({
                "user_id": user_session.user_id,
                "current_state": user_session.current_state,
                "search_history": user_session.search_history,
                "created_at": user_session.created_at.isoformat() if user_session.created_at else None
            }).execute()
            
            return bool(result.data)
            
        except Exception as e:
            logger.error(f"Error saving user session: {e}")
            return False

    async def get_user_session(self, user_id: int) -> Optional[UserSession]:
        """Get user session by user ID"""
        try:
            result = self.client.table("user_sessions").select("*").eq("user_id", user_id).execute()
            
            if result.data:
                return UserSession(**result.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error getting user session: {e}")
            return None

    async def update_rate_limit(self, user_id: int, request_count: int) -> bool:
        """Update rate limit for user"""
        try:
            from datetime import datetime
            
            result = self.client.table("rate_limits").upsert({
                "user_id": user_id,
                "request_count": request_count,
                "window_start": datetime.now().isoformat()
            }).execute()
            
            return bool(result.data)
            
        except Exception as e:
            logger.error(f"Error updating rate limit: {e}")
            return False

    async def get_rate_limit(self, user_id: int) -> Optional[RateLimit]:
        """Get rate limit for user"""
        try:
            result = self.client.table("rate_limits").select("*").eq("user_id", user_id).execute()
            
            if result.data:
                return RateLimit(**result.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error getting rate limit: {e}")
            return None

    async def get_exam_result(self, examno: str) -> Optional['ExamResult']:
        """Get exam result by exam number"""
        try:
            result = self.client.table("exam_results").select("*").eq("examno", examno).execute()
            
            if result.data:
                from app.database.models import ExamResult
                return ExamResult(**result.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error getting exam result: {e}")
            return None

    async def get_student_with_result(self, examno: str) -> Optional[Dict[str, Any]]:
        """Get student information along with exam results"""
        try:
            # Get student info
            student = await self.get_student_by_examno(examno)
            if not student:
                return None
            
            # Get exam results
            exam_result = await self.get_exam_result(examno)
            
            return {
                "student": student,
                "exam_result": exam_result
            }
            
        except Exception as e:
            logger.error(f"Error getting student with result: {e}")
            return None


# Global instance
supabase_client = SupabaseClient()