from typing import List, Literal, Optional
from pydantic import BaseModel, Field

IdentifierType = Literal["email", "phone_number", "username"]
SourceType = Literal["forum", "marketplace", "paste_site"]
MatchType = Literal["keyword_match", "targeted_search_hit"]

class SearchRequest(BaseModel):
    identifier_type: IdentifierType
    identifier_value: str = Field(..., min_length=1, max_length=256)

class SearchAcceptedResponse(BaseModel):
    message: str
    task_id: str

class ResultItem(BaseModel):
    source_url: str
    source_type: SourceType
    capture_timestamp: str
    match_type: MatchType
    matched_keyword: Optional[str] = None
    content_snippet: str
    author_username: Optional[str] = None
    post_url: Optional[str] = None

class TaskPendingResponse(BaseModel):
    status: Literal["pending"]
    task_id: str

class TaskCompleteResponse(BaseModel):
    status: Literal["complete"]
    task_id: str
    data: dict

class KeywordRequest(BaseModel):
    action: Literal["add", "remove"]
    keywords: List[str] = Field(default_factory=list, min_items=1)

class KeywordAcceptedResponse(BaseModel):
    status: str
    message: str
    task_id: Optional[str] = None

