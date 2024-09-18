from services.regions_service import RegionService
from models import Database
import os
import numpy as np
import cv2

class FrameProcess:
    def __init__(self, database: Database)-> None:
        self.database = Database(os.getenv('DATABASE_URL'))
        self.region_service = RegionService(database)

    def get_frame(self, frame: np.ndarray) -> np.ndarray:
        frame = self.cam.get_frame()
        if frame is None or frame.size == 0:
            return None
        return frame

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        
