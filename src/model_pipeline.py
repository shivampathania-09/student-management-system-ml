import joblib
import os
import pandas as pd

def load_model(filepath):
    """Loads a trained machine learning model or encoder."""
    if os.path.exists(filepath):
        return joblib.load(filepath)
    else:
        raise FileNotFoundError(f"File not found at {filepath}")

def predict_grade(weekly_attendance, class_participation, total_score):
    """
    Predicts a student's grade using the trained model.
    Returns a tuple: (predicted_grade, confidence_percentage)
    """
    try:
        # Validate inputs are numeric
        weekly_attendance = float(weekly_attendance)
        class_participation = float(class_participation)
        total_score = float(total_score)
    except ValueError:
        return None, "Error: All inputs must be numeric values."

    model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'student_model.pkl')
    le_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'label_encoder.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(le_path):
        return None, "Error: Model or Label Encoder missing. Train the model first."
        
    try:
        model = load_model(model_path)
        le = load_model(le_path)
    except Exception as e:
        return None, f"Error loading model artifacts: {str(e)}"
    
    # Create DataFrame to match feature names used during training
    input_data = pd.DataFrame({
        'attendance_percentage': [weekly_attendance],
        'class_participation': [class_participation],
        'total_score': [total_score]
    })
    
    try:
        prediction_encoded = model.predict(input_data)[0]
        predicted_grade = le.inverse_transform([prediction_encoded])[0]
        
        confidence = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_data)[0]
            confidence = round(max(probabilities) * 100, 2)
            
        return predicted_grade, confidence
    except Exception as e:
        return None, f"Prediction error: {str(e)}"
