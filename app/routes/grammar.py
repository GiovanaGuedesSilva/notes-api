from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models import User
from app.schemas import GrammarCheckRequest, GrammarCheckResponse
from app.services.grammar_service import check_grammar

router = APIRouter(prefix="/grammar", tags=["grammar"])


@router.post("/check", response_model=GrammarCheckResponse)
def grammar_check(
    request: GrammarCheckRequest,
    current_user: User = Depends(get_current_user),
):
    return check_grammar(request.text)
