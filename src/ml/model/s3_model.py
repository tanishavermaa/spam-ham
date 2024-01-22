# from src.cloud_storage.aws_syncer import S3Sync
import os,sys
import subprocess

from src.cloud_storage.aws_storage import S3Sync
from src.logger import logging as lg
from src.exception import SpamhamException
from src.utils.main_utils import MainUtils
from src.constant.training_pipeline import *
from src.constant.s3_bucket import TRAINING_BUCKET_NAME
from src.constant.training_pipeline import MODEL_FILE_NAME


class S3Model:

    def __init__(self) -> None:
        self.s3_sync = S3Sync()
        self.utils = MainUtils()
    
    def is_bucket_empty(self) -> bool:

        command = f"""aws s3api list-objects-v2 --bucket {TRAINING_BUCKET_NAME} """
        
        output = subprocess.check_output(command, shell=True)

        output = output.decode('utf-8').rstrip()

        response = True if len(output) == 0 else False  

        return response

    def is_model_present(self) -> bool:

        
        if not self.is_bucket_empty():
            command = f"""aws s3api list-objects-v2 --bucket {TRAINING_BUCKET_NAME} --query "contains(Contents[].Key, '{MODEL_TRAINER_TRAINED_MODEL_NAME}')" """
          
            output = subprocess.check_output(command, shell=True)

            output = output.decode('utf-8').rstrip()

            output = True if output=='true' else False
        else:
            output = False      
        return output
        
    def save_model_to_local(self, model_path):
        try:
            self.s3_sync.sync_folder_from_s3(folder=model_path, aws_bucket_name=TRAINING_BUCKET_NAME)
        except Exception as e:
            raise SpamhamException(e,sys)

    def load_s3_model(self, model_dir):
        """
        params:
        
            model_dir : local dir to save the model
            

        """
        
        try:
            is_model_present = self.is_model_present()
            
            if is_model_present:
                self.save_model_to_local(model_dir)
                model = self.utils.load_object(
                    os.path.join(model_dir,
                                 MODEL_FILE_NAME)
                )
            else:
                model = None 
            return model
        except Exception as e:
            raise SpamhamException(e,sys)

    def save_model_to_s3(self,model_dir, remove_existing_model = True):
        
        """
        params:
            model_dir : local dir where the model is saved
        """

        try:
            if remove_existing_model:
                command = f"aws s3 rm s3://{TRAINING_BUCKET_NAME}/{MODEL_TRAINER_TRAINED_MODEL_NAME}"
                os.system(command)
                lg.info("existing model is removed")
            self.s3_sync.sync_folder_to_s3(folder=model_dir, aws_buket_name= TRAINING_BUCKET_NAME)

        except Exception as e:
            raise SpamhamException(e,sys)
    




