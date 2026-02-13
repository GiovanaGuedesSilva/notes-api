from fastapi import APIRouter

from app.schemas import GrammarCheckRequest, GrammarCheckResponse
from app.services.grammar_service import check_grammar

router = APIRouter(prefix="/grammar", tags=["grammar"])


@router.post("/check", response_model=GrammarCheckResponse)
def grammar_check(request: GrammarCheckRequest):
    return check_grammar(request.text)
