import tensorflow as tf
from tensorflow.keras.models import load_model

class ModelLoader:
    """
    Manages the singleton instance of the TensorFlow/Keras CNN model.
    """
    _model = None

    @classmethod
    def load_model(cls, model_path: str):
        if cls._model is None:
            try:
                print("📂 Loading model from:", model_path)

                # ✅ Safe loading
                cls._model = load_model(model_path, compile=False)

                print("✅ Model loaded successfully")

            except Exception as e:
                import traceback
                print("❌ MODEL LOAD ERROR:")
                traceback.print_exc()
                raise RuntimeError(f"Failed to load the ML model from {model_path}: {e}")

    @classmethod
    def get_model(cls) -> tf.keras.Model:
        if cls._model is None:
            raise RuntimeError("ML Model has not been loaded. Call load_model() first.")
        return cls._model


def preprocess_image(image_data, target_size=(224, 224)):
    from PIL import Image
    import numpy as np

    img = Image.open(image_data).convert('RGB')
    img = img.resize(target_size)

    img_array = np.asarray(img)
    img_array = img_array / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    return img_array