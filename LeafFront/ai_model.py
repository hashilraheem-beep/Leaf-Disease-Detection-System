import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Get project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'tomato_model.h5')

# Load trained model
model = load_model(model_path)

# IMPORTANT: Must match training class order exactly
class_indices = {
    0: 'Bacterial Spot',
    1: 'Early Blight',
    2: 'Healthy Leaf',
    3: 'Late Blight',
    4: 'Leaf Mold',
    5: 'Septoria Leaf Spot',
    6: 'Target Spot',
    7: 'Tomato Mosaic Virus',
    8: 'Tomato Yellow Leaf Curl Virus',
    9: 'Two-Spotted Spider Mite',
}

solutions = {
    "Bacterial Spot": "Remove infected leaves and spray Copper Oxychloride 0.3%. Repeat after 7 days.",
    "Early Blight": "Remove infected leaves and spray Azoxystrobin fungicide. Repeat after 7 days.",
    "Healthy Leaf": "Continue normal crop management and monitor regularly.",
    "Late Blight": "Spray Metalaxyl + Mancozeb immediately. Repeat after 5–7 days.",
    "Leaf Mold": "Spray Azoxystrobin fungicide. Improve air circulation.",
    "Septoria Leaf Spot": "Spray Tebuconazole or Mancozeb. Repeat after 7 days.",
    "Target Spot": "Spray Tebuconazole or Azoxystrobin. Repeat after 7–10 days.",
    "Tomato Mosaic Virus": "Remove infected plants. Disinfect tools. Use virus-free seedlings.",
    "Tomato Yellow Leaf Curl Virus": "Remove infected plants. Control whiteflies immediately.",
    "Two-Spotted Spider Mite": "Spray Abamectin or Spiromesifen. Repeat after 7–10 days.",
}

def predict_leaf_disease(img_path):
    try:
        # Load and resize image
        img = image.load_img(img_path, target_size=(224, 224))

        # Convert to array
        img_array = image.img_to_array(img)

        # Expand dimensions
        img_array = np.expand_dims(img_array, axis=0)

        # IMPORTANT: Use MobileNetV2 preprocessing
        img_array = preprocess_input(img_array)

        # Predict
        prediction = model.predict(img_array)
        class_idx = np.argmax(prediction)
        confidence = float(np.max(prediction)) * 100

        disease = class_indices[class_idx]
        solution = solutions[disease]

        return {
            "disease": disease,
            "confidence": round(confidence, 2),
            "solution": solution
        }

    except Exception as e:
        return {"error": str(e)}