from datetime import datetime, timezone
from enum import Enum
from typing import List
from fastapi import APIRouter
from ...config import get_app_config

tags:List[str | Enum]=["测试"]
router = APIRouter(
  tags=tags,
  prefix=f"{get_app_config().api_prefix}/test",
  responses={404: {"description": "Not found"}}
)

@router.get("/")
async def say_hi():
  return {
    "text": "hi",
    'time': datetime.now(timezone.utc).isoformat()
  }

