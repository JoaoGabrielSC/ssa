import csv
import os
import time
from typing import Tuple, Optional

import cv2
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from dotenv import load_dotenv
from numpy.typing import ArrayLike
from sklearn.cluster import KMeans

from models import Database
from services.regions_service import RegionService
from utils.mouse_handler import MouseHandler

load_dotenv()

class FrameProcess:
    def __init__(self, region_service: RegionService) -> None:
        self.region_service = region_service
        self.mouse_handler = MouseHandler()
        self.paused = self.mouse_handler.paused


    def apply_offset(self, polygon: list, x_offset: int, y_offset: int) -> list:
        """
        Aplica um offset à região do polígono
        Args:
            polygon: list - lista com as coordendas da região
            x_offset: int - Offset em x
            y_offset: int - Offset em y
        Return:
            list
        """
        return [[x + x_offset, y + y_offset] for x, y in polygon]

    def draw_polygon_on_frame(self, frame: ArrayLike, polygon: list) -> ArrayLike:
        """
        Desenha a região delimitadora no frame
        Args:
            frame: ArrayLike - Frame processado pela opencv
            polygon: list - Lista contendo as coordenadas da região
        Return: 
            frame: ArrayLike - Frame processado
        """
        pts = np.array(polygon, np.int32).reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

        for point in polygon:
            cv2.circle(frame, (int(point[0]), int(point[1])), 5, (0, 0, 255), -1)

        return frame

    def calculate_index(self, mask: ArrayLike, masked_frame: ArrayLike, i: int) -> float:
        """
        Calcula o somatório do inverso da intensidade dos pixels dentro da ROI
        Args:
            mask: ArrayLike - Frame contendo apenas o pixels que delimitado a região preenchida
            masked_frame: ArrayLike - Frame pós processamento
        Returns:
            index: float - O resultado do cálculo
        Variaveis auxiliares:
            pixels_inside: ArrayLike - Array contendo apenas o pixels dentro da região com tipo unsingned 8bits
            non_zero_pixels: ArrayLike - Array modificado com pixels de intensidade 0 para 1
            inverse_intensities: ArrayLike - Array com o inverso de cada valor de non_zero_pixels
            quantity_pixels: int - inteiro com o tamanho do array pixels_inside
            sum_inverse_intensities: float - Soma do inverso das intensidades
            index: float - Soma do inverso das intensidades dividido pela quantidade de pixels
        """
        pixels_inside = masked_frame[mask == 255]
        pixels_inside = np.array(pixels_inside, dtype=np.uint8)
        non_zero_pixels = np.where(pixels_inside == 0, 1, pixels_inside)
        inverse_intensities = 1 / non_zero_pixels if len(non_zero_pixels) > 0 else 0

        # print(f'Intensidades: {pixels_inside}')
        # print(f'Inverso da intensidade: {inverse_intensities}')
        # print(f'Media do inverso da intensidade: {np.mean(inverse_intensities)}')
        # print(f'Minimo do inverso da intensidade: {np.min(inverse_intensities)}')
        # print(f'Maximo do inverso da intensidade: {np.max(inverse_intensities)}')
        quantity_pixels = len(pixels_inside)
        # print(f'Quantidade de pixels: {quantity_pixels}')
        sum_inverse_intensities = np.sum(inverse_intensities)
        # print(f'Soma do inverso da intensidade: {sum_inverse_intensities}')
        index = sum_inverse_intensities / quantity_pixels

        file = f'logs/log_intensity_{i}.csv'
        if i == 1:
            self.save_log('w', file, pixels_inside)
        if i%300 == 0:
            self.save_log('w', file, pixels_inside)

        return index
    
    @staticmethod
    def save_log(mode: str, filename: str, data: ArrayLike, header: Optional[str] = "Intensities Matrix") -> None:
        with open (filename, mode=mode, newline='') as file:
            writer_ = csv.writer(file)
            writer_.writerow(['Intensities Matrix'])
            for value in data:
                writer_.writerow([value])

    @staticmethod
    def plot_pixel_intensity_heatmap(pixels_inside: ArrayLike, frame_number: int) -> None:
        """
        Plota um heatmap das intensidades dos pixels_inside
        Args:
            pixels_inside: ArrayLike - Intensidades dos pixels dentro da região
            frame_number: int - Número do frame atual (para identificar no gráfico)
        Return: 
            None
        """
        # Normaliza as intensidades para o intervalo [0, 1]
        normalized_intensities = (pixels_inside - np.min(pixels_inside)) / (np.max(pixels_inside) - np.min(pixels_inside))

        # Cria uma matriz 2D para o heatmap (você pode ajustar a forma dependendo do tamanho dos dados)
        heatmap_data = normalized_intensities.reshape(-1, 1)  # Ajusta para ser uma matriz 2D

        plt.figure(figsize=(6, 4))
        cbar_sticks = np.arange(0, 1.1, 0.05)
        sns.heatmap(
            heatmap_data, 
            cmap='gray', 
            cbar=True, 
            vmin=0, 
            vmax=1,
            cbar_kws={'ticks': cbar_sticks}
            )
        plt.title(f'Heatmap de Intensidade de Pixels - Frame {frame_number}')
        plt.xlabel('Pixels')
        plt.ylabel('Intensidade Normalizada')
        plt.show()

    def extract_pixels_inside(self, frame: ArrayLike, polygon: list, debug: bool = False) -> Tuple[ArrayLike, ArrayLike]:
        """
        Performa pixel a pixel o operador AND comparando o frame original com a região de interesse
        Args:
            frame: ArrayLike - Frame Carregado pela opencv
            polygon: list - Lista contendo as coordenadas da região de interesse
            debug: bool - Booleano para mostrar a mask e debugar se for de interesse
        Returns:
            mask masked_frame: Tuple - Uma tupla contendo a mascara e o frame "mascarado"

        Vars:
            pts = array com formato int32 contendo as coordenadas da ROI
            mask = array com o mesmo tamanho da imagem preenchido pixels brancos apenas dentro da região delimitadora
            masked_frame = frame com apenas os pixels dentro da região mantidos
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        pts = np.array(polygon, np.int32)
        mask = cv2.fillPoly(mask, [pts], 255)

        if debug:
            mask = cv2.addWeighted(mask, 0.5, frame, 0.5, 0)
            mask = np.uint8(mask)
            print(f"Frame dtype: {frame.dtype}, shape: {frame.shape}")
            print(f"Mask dtype: {mask.dtype}, shape: {mask.shape}")
            cv2.imshow('Mask', mask)
            cv2.imshow('Masked Frame', masked_frame)

        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        # cv2.imshow('masked', masked_frame)
        return mask, masked_frame

       
    def process_video(self, video_path: str, x_offset: int, y_offset: int, log_folder: str ='logs') -> None:
        """
        Processa o vídeo e performa o cálculo do index e plota a região no frame
        Args:
            video_path: str - Caminho para o vídeo
            x_offset: int - Offset em x
            y_offset: int - Offset em y
            log_folder: str - Caminho para a pasta de logs
        Returns:
            None
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Erro: Não foi possível abrir o vídeo.")
            return
        
        os.makedirs(log_folder, exist_ok=True)
        log_filename = os.path.join(log_folder, f'log_{time.strftime("%Y%m%d-%H%M%S")}.csv')

        regions = self.region_service.list_regions()
        if len(regions) == 0:
            print("Erro: Nenhuma região encontrada.")
            return
        
        region = regions[0]  
        polygon = region.polygon
        # polygon = [[1,1],[2,2]...[n,n]]
        polygon_with_offset = self.apply_offset(polygon, x_offset, y_offset)

        # Definir o callback do mouse para manipular o polígono
        cv2.namedWindow('Vídeo com Polígono')
        cv2.setMouseCallback(
            'Vídeo com Polígono', 
            self.mouse_handler.mouse_callback, 
            param={'polygon_with_offset': polygon_with_offset}
        )

        count = 0
        fps = cap.get(cv2.CAP_PROP_FPS)

        with open(log_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Frame', 'Time(s)', 'Index'])

            while cap.isOpened():
                if not self.paused:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame = cv2.resize(frame, (1080, 720))
                    count += 1

                    # if count % 10 == 0:
                    # print(f'='*30)
                    mask, masked_frame = self.extract_pixels_inside(frame, polygon_with_offset)
                    index = self.calculate_index(mask, masked_frame, count)
                    time_seconds = count / fps
                    writer.writerow([count, time_seconds, index])
                    print(f'Frame: {count}, Tempo: {time_seconds}s, Index: {index}')

                    # if count % 20 == 0:
                    #     self.plot_pixel_intensity_heatmap (masked_frame[mask == 255], count)
                    
                    frame = self.draw_polygon_on_frame(frame, polygon_with_offset)

                # cv2.imshow('Vídeo com Polígono', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
