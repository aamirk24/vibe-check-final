# Vibe-Check 

VibeCheck is an intelligent web application that captures live webcam footage, analyzes the user's facial expression to determine their mood, and then suggests a curated Spotify playlist to match that vibe. This project demonstrates a complete MLOps (Machine Learning Operations) feedback loop, where user feedback is collected and used to fine-tune the underlying AI model for improved accuracy over time.

## 🚀 Key Features

*  **Live Mood Analysis:** Utilizes a live webcam feed and a deep learning model to perform real-time facial emotion recognition.
*  **Dynamic Spotify Playlists:** Connects to the Spotify API to search for and embed playlists that match the detected mood (e.g., "happy vibes", "sad songs").
*  **MLOps Feedback Loop:** Users can provide corrective feedback if the detected mood is incorrect. This feedback is logged to **Comet ML**.
*  **Model Fine-Tuning:** A dedicated script downloads the user feedback and images from Comet ML to fine-tune the AI model, creating a new, more accurate version.
*  **Confidence Score:** The UI displays a confidence bar, showing how certain the model is about its prediction.
*  **Modern UI:** A sleek, responsive, and dark-mode interface for an excellent user experience.

## ✨ Innovative Use of Comet ML for Production Observability

This project leverages Comet not just as an experiment tracker for training, but as a critical **production monitoring and observability tool**. This approach provides deep insights into the model's real-world performance.

* **Traceability from Input to Feedback:**

  * Every analysis generates a unique `prediction_id`.

  * This ID is used to name the input image asset (`input_{id}.jpg`) and is also passed to the frontend.

  * When a user submits feedback, this same `prediction_id` is included in the feedback log.

  * **Innovation:** This creates an unbreakable, traceable link between a specific input image, the model's output, and the user's "ground truth" label. This allows for precise debugging and analysis of individual prediction failures.

* **Live Model Observability:**

  * By logging every prediction's input image, output label (`mood_prediction`), and confidence score, we gain a live dashboard of our model's behavior.

  * **Innovation:** We can visually inspect the exact images that cause low-confidence predictions or are frequently misclassified, helping us identify patterns (e.g., the model struggles with poor lighting, certain angles, or specific expressions).

* **Real-World Evaluation Metrics:**

  * The `feedback_log.csv` generated from user feedback is more than just a log; it's a dataset for calculating **real-world accuracy**.

  * **Innovation:** Unlike evaluation on a static test set, this allows us to answer crucial business-facing questions like, "What was our model's actual accuracy with users this week?" or "Which two emotions are most often confused?" This measures true performance and guides the decision of when it's time to retrain the model.

This system transforms Comet from a simple training utility into the backbone of a data-centric MLOps workflow, enabling continuous improvement driven directly by user interaction.

## 🛠️ Tech Stack

* **Backend:** Python, Flask

* **Frontend:** HTML5, CSS3, JavaScript

* **ML Model:** Hugging Face Transformers (`dima806/facial_emotions_image_detection`)

* **MLOps & Experiment Tracking:** Comet ML

* **Music:** Spotify API (via `spotipy` library)

* **Core ML Libraries:** PyTorch, Pillow, `datasets`, `evaluate`, `accelerate`


## ⚙️ Setup and Installation
 Follow these steps to set up the project locally.

1. Clone the Repository
<img width="323" alt="Screenshot 2025-06-22 at 11 04 41" src="https://github.com/user-attachments/assets/fe7dd6c0-c5c6-4b19-aa82-45650a39f01f" />

2. Create and Activate a Virtual Environment
<img width="282" alt="Screenshot 2025-06-22 at 11 07 24" src="https://github.com/user-attachments/assets/d2690268-6958-4e74-a40f-be0fbc410f74" />

3. Install Dependencies
Install all required Python packages from the requirements.txt file.
<img width="316" alt="Screenshot 2025-06-22 at 11 08 32" src="https://github.com/user-attachments/assets/def1a957-5b93-4b4b-9934-370756764b57" />

Note: The finetune.py script requires additional libraries (datasets, accelerate, etc.), which can be installed separately when needed.

## ▶️ How to Run

   Start the Flask server:
<img width="161" alt="Screenshot 2025-06-22 at 11 13 46" src="https://github.com/user-attachments/assets/2063637c-00b8-47d7-bb4e-4f106fe134c4" />

## ▶️ Demo
<img width="1512" alt="Screenshot 2025-06-22 at 11 52 29" src="https://github.com/user-attachments/assets/22ccae97-ce59-4932-97e4-0473dfcbfb56" />

<img width="1510" alt="Screenshot 2025-06-22 at 11 52 38" src="https://github.com/user-attachments/assets/3f1b87b2-17b1-4c07-941d-d7dec03623fd" />


<img width="1512" alt="Screenshot 2025-06-22 at 11 52 54" src="https://github.com/user-attachments/assets/84bd1326-4730-40c4-a9ab-216916acf34d" />


