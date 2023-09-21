from pathlib import Path
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from task.config import SQLITE_DATABASE_NAME

Base = declarative_base()


class CurrencyConversion(Base):
    __tablename__ = "currency_conversion"

    id: int = Column(Integer, primary_key=True)
    currency: str = Column(String, nullable=False)
    rate: float = Column(Float, nullable=False)
    price_in_pln: float = Column(Float, nullable=False)
    date: datetime.date = Column(Date, nullable=False)


class SqliteDatabaseConnector:
    def __init__(self):
        self.database_path = Path(SQLITE_DATABASE_NAME)
        self.engine = create_engine(f"sqlite:///{self.database_path}")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_database(self):
        if not self.database_path.exists():
            self.database_path.touch()
            print(f"SQLite database file '{self.database_path}' created successfully.")
            Base.metadata.create_all(self.engine)
            print("Database tables initialized.")
        else:
            print(
                f"SQLite database file '{self.database_path}' already exists. Skipping creation."
            )

    def save(self, entity: dict) -> int:
        try:
            conversion = CurrencyConversion(
                currency=entity["currency"],
                rate=entity["rate"],
                price_in_pln=entity["price_in_pln"],
                date=datetime.strptime(entity["date"], "%Y-%m-%d").date(),
            )
            self.session.add(conversion)
            self.session.commit()
            return conversion.id
        except Exception as e:
            print(f"SQLite error: {e}")
            self.session.rollback()
            return -1

    def get_all(self) -> list[CurrencyConversion]:
        try:
            return self.session.query(CurrencyConversion).all()
        except Exception as e:
            print(f"SQLite error: {e}")
            return []

    def get_by_id(self, entity_id: str) -> CurrencyConversion:
        try:
            data = (
                self.session.query(CurrencyConversion).filter_by(id=entity_id).first()
            )
            return data
        except Exception as error:
            print(f"SQLite error: {error}")
            return CurrencyConversion()
