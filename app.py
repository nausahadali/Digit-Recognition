import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

# Load the pre-trained MNIST model
print("Loading MNIST model...")
model_path = 'digit_model.h5'
if not os.path.exists(model_path):
    print("Training improved model... this may take a few minutes")
    
    # Load MNIST dataset
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    
    # Normalize data
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    # Reshape for CNN
    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)
    
    # Data augmentation
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        zoom_range=0.1,
        fill_mode='nearest'
    )
    

    model = tf.keras.Sequential([
        # First convolutional block
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1), padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),
        
        # Second convolutional block
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),
        
        # Third convolutional block
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),
        
        # Flatten and dense layers
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("Training with data augmentation...")
    model.fit(
        datagen.flow(x_train, y_train, batch_size=64),
        epochs=20,
        validation_data=(x_test, y_test),
        verbose=1
    )
    model.save(model_path)
    print("Model trained and saved!")
else:
    print("Loading saved model...")
    model = tf.keras.models.load_model(model_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get image data from request
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Remove data URI prefix
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        # Decode image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes)).convert('L')
        
        # Resize to 28x28
        image = image.resize((28, 28), Image.Resampling.LANCZOS)
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Make prediction
        prediction = model.predict(np.array([image_array]), verbose=0)
        predicted_digit = int(np.argmax(prediction[0]))
        confidence = float(np.max(prediction[0])) * 100
        
        # Get all predictions for visualization
        all_predictions = {str(i): float(prediction[0][i]) * 100 for i in range(10)}
        
        return jsonify({
            'digit': predicted_digit,
            'confidence': round(confidence, 2),
            'all_predictions': all_predictions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port)
