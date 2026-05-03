from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BookResponse
from app.crud import get_books
from datetime import datetime

router = APIRouter(prefix="/analytics", tags=["analytics"])

class RecommendationRequest(BaseModel):
    min_year: int = 1900
    max_rating: float = 5.0
    limit: int = 5

@router.post("/recommend", response_model=list[BookResponse])
def recommend_books(req: RecommendationRequest, db: Session = Depends(get_db)):
    books = get_books(db, skip=0, limit=100)
    if not books:
        raise HTTPException(status_code=404, detail="Нет книг для рекомендации")

    current_year = datetime.now().year
    scored = []
    for b in books:
        if b.year < req.min_year:
            continue
        # Алгоритм взвешенного скоринга
        recency_score = 1.0 / (current_year - b.year + 1)
        # Упрощённая эвристика: новые книги получают бонус, но не доминируют
        final_score = (0.4 * recency_score) + (0.3 * (req.max_rating / 5.0)) + 0.3
        scored.append((b, final_score))

    # Сортировка по убыванию score
    scored.sort(key=lambda x: x[1], reverse=True)
    return [b for b, _ in scored[:req.limit]]