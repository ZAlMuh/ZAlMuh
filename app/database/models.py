from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class Student(BaseModel):
    id: Optional[int] = None
    examno: str
    aname: Optional[str] = None
    gov_name: Optional[str] = None
    gov_code: Optional[str] = None
    sch_name: Optional[str] = None
    sch_code: Optional[str] = None
    sexcode: Optional[str] = None
    accname: Optional[str] = None


class ExamResult(BaseModel):
    examno: str
    stucases: Optional[str] = None
    finalgrd: Optional[str] = None
    finalrate: Optional[str] = None
    # Subject 1
    sub1_name: Optional[str] = None
    sub1_score: Optional[str] = None
    sub1_cscore: Optional[str] = None
    # Subject 2
    sub2_name: Optional[str] = None
    sub2_score: Optional[str] = None
    sub2_cscore: Optional[str] = None
    # Subject 3
    sub3_name: Optional[str] = None
    sub3_score: Optional[str] = None
    sub3_cscore: Optional[str] = None
    # Subject 4
    sub4_name: Optional[str] = None
    sub4_score: Optional[str] = None
    sub4_cscore: Optional[str] = None
    # Subject 5
    sub5_name: Optional[str] = None
    sub5_score: Optional[str] = None
    sub5_cscore: Optional[str] = None
    # Subject 6
    sub6_name: Optional[str] = None
    sub6_score: Optional[str] = None
    sub6_cscore: Optional[str] = None
    # Subject 7
    sub7_name: Optional[str] = None
    sub7_score: Optional[str] = None
    sub7_cscore: Optional[str] = None
    # Subject 8
    sub8_name: Optional[str] = None
    sub8_score: Optional[str] = None
    sub8_cscore: Optional[str] = None
    # Subject 9
    sub9_name: Optional[str] = None
    sub9_score: Optional[str] = None
    sub9_cscore: Optional[str] = None

    def get_subjects_dict(self) -> Dict[str, str]:
        """Get subjects as a dictionary for easy formatting"""
        subjects = {}
        for i in range(1, 10):
            name_attr = f"sub{i}_name"
            score_attr = f"sub{i}_score"
            
            name = getattr(self, name_attr)
            score = getattr(self, score_attr)
            
            if name and score:
                subjects[name] = score
        
        return subjects


class ResultCache(BaseModel):
    examno: str
    api_response: Dict[str, Any]
    cached_at: datetime
    ttl: int


class UserSession(BaseModel):
    user_id: int
    current_state: str
    search_history: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None


class RateLimit(BaseModel):
    user_id: int
    request_count: int
    window_start: datetime


class SearchResult(BaseModel):
    students: list[Student]
    total_count: int
    has_more: bool


class ExamResultResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None