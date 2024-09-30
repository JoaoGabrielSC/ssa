import cv2
import numpy as np

class MouseHandler:
    def __init__(self):
        self.selected_point: any = None
        self.dragging: bool = False
        self.mouse_events = self.set_mouse_event_handlers()
        self.paused = False

    def set_mouse_event_handlers(self):
        """
        Define o mapeamento de eventos de mouse para os respectivos manipuladores.
        
        Returns:
            dict: Mapeamento de eventos de mouse para funções de manipulação de eventos.
        """
        return {
            cv2.EVENT_LBUTTONDOWN: self.handle_lbuttondown,
            cv2.EVENT_MOUSEMOVE: self.handle_mousemove,
            cv2.EVENT_LBUTTONUP: self.handle_lbuttonup
        }

    def handle_lbuttondown(self, x: int, y: int, polygon_with_offset: list) -> None:
        """
        Manipula o evento de clique com o botão esquerdo do mouse (EVENT_LBUTTONDOWN).
        Verifica se o clique está próximo a algum ponto do polígono e seleciona-o para arrastar.

        Args:
            x (int): Coordenada x do clique.
            y (int): Coordenada y do clique.
            polygon_with_offset (list): Lista de pontos do polígono com deslocamento.
        """
        for i, point in enumerate(polygon_with_offset):
            if np.linalg.norm(np.array(point) - np.array([x, y])) < 10:
                self.selected_point = i
                self.dragging = True
                self.paused = True
                break

    def handle_mousemove(self, x: int, y: int, polygon_with_offset: list) -> None:
        """
        Manipula o evento de movimento do mouse (EVENT_MOUSEMOVE).
        Atualiza a posição do ponto selecionado enquanto arrasta.

        Args:
            x (int): Coordenada x do mouse.
            y (int): Coordenada y do mouse.
            polygon_with_offset (list): Lista de pontos do polígono com deslocamento.
        """
        if self.dragging and self.selected_point is not None:
            polygon_with_offset[self.selected_point] = [x, y]

    def handle_lbuttonup(self, x: int, y: int, polygon_with_offset: list) -> None:
        """
        Manipula o evento de soltura do botão esquerdo do mouse (EVENT_LBUTTONUP).
        Termina o processo de arrastar e desmarca o ponto selecionado.
        """
        self.dragging = False
        self.selected_point = None
        self.paused = False

    def mouse_callback(self, event: int, x: int, y: int, flag: any, param: list) -> None:
        """
        Função callback para manipulação de vértices de um polígono com o mouse.
        
        Args:
            event (int): Tipo de evento do mouse.
            x (int): Coordenada x do mouse no momento do evento.
            y (int): Coordenada y do mouse no momento do evento.
            flag (any): Flags indicando o estado atual do mouse.
            param (list): Parâmetros adicionais, contendo o polígono.
        
        Returns:
            None
        """
        polygon_with_offset = param['polygon_with_offset']
        
        # Obter o mapeamento de eventos
        event_handlers = self.set_mouse_event_handlers()
        
        # Verifica se o evento possui um manipulador correspondente e o executa
        if event in event_handlers:
            event_handlers[event](x, y, polygon_with_offset)
