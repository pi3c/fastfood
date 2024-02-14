from fastapi import APIRouter, Depends

from fastfood.schemas import MenuSummary
from fastfood.service.summary import SummaryService

router = APIRouter(
    prefix='/api/v1/summary',
    tags=['summary'],
)


@router.get('/', response_model=list[MenuSummary])
async def get_summary(
    sum: SummaryService = Depends(),
) -> list[MenuSummary]:
    return await sum.read_data()
