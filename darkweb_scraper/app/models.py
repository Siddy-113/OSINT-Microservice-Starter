from typing import List, Literal, Optional
from pydantic import BaseModel, Field

IdentifierType = Literal["email", "phone_number", "username"]

class SearchRequest(BaseModel):
    identifier_type: IdentifierType
    identifier_value: str = Field(..., min_length=1, max_length=512)

class SearchAcceptedResponse(BaseModel):
    message: str
    task_id: str

class KeywordRequest(BaseModel):
    action: Literal["add", "remove"]
    keywords: List[str]

class KeywordAcceptedResponse(BaseModel):
    status: str
    message: str
    task_id: Optional[str] = None

class ResultItem(BaseModel):
    source_url: str
    source_type: str
    capture_timestamp: str
    match_type: str
    matched_keyword: Optional[str]
    content_snippet: str
    author_username: Optional[str]
    post_url: Optional[str]
