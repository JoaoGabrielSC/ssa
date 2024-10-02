import cv2
import numpy as np
import os
import time
from numpy.typing import ArrayLike
from dotenv import load_dotenv
from models import Database
from services.regions_service import RegionService
from utils.frame_process import FrameProcess
import csv
from typing import Tuple

load_dotenv()

if __name__ == '__main__':
    database = Database(os.getenv('DATABASE_URL'))
    region_service = RegionService(database)
    video_drawer = FrameProcess(region_service)

    video_drawer.process_video('videos/video_2.avi', x_offset=0, y_offset=0)
