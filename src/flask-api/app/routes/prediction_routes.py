"""
API routes for prediction endpoint.
"""
from flask import Blueprint, request, jsonify
import pickle
import pandas as pd
from config import Config
from app.utils.feature_extraction import extract_all_features

# Create blueprint
prediction_bp = Blueprint('prediction', __name__)

# Load the trained model
try:
    with open(Config.MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    model_loaded = True
except Exception as e:
    print(f"Error loading model: {e}")
    model_loaded = False

@prediction_bp.route('/predict', methods=['POST'])
def predict():
    """
    Flask endpoint to extract features from packet data and make prediction.

    Request:
        JSON array of packets from node.js

    Returns:
        {
            "prediction": 0 or 1,
            "is_attack": true/false
        }
    """
    try:
        # Check if model is loaded
        if not model_loaded:
            return jsonify({'error': 'Model not loaded. Check server logs.'}), 503
            
        # Get packet data from request
        packet_data = request.json

        if not packet_data or len(packet_data) == 0:
            return jsonify({'error': 'Empty packet data'}), 400

        # Validate packet structure
        required_fields = ['timestamp', 'src_ip', 'dst_ip', 'src_port', 'dst_port']
        for packet in packet_data:
            missing_fields = [field for field in required_fields if field not in packet]
            if missing_fields:
                return jsonify({
                    'error': f'Missing required fields in packet: {", ".join(missing_fields)}'
                }), 400

        # Extract features
        features = extract_all_features(packet_data)

        # Create DataFrame for prediction
        feature_df = pd.DataFrame([features])

        # Ensure columns are in the correct order for the model
        expected_cols = ['Fwd IAT Std', 'Bwd IAT Std', 'Flow IAT Std',
                        'Fwd IAT Max', 'Flow IAT Mean', 'Flow IAT Max',
                        'Fwd IAT Mean', 'Fwd IAT Total', 'Flow Duration',
                        'Bwd IAT Max', 'Idle Max', 'Idle Mean']

        feature_df = feature_df[expected_cols]

        # Make prediction
        probabilities = model.predict_proba(feature_df)[0].tolist()

        # Apply threshold for binary classification (class 1 is typically the attack class)
        is_attack = probabilities[1] > Config.PREDICTION_THRESHOLD

        # Return minimal result as requested
        result = {
            'prediction': int(is_attack),
            'is_attack': bool(is_attack)
        }

        # Add detailed results if debug mode is enabled
        if hasattr(Config, 'DEBUG_MODE') and Config.DEBUG_MODE:
            result['details'] = {
                'probabilities': probabilities,
                'threshold': Config.PREDICTION_THRESHOLD,
                'features': features
            }

        return jsonify(result)

    except ValueError as e:
        # Handle specific ValueError exceptions (like timestamp parsing)
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        # Log the exception for server-side debugging
        print(f"Prediction error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500