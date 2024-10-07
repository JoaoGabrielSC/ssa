from abc import ABC, abstractmethod

class IMachineLearningModel(ABC):

    def __init__(self, model: any):
        self.model = model

    @abstractmethod
    def execute(self, input: any):
        pass
