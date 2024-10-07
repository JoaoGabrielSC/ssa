from machine_models.machine_learning_factory import MachineLearningModelFactory
import cv2

factory = MachineLearningModelFactory()
sam2_model = factory.create_model("sam2", r"D:\Users\n67121\OneDrive - ArcelorMittal\Documents\ssa\sam2_t.pt")
frame = cv2.imread('img/background_1.png')
result = sam2_model.process_frame(frame)
# cv2.imshow('frame', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
