from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelEvaluationArtifact, DataTransformationArtifact
from sklearn.metrics import f1_score
from src.exception import SpamhamException
from src.constant.training_pipeline import TARGET_COLUMN
from src.logger import logging

import sys
import pandas as pd
import numpy as np

from src.constant.training_pipeline import *

from src.ml.model.s3_model import S3Model

from dataclasses import dataclass
from typing import Optional
from src.entity.config_entity import Prediction_config

from src.utils.main_utils import MainUtils,load_numpy_array_data
from src.ml.metric import calculate_metric
from src.entity.artifact_entity import ClassificationMetricArtifact


@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    changed_accuracy: float
    best_model_metric_artifact: ClassificationMetricArtifact

def convert_test_numpy_array_to_dataframe(array:str):
    """Converts numpy array to dataframe"""
    prediction_config = Prediction_config().__dict__
    columns = prediction_config['prediction_schema']['columns'].keys()
    
    
    dataframe = pd.DataFrame(array, columns=columns)
    return dataframe

class ModelEvaluation:

    def __init__(self, model_eval_config: ModelEvaluationConfig, data_ingestion_artifact: DataIngestionArtifact,
                 model_trainer_artifact: ModelTrainerArtifact, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.utils = MainUtils()
            
            self.s3_model = S3Model()
        except Exception as e:
            raise SpamhamException(e, sys) from e

    def get_best_model(self):
        try:
                        
            spamham_detector = self.s3_model.load_s3_model(model_dir=self.model_eval_config.best_model_dir)

            if spamham_detector:
                return spamham_detector
            
            return None
        
        except Exception as e:
            raise SpamhamException(e, sys)
        
    def generate_test_data(self):
        try:
            test_array = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            _, y_test = test_array[:, :-1], test_array[:, -1]
            
            x_test = test_df[FEATURE_COLUMN]
            
            return x_test, y_test
        except Exception as e:
            raise SpamhamException(e, sys)

    def evaluate_model(self) -> EvaluateModelResponse:
        try:
<<<<<<< HEAD
            test_arr = np.load(self.data_transformation_artifact.transformed_test_file_path)
            # x_test = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            x_test, y_test = test_arr[:, :-1] , test_arr[:, -1]
           
=======
            x_test, y_test = self.generate_test_data()
            
          
>>>>>>> 73fedd4aa8a26de2f5444430f6e819dce608ea0d
            trained_model = self.utils.load_object(file_path=self.model_trainer_artifact.trained_model_file_path)
            # y.replace(TargetValueMapping().to_dict(), inplace=True)
            y_hat_trained_model = trained_model.predict(x_test)

            trained_model_f1_score = f1_score(y_test, y_hat_trained_model)
            best_model_f1_score = None
            best_model_metric_artifact = None
            best_model = self.get_best_model()
            if best_model is not None:
                y_hat_best_model = best_model.predict(x_test)
                best_model_f1_score = f1_score(y_test, y_hat_best_model)
                best_model_metric_artifact = calculate_metric(best_model, x_test, y_test)
            # calucate how much percentage training model accuracy is increased/decreased
            tmp_best_model_score = 0 if best_model_f1_score is None else best_model_f1_score
            result = EvaluateModelResponse(trained_model_f1_score=trained_model_f1_score,
                                           best_model_f1_score=best_model_f1_score,
                                           is_model_accepted=trained_model_f1_score > tmp_best_model_score,
                                           changed_accuracy=trained_model_f1_score - tmp_best_model_score,
                                           best_model_metric_artifact=best_model_metric_artifact
                                           )
            logging.info(f"Result: {result}")
            return result

        except Exception as e:
            raise SpamhamException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            evaluate_model_response = self.evaluate_model()
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                best_model_path=self.model_trainer_artifact.trained_model_file_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.changed_accuracy,
                best_model_metric_artifact=evaluate_model_response.best_model_metric_artifact
            )

          
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise SpamhamException(e, sys) from e
