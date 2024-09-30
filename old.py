from services.regions_service import RegionService
from numpy.typing import ArrayLike
from dotenv import load_dotenv
from models import Database
import numpy as np
import cv2
import os

load_dotenv()

class VideoPolygonDrawer:
    def __init__(self, region_service: RegionService, index_target: float)->None:
        self.region_service = region_service
        self.index_target = index_target

    def apply_offset(self, polygon: list, x_offset:int, y_offset:int) -> list:
        """
        Função auxiliar para desenhar a região na imagem do vídeo
        Args:

        """
        return [[x + x_offset, y + y_offset] for x, y in polygon]

    def draw_polygon_on_frame(self, frame: ArrayLike, polygon)->ArrayLike:
        pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
        return frame

    def calculate_inverse_sum(self, mask, masked_frame):
        pixels_inside = masked_frame[mask == 255]
        pixels_inside = np.array(pixels_inside, dtype=np.uint8)
        pixels_inside_handled = np.where(pixels_inside == 0, 1, pixels_inside)
        inverse_intensities = 1 / pixels_inside_handled if len(pixels_inside_handled) > 0 else 0

        quantity_pixels = len(pixels_inside)
        sum_inverse_intensities = np.sum(inverse_intensities)
        index_initial = sum_inverse_intensities / quantity_pixels
        return index_initial
    
    def debbuger(frame: ArrayLike, mask: ArrayLike) -> None:
        mask = cv2.addWeighted(mask, 0.5, frame, 0.5, 0)
        mask = np.uint8(mask)
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        print(f"Frame dtype: {frame.dtype}, shape: {frame.shape}")
        print(f"Mask dtype: {mask.dtype}, shape: {mask.shape}")
        cv2.imshow('Mask', mask)
        cv2.imshow('Masked Frame', masked_frame)

    def apply_polygon_mask(self, frame: np.array, polygon: list, debug: bool = False)->tuple:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        pts = np.array(polygon, np.int32)
        mask = cv2.fillPoly(mask, [pts], 255)

        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    
        return mask, masked_frame

    def process_video(self, video_path, x_offset=0, y_offset=0)->None:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Erro: Não foi possível abrir o vídeo.")
            return
        
        regions = self.region_service.list_regions()
        if len(regions) == 0:
            print("Erro: Nenhuma região encontrada.")
            return
        
        region = regions[0]  
        polygon = region.polygon
        
        polygon_with_offset = self.apply_offset(polygon, x_offset, y_offset)
        count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.resize(frame, (1080, 720))
            if not ret:
                break
            count += 1

            initial_var = self.calculate_inverse_sum(frame, polygon_with_offset)

            if count % 10 == 0:
                print(f'Frame: {count}')
                print('=== Resultados ===')
                print(f'Initial index: {initial_var}')

            frame = self.draw_polygon_on_frame(frame, polygon_with_offset)
            
            cv2.imshow('Vídeo com Polígono', frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# Uso
database = Database(os.getenv('DATABASE_URL'))
region_service = RegionService(database)
video_drawer = VideoPolygonDrawer(region_service)

video_drawer.process_video('videos/video_2.avi', x_offset=-10, y_offset=25)
