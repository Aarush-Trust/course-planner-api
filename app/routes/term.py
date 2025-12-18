from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date
from app.models import Term

router = APIRouter(
    prefix="/terms",
    tags=["Terms"],
)

#Hypothetical Data
fake_terms: List[Term] = [
    Term(
        id = 1,
        name = "Winter 2026",
        start_date = date(2026, 1, 6),
        end_date = date(2026, 4, 20)
    ),

    Term(
        id = 2,
        name = "Summer 2026",
        start_date = date(2026, 5, 6),
        end_date = date(2026, 8, 20)
    )
]

#Return all the terms
@router.get("/", response_model = List[Term])
def list_terms():
    return fake_terms

#Return the requested Term
@router.get("/{term_id}", response_model = Term)
def get_term(term_id: int):
    for term in fake_terms:
        if term.id == term_id:
            return term
    raise HTTPException(status_code = 404, detail = {"code": "MISSING TERM",
                                                    "message": "Term not found"})