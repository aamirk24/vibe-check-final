from transformers import pipeline
from PIL import Image
import io

print("Initializing local image classification pipeline...")

# --- THE CHANGE ---
# Instead of loading from the internet, load from your local fine-tuned model directory.
# This path should match the NEW_MODEL_NAME from your finetune.py script.
MODEL_PATH = "./vibecheck-mood-detector-v2" 
# ---

classifier = pipeline(
    "image-classification", 
    model=MODEL_PATH, 
    use_fast=True
)
print(f"Pipeline initialized successfully from local model: {MODEL_PATH}")


def detect_mood(image_data):
    """
    Analyzes image data using a local transformers pipeline and returns the detected mood.
    """
    try:
        # The image_data is in bytes. We need to convert it into a format
        # the pipeline can read. We use PIL (Pillow) for this.
        # io.BytesIO treats the byte string like a file in memory.
        image = Image.open(io.BytesIO(image_data))

        # The classifier pipeline takes the image and returns the results.
        result = classifier(image)

        # --- Robust Checks ---
        # Handle cases where the pipeline might return a list within a list, e.g., [[...]]
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            result = result[0]

        # Ensure result is a non-empty list of dictionaries before proceeding
        if not (isinstance(result, list) and len(result) > 0 and all(isinstance(item, dict) for item in result)):
            print(f"Unexpected or empty result format from model: {result}")
            return None

        # Find the dictionary with the highest score. This is our top mood.
        top_mood_dict = max(result, key=lambda x: x.get('score', 0))

        # We need to ensure both keys exist before returning.
        if 'label' in top_mood_dict and 'score' in top_mood_dict:
            # The print statement from your example code is kept here for debugging
            print(top_mood_dict) 
            return top_mood_dict
        else:
            return None
    
    except Exception as e:
        print(f"Error during local mood detection: {e}. The input image might be invalid.")
        return None
