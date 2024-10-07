from .interface_machine_learning import IMachineLearningModel
from ultralytics import SAM
import cv2
from typing import Optional

class SAM2(IMachineLearningModel):

    def __init__(self, model_path: str):
        super().__init__(model = SAM(model_path))

    def execute(self, input: cv2.typing.MatLike, device: Optional[str] = 'cpu'):
        print('running execute')    
        results = self.model(input, device=device)
        return results

    def process_frame(self, frame: cv2.typing.MatLike)->cv2.typing.MatLike:
        print('running execute')
        results = self.execute(input = frame)
        print(type(results))

        # for i, result in enumerate(results):
        #     if result.masks is not None:
        #         masks = result.masks.data

        #         boxes = result.boxes.xyxy
        #         boxes_np = boxes.cpu().numpy()
        #         masks_np = masks.cpu().numpy()

        #         for mask in masks_np:
        #             frame[mask > 0] = (0,255,0)
            
        # return frame
