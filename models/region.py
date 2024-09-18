from sqlalchemy import Column, Integer, String, JSON
from models.base import Base

# Definir o modelo Region
class Region(Base):
    __tablename__ = 'data_entries'  # Nome da tabela

    id = Column(Integer, primary_key=True)
    name = Column(String)
    polygon = Column(JSON)  # Coluna para armazenar JSON

    def __repr__(self):
        return f"<Region(name={self.name}, data={self.data})>"
