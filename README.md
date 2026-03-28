# Handwritten Digit Recognition Web Application

A modern, polished web application that uses TensorFlow and Flask to recognize handwritten digits drawn by users. Features a beautiful, responsive interface with real-time prediction and confidence visualization.

## Features

✨ **Interactive Canvas Drawing**
- Draw digits naturally using your mouse
- Real-time cursor feedback
- Smooth, responsive drawing experience

🤖 **AI-Powered Recognition**
- TensorFlow-based neural network trained on MNIST dataset
- High accuracy digit classification (0-9)
- Instant predictions

📊 **Confidence Visualization**
- Real-time confidence scores
- Visual confidence bar
- Complete breakdown of all digit probabilities
- Sorted by likelihood

🎨 **Modern, Polished UI**
- Sleek cyberpunk-inspired dark theme
- Smooth animations and transitions
- Fully responsive design
- Intuitive controls

## System Requirements

- Python 3.8 or higher
- 4GB RAM minimum (2GB for TensorFlow)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

### 1. Clone or download the project
```bash
cd digit-recognition
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

**If you have a stable internet connection:**
```bash
pip install -r requirements.txt
```

**If you get timeout errors (recommended for slow/unstable internet):**
```bash
pip install --default-timeout=1000 -r requirements.txt
```

**Or install one by one:**
```bash
pip install --default-timeout=1000 --retries 5 Flask Pillow numpy Werkzeug
pip install --default-timeout=1000 --retries 5 TensorFlow
```

Note: TensorFlow download is ~1.9GB on first install. See `INSTALLATION_GUIDE.md` for more solutions if you experience timeout errors.

## Running the Application

### 1. Start the Flask server
```bash
python app.py
```

The first run will:
- Download the MNIST dataset (~11MB)
- Train a neural network (takes 2-3 minutes)
- Save the trained model as `digit_model.h5`

Subsequent runs will load the pre-trained model instantly.

### 2. Open in browser
Navigate to: `http://localhost:5000`

## How to Use

1. **Draw a Digit**: Use your mouse to draw a digit (0-9) on the canvas
2. **Predict**: Click the "Predict" button to analyze your drawing
3. **View Results**: See the predicted digit and confidence score
4. **Clear**: Click "Clear" to erase and try again

### Tips for Best Results

**For Higher Accuracy:**
- Draw on a **white background** (white strokes on black, as the model expects)
- Make digits **large and bold** - fill most of the canvas
- Use **smooth, continuous strokes** without shaking
- Keep the digit **roughly centered** with margins
- Write in a **standard style** - not too slanted or decorative

See **ACCURACY_GUIDE.md** for detailed tips to improve recognition accuracy!

## Project Structure

```
digit-recognition/
├── app.py                 # Flask backend with TensorFlow model
├── requirements.txt       # Python dependencies
├── digit_model.h5        # Trained model (created on first run)
└── templates/
    └── index.html        # Frontend with canvas and UI
```

## Technical Stack

- **Backend**: Flask (Python web framework)
- **ML Model**: TensorFlow/Keras
- **Data**: MNIST dataset (70,000 handwritten digits)
- **Frontend**: HTML5 Canvas, Vanilla JavaScript, CSS3
- **Image Processing**: PIL (Python Imaging Library)

## Model Architecture

The neural network is a **Convolutional Neural Network (CNN)** with:

- **3 Convolutional blocks** with 32, 64, and 128 filters
- **Batch normalization** for stable training
- **Max pooling layers** to reduce spatial dimensions
- **Dropout layers** (25-50%) for regularization
- **2 Dense layers** (256 and 128 neurons) for classification
- **Total parameters**: ~650K

**Key Improvements**:
- CNN architecture better captures spatial patterns
- Data augmentation (rotations, shifts, zoom) during training
- Advanced image preprocessing (blur, adaptive thresholding, contour detection)
- Better handling of different handwriting styles

Training: 20 epochs on 60,000 MNIST samples + augmented data

Expected test accuracy: **~99% on MNIST**, **70-95% on real handwriting**

## API Endpoint

### POST `/predict`
Predicts the digit in a canvas drawing.

**Request:**
```json
{
    "image": "data:image/png;base64,..."
}
```

**Response:**
```json
{
    "digit": 5,
    "confidence": 98.75,
    "all_predictions": {
        "0": 0.1,
        "1": 0.2,
        "2": 0.3,
        ...
        "9": 0.05
    }
}
```

## Troubleshooting

### Installation timeout errors
If you get `ReadTimeoutError` during `pip install`:

```bash
# Use increased timeout (most common fix)
pip install --default-timeout=1000 -r requirements.txt
```

Or install packages one by one:
```bash
pip install --default-timeout=1000 --retries 5 Flask Pillow numpy Werkzeug
pip install --default-timeout=1000 --retries 5 TensorFlow
```

See `INSTALLATION_GUIDE.md` for 6 different solutions.

### TensorFlow takes long to import
- This is normal on first run. The library is optimizing for your system.
- Subsequent imports are much faster.

### Model training is slow
- First training takes 2-3 minutes
- This is normal; GPU acceleration would speed it up but isn't required.

### Canvas drawing is laggy
- Ensure no other heavy applications are running
- Try using a different browser
- Clear browser cache

### Port 5000 already in use
```bash
# Run on a different port
python -c "from app import app; app.run(port=5001)"
```



## Performance

- **Prediction Time**: ~100-200ms (including image preprocessing)
- **Model Size**: ~1.5MB (stored as digit_model.h5)
- **Memory Usage**: ~500MB (TensorFlow + Model)

## Future Enhancements

- [ ] Add digit confidence threshold
- [ ] Support for multi-digit recognition
- [ ] Real-time predictions as you draw
- [ ] Batch prediction capability
- [ ] Customizable brush sizes
- [ ] Drawing history/undo feature
- [ ] Export predictions as JSON/CSV
- [ ] GPU acceleration support
- [ ] Mobile touch support enhancement
- [ ] Custom model training interface

## License

This project is open source and available for educational and personal use.

## Acknowledgments

- MNIST Dataset: Yann LeCun, Corinna Cortes, Christopher J.C. Burges
- TensorFlow: Google AI
- Flask: Armin Ronacher and contributors

## Support

For issues or questions:
1. Check that all dependencies are installed correctly
2. Ensure Python 3.8+ is being used
3. Try running in a fresh virtual environment
4. Check that port 5000 is available

---

**Enjoy recognizing handwritten digits!** ✨
