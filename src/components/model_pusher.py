import os, sys

from src.constant.s3_bucket import *
# from src.cloud_storage.aws_storage import S3Sync
from src.ml.model.s3_model import S3Model

from src.entity.artifact_entity import (ModelPusherArtifact,
                                           ModelTrainerArtifact)
from src.entity.config_entity import ModelPusherConfig
from src.exception import SpamhamException
from src.logger import logging


class ModelPusher:
    def __init__(
        self,
        model_trainer_artifact: ModelTrainerArtifact,
        model_pusher_config: ModelPusherConfig,
    ):
        self.s3_model =  S3Model()
        self.model_trainer_artifact = model_trainer_artifact
        self.model_pusher_config = model_pusher_config
        

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")

        try:
            logging.info("Uploading artifacts folder to s3 bucket")
            self.s3_model.save_model_to_s3(
                model_dir= os.path.dirname(self.model_trainer_artifact.trained_model_file_path),
                # bucket_name = self.model_pusher_config.bucket_name
            )
            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path,
            )
            logging.info("Uploaded artifacts folder to s3 bucket")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelTrainer class")
            return model_pusher_artifact
        except Exception as e:
            raise SpamhamException(e, sys) from e
