import time
import cv2
import os

class SaveVideoManager:
    def __init__(self):
        self.video_folder =  'videos'
        self.video_output_name = ""
        self.frame_width = 1080
        self.frame_height = 720
        self.save_video = False
        self.video_output = None

        self._set_save_fps()

    def _set_save_fps(self):
        self.fps = 15

    def set_video_output_path(self):
        formated_time = time.strftime("%Y_%m_%d_%Hh%Mmin%Ss")
        file_name = "video_salvo_" + formated_time + ".avi"
        self.video_output_name = os.path.join( self.video_folder, file_name)

    def setup_saving_video(self):
        self.save_video = True
        self.set_video_output_path()
        self.check_video_folder()


        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_output = cv2.VideoWriter(
            self.video_output_name, fourcc, self.fps, (self.frame_width, self.frame_height))

    def pipeline_save_video(self, frame):
        if self.save_video:
            try:
                self.video_output.write(frame)
            except Exception as e:
                print("Interno/saveVideoManager.py/pipeline_save_video(): erro ao salvar video: %s", str(e))

    def end_saving_video(self):
        print("Interno/saveVideoManager.py/end_saving_video() Finalizando video")
        self.video_output.release()
        self.save_video = False

    def check_video_folder(self):
        print(f"Interno/saveVideoManager.py/check_video_folder() Folder: {self.video_folder}")
        try:
            if not os.path.exists(self.video_folder):
                os.makedirs(self.video_folder)
        except Exception as e:
            print(f"Interno/saveVideoManager.py/check_video_folder(): Erro ao criar pasta: {str(e)}")

save_video_manager = SaveVideoManager()
