import numpy as np
import tensorflow as tf
import os

# Path to model files
MODEL_PATH = "model1.json"
WEIGHTS_PATH = "model1.h5"

def load_model():
    """Load the DOS detection model"""
    try:
        # Load model architecture from JSON
        with open(MODEL_PATH, 'r') as json_file:
            loaded_model_json = json_file.read()
        model = tf.keras.models.model_from_json(loaded_model_json)
        
        # Load weights
        model.load_weights(WEIGHTS_PATH)
        
        # Compile model
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("DOS detection model loaded successfully!")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def predict_dos_attack(time_diffs):
    """
    Predict if a request pattern is a DOS attack
    
    Args:
        time_diffs: List of 8 time differences between requests
    
    Returns:
        tuple: (is_attack, confidence) where is_attack is a boolean and confidence is a float
    """
    # Load the model
    model = load_model()
    if model is None:
        print("Model not available. Cannot make predictions.")
        return False, 0.0
    
    try:
        # Preprocess the data
        features = np.array(time_diffs).reshape(1, 8, 1)  # Reshape for Conv1D input
        
        # Predict using the model
        prediction = model.predict(features)
        predicted_class = np.argmax(prediction, axis=1)[0]
        confidence = float(prediction[0][predicted_class])
        
        # Print prediction results
        print(f"Prediction: {'DOS Attack' if predicted_class == 1 else 'Normal Traffic'}")
        print(f"Confidence: {confidence:.4f}")
        
        # Return True if DOS attack (class 1) along with confidence
        return (predicted_class == 1), confidence
    except Exception as e:
        print(f"Error during prediction: {e}")
        return False, 0.0

def main():
    # Check if model exists
    if not os.path.exists(MODEL_PATH) or not os.path.exists(WEIGHTS_PATH):
        print(f"Model files not found. Please make sure {MODEL_PATH} and {WEIGHTS_PATH} exist.")
        return
    
    # Example data for testing
    print("Testing with normal traffic pattern:")
    normal_example = [0.5, 0.7, 0.6, 0.8, 0.5, 0.7, 0.9, 0.6]  # Varied timestamps
    is_attack, confidence = predict_dos_attack(normal_example)
    print(f"Is attack: {is_attack}, Confidence: {confidence:.4f}\n")
    
    print("Testing with DOS attack pattern:")
    attack_example = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]  # Very regular timestamps
    is_attack, confidence = predict_dos_attack(attack_example)
    print(f"Is attack: {is_attack}, Confidence: {confidence:.4f}\n")
    
    # Let user test with custom input
    print("Enter 8 time differences to test (comma-separated):")
    try:
        user_input = input().strip()
        if user_input:
            time_diffs = [float(x.strip()) for x in user_input.split(',')]
            if len(time_diffs) == 8:
                is_attack, confidence = predict_dos_attack(time_diffs)
                print(f"Is attack: {is_attack}, Confidence: {confidence:.4f}")
            else:
                print("Please provide exactly 8 values.")
    except ValueError:
        print("Invalid input. Please enter numeric values separated by commas.")

if __name__ == "__main__":
    main()