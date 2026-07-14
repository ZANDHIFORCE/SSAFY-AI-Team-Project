from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from database import get_db
import models
from utils.data_loader import get_local_context_for_ai


class PlaceResponse(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    description: Optional[str] = None
    sigungu_code: str
    post_count: int

    model_config = ConfigDict(from_attributes=True)


router = APIRouter(
    prefix="/api/places",
    tags=["places"]
)


@router.get("", response_model=List[PlaceResponse])
def list_places(db: Session = Depends(get_db)):
    """[BE-01] 장소 목록 조회 (post_count 기준 내림차순 정렬)"""
    places = db.query(models.Place).all()
    results = []
    for place in places:
        post_count = db.query(models.Post).filter(models.Post.place_id == place.id).count()
        results.append(
            PlaceResponse(
                id=place.id,
                name=place.name,
                lat=place.lat,
                lng=place.lng,
                description=place.description,
                sigungu_code=place.sigungu_code,
                post_count=post_count
            )
        )
    # post_count 기준 내림차순 정렬
    results.sort(key=lambda x: x.post_count, reverse=True)
    return results


@router.get("/{place_id}", response_model=PlaceResponse)
def get_place(place_id: int, db: Session = Depends(get_db)):
    """[BE-02] 장소 단건 조회 (post_count 포함)"""
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 장소입니다.")
    
    post_count = db.query(models.Post).filter(models.Post.place_id == place.id).count()
    return PlaceResponse(
        id=place.id,
        name=place.name,
        lat=place.lat,
        lng=place.lng,
        description=place.description,
        sigungu_code=place.sigungu_code,
        post_count=post_count
    )
