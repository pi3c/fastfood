from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: Optional[str]
    
    class Config:
        from_attributes = True


class Menu(MenuBase):
    id: UUID
    title: str
    description: Optional[str]
    # submenus: Optional[List[SubMenu]]

    class Config:
        from_attributes = True
