import logging

from pix_app.db.base import SessionLocal
from pix_app.db.models.pix_model import PixModel

logger = logging.getLogger(__name__)


def save_pix(pix_model: PixModel):
    db = SessionLocal()
    try:
        db.add(pix_model)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao salvar PIX: {e}")
        raise
    finally:
        db.close()


def get_pix_by_hash(hash_id: str):
    db = SessionLocal()
    try:
        return db.query(PixModel).filter(PixModel.hash_id == hash_id).first()
    finally:
        db.close()


def increment_pix_clicks(pix_obj: PixModel):
    db = SessionLocal()
    try:
        obj = db.query(PixModel).filter(PixModel.id == pix_obj.id).first()
        if obj:
            obj.clicks += 1
            db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao incrementar cliques: {e}")
    finally:
        db.close()
