from typing import Optional
from sqlalchemy.orm import Session
import models
from database import SessionLocal


def load_initial_seed_data(db: Session) -> None:
    """SigunguCode 및 Place 테이블에 초기 시드 데이터를 적재합니다."""
    # SigunguCode 시드 데이터 적재 (서울시 전체 25개 구)
    if db.query(models.SigunguCode).count() == 0:
        sigungu_seeds = [
            models.SigunguCode(sigungu_code="110", sido_name="서울특별시", sigungu_name="종로구"),
            models.SigunguCode(sigungu_code="140", sido_name="서울특별시", sigungu_name="중구"),
            models.SigunguCode(sigungu_code="170", sido_name="서울특별시", sigungu_name="용산구"),
            models.SigunguCode(sigungu_code="200", sido_name="서울특별시", sigungu_name="성동구"),
            models.SigunguCode(sigungu_code="215", sido_name="서울특별시", sigungu_name="광진구"),
            models.SigunguCode(sigungu_code="230", sido_name="서울특별시", sigungu_name="동대문구"),
            models.SigunguCode(sigungu_code="260", sido_name="서울특별시", sigungu_name="중랑구"),
            models.SigunguCode(sigungu_code="290", sido_name="서울특별시", sigungu_name="성북구"),
            models.SigunguCode(sigungu_code="305", sido_name="서울특별시", sigungu_name="강북구"),
            models.SigunguCode(sigungu_code="320", sido_name="서울특별시", sigungu_name="도봉구"),
            models.SigunguCode(sigungu_code="350", sido_name="서울특별시", sigungu_name="노원구"),
            models.SigunguCode(sigungu_code="380", sido_name="서울특별시", sigungu_name="은평구"),
            models.SigunguCode(sigungu_code="410", sido_name="서울특별시", sigungu_name="서대문구"),
            models.SigunguCode(sigungu_code="440", sido_name="서울특별시", sigungu_name="마포구"),
            models.SigunguCode(sigungu_code="470", sido_name="서울특별시", sigungu_name="양천구"),
            models.SigunguCode(sigungu_code="500", sido_name="서울특별시", sigungu_name="강서구"),
            models.SigunguCode(sigungu_code="530", sido_name="서울특별시", sigungu_name="구로구"),
            models.SigunguCode(sigungu_code="545", sido_name="서울특별시", sigungu_name="금천구"),
            models.SigunguCode(sigungu_code="560", sido_name="서울특별시", sigungu_name="영등포구"),
            models.SigunguCode(sigungu_code="590", sido_name="서울특별시", sigungu_name="동작구"),
            models.SigunguCode(sigungu_code="620", sido_name="서울특별시", sigungu_name="관악구"),
            models.SigunguCode(sigungu_code="650", sido_name="서울특별시", sigungu_name="서초구"),
            models.SigunguCode(sigungu_code="680", sido_name="서울특별시", sigungu_name="강남구"),
            models.SigunguCode(sigungu_code="710", sido_name="서울특별시", sigungu_name="송파구"),
            models.SigunguCode(sigungu_code="740", sido_name="서울특별시", sigungu_name="강동구"),
        ]
        db.add_all(sigungu_seeds)
        db.commit()

    # Place 시드 데이터 적재 (서울시 전체 25개 구 통일)
    if db.query(models.Place).count() == 0:
        place_seeds = [
            models.Place(id=1, name="종로구", lat=37.5730, lng=126.9794, description="서울특별시 종로구 지역 정보 공유", sigungu_code="110"),
            models.Place(id=2, name="중구", lat=37.5637, lng=126.9975, description="서울특별시 중구 지역 정보 공유", sigungu_code="140"),
            models.Place(id=3, name="용산구", lat=37.5326, lng=126.9900, description="서울특별시 용산구 지역 정보 공유", sigungu_code="170"),
            models.Place(id=4, name="성동구", lat=37.5633, lng=127.0371, description="서울특별시 성동구 지역 정보 공유", sigungu_code="200"),
            models.Place(id=5, name="광진구", lat=37.5385, lng=127.0823, description="서울특별시 광진구 지역 정보 공유", sigungu_code="215"),
            models.Place(id=6, name="동대문구", lat=37.5744, lng=127.0396, description="서울특별시 동대문구 지역 정보 공유", sigungu_code="230"),
            models.Place(id=7, name="중랑구", lat=37.6063, lng=127.0928, description="서울특별시 중랑구 지역 정보 공유", sigungu_code="260"),
            models.Place(id=8, name="성북구", lat=37.5894, lng=127.0167, description="서울특별시 성북구 지역 정보 공유", sigungu_code="290"),
            models.Place(id=9, name="강북구", lat=37.6398, lng=127.0255, description="서울특별시 강북구 지역 정보 공유", sigungu_code="305"),
            models.Place(id=10, name="도봉구", lat=37.6688, lng=127.0471, description="서울특별시 도봉구 지역 정보 공유", sigungu_code="320"),
            models.Place(id=11, name="노원구", lat=37.6542, lng=127.0568, description="서울특별시 노원구 지역 정보 공유", sigungu_code="350"),
            models.Place(id=12, name="은평구", lat=37.6027, lng=126.9291, description="서울특별시 은평구 지역 정보 공유", sigungu_code="380"),
            models.Place(id=13, name="서대문구", lat=37.5791, lng=126.9368, description="서울특별시 서대문구 지역 정보 공유", sigungu_code="410"),
            models.Place(id=14, name="마포구", lat=37.5663, lng=126.9016, description="서울특별시 마포구 지역 정보 공유", sigungu_code="440"),
            models.Place(id=15, name="양천구", lat=37.5170, lng=126.8665, description="서울특별시 양천구 지역 정보 공유", sigungu_code="470"),
            models.Place(id=16, name="강서구", lat=37.5509, lng=126.8495, description="서울특별시 강서구 지역 정보 공유", sigungu_code="500"),
            models.Place(id=17, name="구로구", lat=37.4954, lng=126.8874, description="서울특별시 구로구 지역 정보 공유", sigungu_code="530"),
            models.Place(id=18, name="금천구", lat=37.4569, lng=126.8955, description="서울특별시 금천구 지역 정보 공유", sigungu_code="545"),
            models.Place(id=19, name="영등포구", lat=37.5264, lng=126.8963, description="서울특별시 영등포구 지역 정보 공유", sigungu_code="560"),
            models.Place(id=20, name="동작구", lat=37.5124, lng=126.9393, description="서울특별시 동작구 지역 정보 공유", sigungu_code="590"),
            models.Place(id=21, name="관악구", lat=37.4782, lng=126.9515, description="서울특별시 관악구 지역 정보 공유", sigungu_code="620"),
            models.Place(id=22, name="서초구", lat=37.4836, lng=127.0327, description="서울특별시 서초구 지역 정보 공유", sigungu_code="650"),
            models.Place(id=23, name="강남구", lat=37.5172, lng=127.0473, description="서울특별시 강남구 지역 정보 공유", sigungu_code="680"),
            models.Place(id=24, name="송파구", lat=37.5145, lng=127.1059, description="서울특별시 송파구 지역 정보 공유", sigungu_code="710"),
            models.Place(id=25, name="강동구", lat=37.5301, lng=127.1238, description="서울특별시 강동구 지역 정보 공유", sigungu_code="740"),
        ]
        db.add_all(place_seeds)
        db.commit()


