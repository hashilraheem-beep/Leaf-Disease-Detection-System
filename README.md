# Leaf Disease Detection System

A deep learning web application that classifies plant leaf diseases from images for fast, early diagnosis.

## Features
- Upload a leaf image and get the predicted disease
- Image processing with OpenCV and a trained deep learning model (TensorFlow/Keras)
- User interface (`LeafFront`) and admin panel (`LeafBack`)
- Model training script (`train_model.py`)

## Tech Stack
Python, Django, TensorFlow, Keras, OpenCV, SQLite

## Project Structure
- `LeafFront/` – user-facing app
- `LeafBack/` – admin app
- `LeafDiseaseDetection/` – Django project settings
- `train_model.py` – trains the model
- `best_model.h5`, `tomato_model.h5` – trained models

## How to Run
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Create an admin user: `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`
6. Open http://127.0.0.1:8000 in your browser

## Note
The training dataset is not included because of its size.

## Author
Hashil K R
