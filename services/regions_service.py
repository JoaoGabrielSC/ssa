from models import Database, Region
from services.dto import RegionDTO

class RegionService:
    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, data: RegionDTO) -> None:
        entry = Region(
            name=data.name, 
            polygon=data.polygon 
        )
        session = self.database.new_session()
        session.add(entry)
        session.commit()
        session.close()
        return entry

    def update_region(self, id: int, data: RegionDTO) -> None:
        session = self.database.new_session()
        entry = session.query(Region).filter(Region.id == id).first()
        entry.name = data.name
        entry.polygon = data.polygon
        session.commit()
        session.close()
        print('Updated')
        return entry
    
    def delete_region(self, id: int) -> None:
        entry = self.database.session.query(Region).filter(Region.id == id).first()
        session = self.database.new_session()
        session.delete(entry)
        session.commit()
        session.close()
        return entry

    def list_regions(self):
        print('Listing regions')
        session = self.database.new_session()
        regions = session.query(Region).filter(Region.id==1).all()
        session.close()
        return regions
