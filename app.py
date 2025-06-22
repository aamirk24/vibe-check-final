from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import base64
import uuid
import comet_ml
from PIL import Image
import io
import datetime
import json

# --- Comet ML Setup ---
load_dotenv()
comet_experiment = None
api_key = os.getenv("COMET_API_KEY")
project_name = os.getenv("COMET_PROJECT_NAME")
workspace = os.getenv("COMET_WORKSPACE")

if api_key and project_name and workspace:
    try:
        comet_experiment = comet_ml.Experiment(
            api_key=api_key,
            project_name=project_name,
            workspace=workspace
        )
        comet_experiment.set_name("moody-playlist-webapp-session")
        print("Comet ML Experiment initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize Comet ML Experiment: {e}")
else:
    print("Comet ML environment variables not fully set. Skipping initialization.")
# --- End Comet Setup ---

from mood_detector import detect_mood
from spotify_player import initialize_spotify, get_playlist

initialize_spotify()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        image_data = base64.b64decode(data['image'].split(',')[1])
        mood_result = detect_mood(image_data)
        
        if not mood_result:
            return jsonify({'error': 'Could not detect mood'}), 500

        mood = mood_result.get('label')
        confidence = mood_result.get('score')

        playlist = get_playlist(mood)
        if not playlist:
            return jsonify({'error': 'Could not find a suitable playlist'}), 500

        if comet_experiment:
            prediction_id = str(uuid.uuid4())
            
            # Note: We are no longer using the context_manager, as it's not needed
            # with our new, more direct logging method.
            try:
                image = Image.open(io.BytesIO(image_data))
                # --- THE FIX ---
                # Embed the prediction_id directly in the image's filename.
                comet_experiment.log_image(image, name=f"input_{prediction_id}.jpg")
            except Exception as e:
                print(f"Failed to log image to Comet: {e}")
            
            # Log metrics and parameters normally
            comet_experiment.log_metric("confidence", confidence, step=comet_experiment.curr_step)
            comet_experiment.log_parameter("mood_prediction", mood, step=comet_experiment.curr_step)
        else:
            prediction_id = str(uuid.uuid4()) 
        
        return jsonify({
            'mood': mood,
            'confidence': confidence,
            'playlist': playlist,
            'prediction_id': prediction_id
        })

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({'error': 'An internal server error occurred'}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.json
        prediction_id = data.get('prediction_id')
        correct_mood = data.get('mood')

        if not (prediction_id and correct_mood):
            return jsonify({'error': 'Missing prediction_id or mood for feedback'}), 400

        if comet_experiment:
            feedback_payload = {
                "prediction_id": prediction_id,
                "ground_truth_mood": correct_mood,
                "timestamp": str(datetime.datetime.now())
            }
            feedback_string = json.dumps(feedback_payload, indent=2)

            # Log feedback as a unique JSON asset. This part is already correct.
            comet_experiment.log_asset_data(
                data=feedback_string,
                file_name=f"feedback_{prediction_id}.json"
            )
        
        app.logger.info(f"Feedback received for prediction {prediction_id}: Correct mood is {correct_mood}")
        return jsonify({'status': 'Feedback received, thank you!'})

    except Exception as e:
        app.logger.error(f"Error processing feedback: {e}")
        return jsonify({'error': 'Failed to process feedback'}), 500

if __name__ == '__main__':
    app.run(debug=True)
