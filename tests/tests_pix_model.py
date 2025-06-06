import unittest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models.pix_model import PixModel
from app.db.models.pix_model import mapper_registry


class TestPixModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        # Cria as tabelas a partir do metadata do registry
        mapper_registry.metadata.create_all(self.engine)

        session = sessionmaker(bind=self.engine)
        self.db_session = session()

    def tearDown(self):
        self.db_session.close()
        self.engine.dispose()

    def test_create_pix_model(self):
        pix = PixModel(
            full_name="Cleiton Leonel",
            pix_key="cleiton.leonel@gmail.com",
            city="Cariacica",
            zip_code="29148613",
            amount=Decimal("49.99"),
            description="Teste de pagamento",
            identification="txid123456",
            location="https://pix.example.com",
            br_code="000201...",
            base64_qr="data:image/png;base64,...",
            hash_id="abcdef123456"
        )

        self.db_session.add(pix)
        self.db_session.commit()

        retrieved = self.db_session.query(PixModel).filter_by(hash_id="abcdef123456").first()

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.full_name, "Cleiton Leonel")
        self.assertEqual(retrieved.pix_key, "cleiton.leonel@gmail.com")
        self.assertEqual(retrieved.city, "Cariacica")
        self.assertEqual(retrieved.zip_code, "29148613")
        self.assertEqual(retrieved.amount, Decimal("49.99"))
        self.assertEqual(retrieved.description, "Teste de pagamento")
        self.assertEqual(retrieved.identification, "txid123456")
        self.assertEqual(retrieved.location, "https://pix.example.com")
        self.assertEqual(retrieved.br_code, "000201...")
        self.assertTrue(retrieved.base64_qr.startswith("data:image/png;base64"))
        self.assertEqual(retrieved.hash_id, "abcdef123456")
        self.assertIsNotNone(retrieved.created_at)
        self.assertIsNotNone(retrieved.updated_at)
        self.assertEqual(retrieved.clicks, 0)


if __name__ == "__main__":
    unittest.main()
