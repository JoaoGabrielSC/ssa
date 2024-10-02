import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from numpy.typing import ArrayLike
from spinnaker_api.Python3.AcquireAndDisplay import acquire_and_display_images, run_single_camera
import PySpin

# create a module that can be imported in other scripts
class CameraModule:
    def __init__(self) -> None:
        self.camera = run_single_camera()

    def get_frame(self) -> ArrayLike:
        # get the frame and return the image
        return acquire_and_display_images(self.camera)



