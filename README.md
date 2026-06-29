🎵 Moodify – AI-Powered Emotion-Based Music Recommendation System

Moodify is an intelligent music recommendation web application that analyzes a user's emotions through facial expressions, speech, or text input, and recommends personalized songs based on their emotional state. The project integrates Machine Learning, Computer Vision, and Natural Language Processing (NLP) to provide an engaging and personalized music experience.

The system uses Facial Emotion Recognition (FER) with MTCNN for face detection, Speech-to-Text for voice analysis, keyword-based text emotion detection, and Agglomerative Hierarchical Clustering to group songs based on Spotify audio features.

✨ Features
😊 Facial Emotion Detection using FER and MTCNN
🎤 Speech Emotion Detection using Speech Recognition
💬 Text-Based Emotion Detection
🎵 AI-powered Song Recommendation
🎧 YouTube Search Integration for song playback
👤 User Authentication with Secure Password Hashing
❤️ Like and Save Favorite Songs
➕ Add Custom Songs
📂 Personalized User Dashboard
📊 Spotify Audio Feature-Based Clustering
🔐 Secure Login using Password Hashing
🌐 Responsive Flask Web Application
🛠️ Tech Stack
Frontend
HTML5
CSS3
JavaScript
Jinja2 Templates
Backend
Python
Flask
Machine Learning
Agglomerative Hierarchical Clustering
StandardScaler
FER (Facial Emotion Recognition)
MTCNN
OpenCV
Database
SQLite
Libraries
Pandas
NumPy
Scikit-learn
OpenCV
FER
SpeechRecognition
Matplotlib
SciPy
Werkzeug
Pickle
📌 Workflow
User
   │
   ├── Face Emotion Detection
   ├── Speech Emotion Detection
   └── Text Emotion Detection
           │
           ▼
Detected Emotion
           │
           ▼
Emotion Mapping
           │
           ▼
Agglomerative Hierarchical Clustering
           │
           ▼
Spotify Song Recommendation
           │
           ▼
YouTube Playback
📊 Machine Learning Pipeline
Data Cleaning
Missing Value Removal
Duplicate Removal
Feature Selection
Feature Scaling using StandardScaler
Agglomerative Hierarchical Clustering
Emotion-to-Cluster Mapping
Personalized Song Recommendation
📁 Dataset

Spotify Audio Features Dataset

Selected Features:

Energy
Valence
Tempo
Danceability
Loudness
