from typing import Optional, Type

from machine_models.strategies import SAM2, IMachineLearningModel


class MachineLearningModelFactory:
    """
    Design Pattern: Factory
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
        """ Factory method para instanciar um modelo de machine learning

        Args:
            model_name (str): O nome da instancia do modelo. ("sam2")
            model_path (Optional[str]): Argumento opcional com o caminho do modelo a ser instanciado
             (para aqueles que precisam como yolo_model = YOLO(model_path = 'yolo_v9n.pt')).
        
        Returns:
            IMachineLearningModel: Uma instancia do modelo solicitado.
        
        Raises:
            ValueError: Se o nome do modelo não ser encontrado na factory
            TypeError: Se o modelo precisa de um path e não foi passado
        Example:
            >> factory = MachineLearningModelFactory()
            >> sam2_model = factory.create_model("sam2", "sam2_t_pt")
        """
        if model_name not in cls._models:
            raise ValueError(f"Model '{model_name}' não encontrado na factory.")
        
        model_class = cls._models[model_name]

        # If the model requires a model path, check if it was provided
        if model_class == SAM2:
            if model_path is None:
                raise TypeError(f"{model_class.__name__} requires a model path for initialization.")
            return model_class(model_path)
        
        return model_class()