def get_local_context_for_ai(place_id: Optional[int] = None, db: Optional[Session] = None) -> str:
    """AI 챗봇 프롬프트에 제공할 장소 및 랭킹 컨텍스트 문자열을 반환합니다."""
    close_db = False
    if db is None:
        from database import engine, Base
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        close_db = True
        try:
            if db.query(models.SigunguCode).count() == 0 or db.query(models.Place).count() == 0:
                load_initial_seed_data(db)
        except Exception:
            pass
    try:
        if place_id is not None:
            place = db.query(models.Place).filter(models.Place.id == place_id).first()
            if not place:
                return "존재하지 않는 장소입니다."
            
            post_cnt = db.query(models.Post).filter(models.Post.place_id == place_id).count()
            posts = db.query(models.Post).filter(models.Post.place_id == place_id).order_by(models.Post.id.desc()).limit(10).all()
            post_texts = "\n".join([f"- {p.title}: {p.content[:50]}" for p in posts])
            
            return (
                f"[장소 정보]\n"
                f"이름: {place.name}\n"
                f"설명: {place.description or '설명 없음'}\n"
                f"게시글 수: {post_cnt}건\n"
                f"최신 게시글 요약/동향:\n{post_texts or '아직 등록된 게시글이 없습니다.'}"
            )
        else:
            places = db.query(models.Place).all()
            places_with_count = []
            for pl in places:
                cnt = db.query(models.Post).filter(models.Post.place_id == pl.id).count()
                places_with_count.append((pl, cnt))
            places_with_count.sort(key=lambda x: x[1], reverse=True)
            
            lines = []
            for pl, cnt in places_with_count[:10]:
                lines.append(f"- {pl.name} (게시글 {cnt}건): {pl.description or ''}")
            return "서울 전역 핫플레이스 실시간 랭킹 및 현황:\n" + "\n".join(lines)
    finally:
        if close_db:
            db.close()
