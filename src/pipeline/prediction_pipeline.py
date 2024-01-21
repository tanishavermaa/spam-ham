from src.logger import logging
from src.entity.config_entity import DataTransformationConfig , ModelTrainerConfig
from src.constant.training_pipeline import *
from src.entity.config_entity import training_pipeline_config
from src.entity.config_entity import Prediction_config, PredictionPipelineConfig

from src.entity.config_entity import DataTransformationConfig , ModelTrainerConfig
from src.logger import logging
from src.utils.main_utils import MainUtils
from src.ml.model.s3_model import S3Model

from src.exception import SpamhamException
import pandas as pd
import numpy as np
import sys

import logging
import sys
from pandas import DataFrame
import pandas as pd



    
class PredictionPipeline:
    def __init__(self):
        self.utils = MainUtils()
        self.s3_model = S3Model()
        
        
    def get_trained_model(self):
        """
        method: get_trained_model
        
        objective: this method returns the best model which is pushed to s3 bucket. 

      

        Raises:
            SpamhamException: 

        Returns:
            model: latest trained model from s3 bucket
        """
        try:
            prediction_config = PredictionPipelineConfig()
            
            model = self.s3_model.load_s3_model(
                model_dir= prediction_config.model_storing_dir
            )
            
            return model
                
        except Exception as e:
            raise SpamhamException(e, sys) from e
        
    def run_pipeline(self, input_data:list):
        
        """
        method: run_pipeline
        
        objective: run_pipeline method runs the whole prediction pipeline.

        Raises:
            SpamhamException: 
        """
        try:
            model = self.get_trained_model()
            prediction = model.predict(input_data)
            return prediction
            
        except Exception as e:
            raise SpamhamException(e, sys)
            
            
        
            
        

 
        

        