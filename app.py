import tensorflow as tf
import numpy as np
import base64
import cv2
from flask import Flask, request, jsonify
from PIL import Image
import io
from flask import Flask, render_template

app = Flask(__name__)

# Load model
model = tf.keras.models.load_model("best_model_fix.keras")  # Pastikan ini model yang benar

# Kelas penyakit yang akan diprediksi
class_labels = [ "Blight", "Blast", "Brown Spot", "Tungro", "Cercospora", "False Smut"]

def preprocess_image(image):
    """Preprocessing gambar sebelum masuk model"""
    image = image.convert('RGB')
    image = image.resize((224, 224))  # Sesuaikan ukuran model
    image = np.array(image) / 255.0  # Normalisasi
    image = np.expand_dims(image, axis=0)  # Tambahkan batch dimension
    return image

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        image_data = data.get("image")

        if image_data.startswith("data:image"):
            image_data = image_data.split(",")[1]  # Hapus prefix data:image/png;base64,
        
        image_bytes = base64.b64decode(image_data)  
        image = Image.open(io.BytesIO(image_bytes))  # Buka gambar dengan PIL
        
        processed_image = preprocess_image(image)  # Preprocessing sebelum ke model
        predictions = model.predict(processed_image)[0]  # Model memberi output array probabilitas
        
        max_index = np.argmax(predictions)  # Ambil index dengan nilai tertinggi
        predicted_class = class_labels[max_index]  # Ambil label sesuai index
        confidence = float(predictions[max_index]) * 100  # Ambil confidence dalam %

        return jsonify({
            "prediction": predicted_class,
            "confidence": f"{confidence:.2f}%"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
