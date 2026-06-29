# 🎵 Moodify – AI-Powered Emotion-Based Music Recommendation System

> Detect your mood. Discover the perfect music.

Moodify is an AI-powered web application that recommends personalized songs based on a user's emotional state. The system detects emotions through **facial expressions**, **speech**, or **text input**, and generates music recommendations using **Machine Learning**, **Computer Vision**, and **Natural Language Processing (NLP)**.

The application clusters Spotify songs based on their audio features using **Agglomerative Hierarchical Clustering** and redirects users to YouTube for seamless music playback.

---

## 📌 Features

- 😊 Facial Emotion Detection using **FER** and **MTCNN**
- 🎤 Speech Emotion Detection using **Speech Recognition**
- 💬 Text-Based Emotion Detection
- 🎵 AI-Powered Music Recommendation
- 🎧 YouTube Search Integration for Song Playback
- 🔐 Secure User Authentication
- ❤️ Save Favorite Songs
- ➕ Add Custom Songs
- 📂 Personalized User Dashboard
- 📊 Machine Learning-Based Song Clustering
- 📱 Responsive and User-Friendly Interface

---

## 🏗️ Project Architecture

```text
                    User
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
 Face Input      Speech Input     Text Input
      │               │                │
      ▼               ▼                ▼
FER + MTCNN     Speech Recognition  NLP Processing
      │               │                │
      └───────────────┼────────────────┘
                      ▼
             Emotion Detection
                      │
                      ▼
          Emotion-to-Cluster Mapping
                      │
                      ▼
 Agglomerative Hierarchical Clustering
                      │
                      ▼
          Spotify Song Recommendation
                      │
                      ▼
             YouTube Search Redirect
```

---

# 🧠 Machine Learning Workflow

```text
Spotify Dataset
        │
        ▼
Data Cleaning
        │
        ▼
Feature Selection
        │
        ▼
Feature Scaling (StandardScaler)
        │
        ▼
Agglomerative Hierarchical Clustering
        │
        ▼
Emotion Mapping
        │
        ▼
Song Recommendation
```

---

# ⚙️ Tech Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2

## Backend

- Python
- Flask

## Machine Learning

- Agglomerative Hierarchical Clustering
- StandardScaler
- FER (Facial Emotion Recognition)
- MTCNN
- OpenCV

## Database

- SQLite

## Libraries

- Pandas
- NumPy
- Scikit-learn
- OpenCV
- FER
- SpeechRecognition
- SciPy
- Matplotlib
- Werkzeug
- Pickle

---

# 📂 Project Structure

```text
Moodify/
│── app.py
│── requirements.txt
│── database/
│── emotion/
│── recommendation/
│── templates/
│── static/
│── dataset/
│── models/
│── README.md
```

---

# 📊 Dataset

**Dataset Used:** Spotify Audio Features Dataset

### Features Used

- Energy
- Valence
- Tempo
- Danceability
- Loudness

### Data Preprocessing

- Removed missing values
- Removed duplicate records
- Feature selection
- StandardScaler for feature scaling
- Song clustering using Agglomerative Hierarchical Clustering

---

# 🤖 Machine Learning Model

### Algorithm Used

- Agglomerative Hierarchical Clustering

### Linkage Method

- Ward Linkage

### Number of Clusters

- 5

### Why Agglomerative Clustering?

- Works well for unlabeled datasets
- Produces stable clusters
- Generates a dendrogram for visualization
- Groups songs with similar emotional characteristics

---

# 😊 Emotion Detection

### Face Emotion Detection

- FER
- MTCNN
- OpenCV

### Speech Emotion Detection

- SpeechRecognition
- Google Speech-to-Text

### Text Emotion Detection

- Keyword-based NLP

Supported emotions include:

- 😊 Happy
- 😢 Sad
- 😡 Angry
- 😐 Neutral
- 😌 Calm
- 😲 Surprise

---

# 🔐 Authentication

- User Registration
- Secure Login
- Password Hashing
- Session Management
- SQLite Database

---

# 🎵 Recommendation Pipeline

```text
Detected Emotion
        │
        ▼
Emotion Mapping
        │
        ▼
Cluster Selection
        │
        ▼
Recommended Songs
        │
        ▼
YouTube Search Redirect
```

---
