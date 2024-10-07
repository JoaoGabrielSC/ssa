import csv
import os
import time
from typing import Tuple

import cv2
import numpy as np
from dotenv import load_dotenv
from numpy.typing import ArrayLike

from models import Database
from services.regions_service import RegionService
from utils.frame_process import FrameProcess

load_dotenv()

if __name__ == '__main__':
    database = Database(os.getenv('DATABASE_URL'))
    region_service = RegionService(database)
    video_drawer = FrameProcess(region_service)

    video_drawer.process_video('videos/video_2.avi', x_offset=0, y_offset=0)
