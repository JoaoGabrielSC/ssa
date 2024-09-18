from services.regions_service import RegionService
from services.dto import RegionDTO
from models import Database
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == '__main__':
    print("*** Writing to the database ***")
    database = Database(os.getenv('DATABASE_URL'))
    region_service = RegionService(database)

    data = RegionDTO(
        name='ladle',
        polygon=[[0, 0], [1, 1], [0, 1]]
    )
    region_service.create(data)
    print("*** Done Successfully ***")
