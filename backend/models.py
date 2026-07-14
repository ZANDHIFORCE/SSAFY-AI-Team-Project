from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base


class SigunguCode(Base):
    __tablename__ = "sigungu_code"

    sigungu_code = Column(String, primary_key=True, index=True)
    sido_name = Column(String, nullable=False)
    sigungu_name = Column(String, nullable=False)

    places = relationship("Place", back_populates="sigungu")


class Place(Base):
    __tablename__ = "place"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    sigungu_code = Column(String, ForeignKey("sigungu_code.sigungu_code"), nullable=False)

    sigungu = relationship("SigunguCode", back_populates="places")
    posts = relationship("Post", back_populates="place")


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("place.id"), nullable=False)
    nickname = Column(String, nullable=False, default="익명")
    password = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    place = relationship("Place", back_populates="posts")
