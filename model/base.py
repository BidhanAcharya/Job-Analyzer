from pydantic import BaseModel, Field
from typing import List 
class KeywordsModel(BaseModel):
    keywords: List[str] =Field(description="list of keywords extracted from resume")