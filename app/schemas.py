from pydantic import BaseModel
from typing import List, Dict, Any

class UserPayload(BaseModel):
    users: List[Dict[str, Any]]
