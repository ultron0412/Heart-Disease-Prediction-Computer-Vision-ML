import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
MODEL_PATH = BASE_DIR / "models" / "image" / "heart_cnn.keras"

model = load_model(MODEL_PATH)

def predict_ecg_image(img_path: str) -> float:
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    prob = model.predict(img_array)[0][0]
    return float(prob)
