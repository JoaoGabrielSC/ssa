import os

from dotenv import load_dotenv

from models import Database
from services.dto import RegionDTO
from services.regions_service import RegionService

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
