import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
import io
import base64
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load TFLite Model
interpreter = tflite.Interpreter(model_path="model.tflite")  
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

class_labels = ["Blight", "Blast", "Brown Spot", "Tungro", "Cercospora", "False Smut"]

def preprocess_image(image):
    """Preprocess gambar untuk TFLite"""
    image = image.convert('RGB')
    image = image.resize((224, 224))
    image = np.asarray(image, dtype=np.float32) / 255.0
    return np.expand_dims(image, axis=0)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        image_data = data.get("image")

        if image_data.startswith("data:image"):
            image_data = image_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        processed_image = preprocess_image(image)

        interpreter.set_tensor(input_details[0]["index"], processed_image)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]["index"])

        max_index = np.argmax(output_data[0])
        predicted_class = class_labels[max_index]
        confidence = float(output_data[0][max_index]) * 100

        return jsonify({
            "prediction": predicted_class,
            "confidence": f"{confidence:.2f}%"
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
