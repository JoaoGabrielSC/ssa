from vidgear.gears import CamGear
import time
from datetime import datetime
import cv2

class Reconnecting_CamGear:

    def __init__(self, cam_address, reset_attempts=50, reset_delay=5):
        self.reset_attempts_max = reset_attempts
        self.cam_address = cam_address
        self.reset_attempts = reset_attempts
        self.reset_delay = reset_delay
        self.source = None
        self.running = True

    def start(self):
        self.running = True
        self.reset_attempts = self.reset_attempts_max
        self.source = CamGear(source=self.cam_address).start()

    def read(self):
        if self.source is None:
            print("Source is None")
            return None
        if self.running and self.reset_attempts > 0:
            frame = self.source.read()
            if frame is None:
                self.source.stop()
                self.reset_attempts -= 1
                print(
                    "Re-connection Attempt-{} occured at time:{}".format(
                        str(self.reset_attempts),
                        datetime.datetime.now().strftime("%m-%d-%Y %I:%M:%S%p"),
                    )
                )
                time.sleep(self.reset_delay)
                self.source = CamGear(source=self.cam_address).start()
                # return previous frame
                return self.frame
            else:
                self.frame = frame
                return frame
        else:
            print("No running")
            print(self.reset_attempts)
            print(self.running)
            return None

    def stop(self):
        self.running = False
        self.reset_attempts = 0
        self.frame = None
        if not self.source is None:
            self.source.stop()

    def get_frame(self):
        self.start()
        frame = self.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.stop()
        return frame
