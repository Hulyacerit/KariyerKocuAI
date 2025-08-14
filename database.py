import enum
import datetime
import os  # BU SATIRI EKLEDİK
from sqlalchemy import create_engine, Column, Integer, String, Enum as SQLAlchemyEnum, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# ================== DEĞİŞEN KISIM BAŞLANGICI ==================

# Projenin çalıştığı ana dizini buluyoruz (örn: /home/Hulya5/KariyerKocuAI)
basedir = os.path.abspath(os.path.dirname(__file__))

# Veritabanı URL'sini bu dinamik yola göre oluşturuyoruz
DATABASE_URL = "sqlite:///" + os.path.join(basedir, "kariyer_kocu.db")

# ================== DEĞİŞEN KISIM BİTİŞİ ==================

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- Dosyanın geri kalanı tamamen aynı, değişiklik yok ---
class EgitimDurumu(str, enum.Enum):
    ilkokul_ogrenci = "İlkokul Öğrencisi"
    ilkokul_mezun = "İlkokul Mezunu"
    ortaokul_ogrenci = "Ortaokul Öğrencisi"
    ortaokul_mezun = "Ortaokul Mezunu"
    lise_ogrenci = "Lise Öğrencisi"
    lise_mezun = "Lise Mezunu"
    universite_ogrenci = "Üniversite Öğrencisi"
    universite_mezun = "Üniversite Mezunu"

class Cinsiyet(str, enum.Enum):
    kadin = "Kadın"
    erkek = "Erkek"
    belirtmek_istemiyor = "Belirtmek İstemiyorum"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    ad_soyad = Column(String, nullable=False)
    yas = Column(Integer, nullable=False)
    cinsiyet = Column(SQLAlchemyEnum(Cinsiyet), nullable=False)
    egitim_durumu = Column(SQLAlchemyEnum(EgitimDurumu), nullable=False)
    is_deneyimi = Column(Integer, nullable=True)
    kariyer_hedefi = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    diary_entries = relationship("DiaryEntry", back_populates="owner")
    analysis_results = relationship("AnalysisResult", back_populates="owner")
    goals = relationship("Goal", back_populates="owner")
    cvs = relationship("Cv", back_populates="owner")

class DiaryEntry(Base):
    __tablename__ = "diary_entries"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="diary_entries")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, index=True)
    request_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    analysis_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="analysis_results")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="goals")

class Cv(Base):
    __tablename__ = "cvs"
    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=True)
    target_company = Column(String)
    target_position = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="cvs")

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
    print("Veritabanı ve tablolar başarıyla oluşturuldu/güncellendi.")

if __name__ == "__main__":
    create_db_and_tables()