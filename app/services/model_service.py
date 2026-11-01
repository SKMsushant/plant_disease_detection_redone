from PIL import Image
import io
import tensorflow as tf
import numpy as np
import json

from model_definition import build_optimal_model
from ..config import WEIGHTS_PATH,HPS_PATH,CLASS_NAMES,REMEDIES,IMG_SIZE,DEFAULT_REMEDY
from ..data.remedies import get_remedy_for_class


class PlantDiseasePredictor:

    def __init__(self):
        self.model=None

    def load_model(self)->None:
        """Loads hyperparameters ,build architechture and loads weights into memory"""

        print("Loading HyperParameters............")
        with open(HPS_PATH,'r') as f:
            hps=json.load(f)

        print("[INFO] Rebuilding YOLOv8Nano + 4 head Transformer model")
        self.model=build_optimal_model(
            num_classes=len(CLASS_NAMES),
            img_size=IMG_SIZE,
            hps_dict=hps
        )

        print("[INFO] Loading weights into model architechture")
        self.model.load_weights(str(WEIGHTS_PATH))
        print("weights to the model loaded successfully into memory.......")

    def preprocess_image(self,image_bytes:bytes)->dict:
        """converts raw image bytes into RGB and resizes it to (224,224) and creates batch"""

        image=Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image=image.resize(
            size=(IMG_SIZE,IMG_SIZE)
        )
        image_array=np.array(image,dtype=np.float32)
        image_batch=np.expand_dims(image_array,axis=0)
        return image_batch


    def predict(self,image_bytes:bytes,filename:str)->dict:
        """Runs model's Inference and returns disease prediction with remedies"""

        if self.model is None:
            raise RuntimeError('Model is not initialized run load_model() first')

        image_batch=self.preprocess_image(image_bytes)

        predictions=self.model(image_batch,training=False)[0].numpy()

        pred_idx=int(np.argmax(predictions))
        pred_class=CLASS_NAMES[pred_idx]
        pred_confidence=float(predictions[pred_idx])

        plant_details=get_remedy_for_class(predicted_class=pred_class)


        remedyinforesponse={
            "disease":plant_details['Disease'],
            "actions":plant_details['Action']
        }

        final_respoonse={
            "filename":filename,
            "plant":plant_details['Plant'],
            "condition":plant_details['Condition'],
            "is_healthy":plant_details['Is_Healthy'],
            "confidence":pred_confidence,
            "remedy":remedyinforesponse
        }

        return final_respoonse


predictor=PlantDiseasePredictor()