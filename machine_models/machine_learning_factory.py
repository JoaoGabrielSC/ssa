from typing import Optional, Type

from strategies import SAM2, IMachineLearningModel


class MachineLearningModelFactory:
    """ Factory class to create machine learning models 
    Attributes:
        _models (dict): A dictionary containing the available models in the factory.
    Args:
        model_name (str): The name of the model to instantiate.
        model_path (Optional[str]): Optional path to the model file (for models requiring a file path).
    Return: 
        IMachineLearningModel: An instance of the requested machine learning model.
    Raises:
        ValueError: If the model name is not found in the factory.
        TypeError: If the model requires a model_path but it is not provided.
    """
    _models = {
        'sam2': SAM2
    }

    @classmethod
    def register_model(cls, model_name: str, model_class: Type[IMachineLearningModel]):
        """ Registers a new model in the factory """
        if not issubclass(model_class, IMachineLearningModel):
            raise TypeError(f"{model_class.__name__} must inherit from IMachineLearningModel")
        cls._models[model_name] = model_class

    @classmethod
    def create_model(cls, model_name: str, model_path: Optional[str] = None) -> IMachineLearningModel:
        """ Factory method to create a machine learning model

        Args:
            model_name (str): The name of the model to instantiate. ("sam2")
            model_path (Optional[str]): Optional path to the model file (for models requiring a file path).
        
        Returns:
            IMachineLearningModel: An instance of the requested machine learning model.
        
        Raises:
            ValueError: If the model name is not found in the factory.
            TypeError: If the model requires a model_path but it is not provided.
        Example:
            >> factory = MachineLearningModelFactory()
            >> sam2_model = factory.create_model("sam2", "sam2_t_pt")
        """
        if model_name not in cls._models:
            raise ValueError(f"Model '{model_name}' not found in the factory.")
        
        model_class = cls._models[model_name]

        # If the model requires a model path, check if it was provided
        if model_class == SAM2:
            if model_path is None:
                raise TypeError(f"{model_class.__name__} requires a model path for initialization.")
            return model_class(model_path)
        
        return model_class()
