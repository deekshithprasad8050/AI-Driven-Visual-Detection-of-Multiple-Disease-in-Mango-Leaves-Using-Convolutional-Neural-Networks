import numpy as np
from PIL import Image
from io import BytesIO
from flask import current_app
from .model_loader import ModelLoader
import cv2 

class PredictService:
    """
    Handles all pre-processing, prediction execution, and post-processing 
    for the mango leaf disease classification model.
    """
    
    def __init__(self):
        self.classes = current_app.config['DISEASE_CLASSES']
        self.image_size = current_app.config['IMAGE_SIZE']
        self.color_mode = current_app.config['COLOR_MODE']
        self.model = ModelLoader.get_model()

        # ✅ Reduced threshold (less strict)
        self.BLUR_THRESHOLD = 10.0  

    def _preprocess_image(self, image_file_storage):
        try:
            # ✅ Read image safely
            image_data = image_file_storage.read()
            image_file_storage.seek(0)  # IMPORTANT FIX

            img_stream = BytesIO(image_data)
            img = Image.open(img_stream)

            # Resize + convert
            img_resized = img.convert('RGB').resize(self.image_size)

            # ✅ Blur detection
            img_array_cv = np.asarray(img_resized, dtype=np.uint8)
            gray = cv2.cvtColor(img_array_cv, cv2.COLOR_RGB2GRAY)

            variance = cv2.Laplacian(gray, cv2.CV_64F).var()

            # ⚠️ Don't crash → only warn
            if variance < self.BLUR_THRESHOLD:
                current_app.logger.warning(
                    f"Blur detected ({variance:.2f}) but continuing prediction"
                )

            # Normalize
            img_array = np.asarray(img_resized, dtype=np.float32) / 255.0

            return np.expand_dims(img_array, axis=0)

        except Exception as e:
            current_app.logger.error(f"Preprocessing error: {e}")
            raise ValueError("Invalid image file or preprocessing failed.")

    def analyze_image(self, image_file_storage):
        try:
            # 1. Preprocess
            model_input = self._preprocess_image(image_file_storage)

            # 2. Predict
            predictions = self.model.predict(model_input)[0]

            # 3. Post-process
            max_index = np.argmax(predictions)

            predicted_class = self.classes[max_index]
            confidence_score = float(predictions[max_index])

            raw_output = {
                self.classes[i]: float(prob)
                for i, prob in enumerate(predictions)
            }

            return {
                "predicted_class": predicted_class,
                "confidence_score": confidence_score,
                "raw_output": raw_output
            }

        except Exception as e:
            current_app.logger.error(f"Prediction error: {e}")
            raise ValueError("Prediction failed. Please try again.")