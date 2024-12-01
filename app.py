from flask import Flask, request, jsonify
from flask_cors import CORS  
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')


app = Flask(__name__)
CORS(app) 
model = load_model('leaf_disease_model.h5')  

# Preprocessing function
def preprocess_image(image):
    try:
        image = Image.open(image)
        image = image.resize((64, 64))
        image = image.convert('RGB')  
        image = np.array(image) / 255.0  
        image = np.expand_dims(image, axis=0)  
        return image
    except Exception as e:
        print(f"Error in image preprocessing: {e}")
        return None

@app.route('/predict', methods=['POST'])
def predict():
    print("Request received")
    
    if 'image' not in request.files:
        print("No image part in the request")
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']
    
    if image.filename == '':
        print("Empty file received")
        return jsonify({"error": "No image selected"}), 400
    
    try:
        print(f"File received: {image.filename}")
        
        img = preprocess_image(image)
        
        if img is None:
            return jsonify({"error": "Failed to preprocess the image"}), 500
        
        prediction = model.predict(img)
        predicted_label = np.argmax(prediction, axis=1)[0]
        
        categories = ["Healthy", "Rusty", "Powdery"]
        result = categories[predicted_label]

        print(f"Prediction: {result}")
        
        precautions = {
            "Healthy": "No action needed.",
            "Rusty": "Apply anti-rust fungicide.",
            "Powdery": "Use sulfur-based fungicides."
        }

        return jsonify({"prediction": result, "precautions": precautions[result]})
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "Failed to process the image"}), 500


if __name__ == '__main__':
    app.run(debug=True) 
