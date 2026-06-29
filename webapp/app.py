from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sys
import os
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import db
from emotion.face_emotion import get_face_emotion
from emotion.speech_emotion import get_speech_emotion
from emotion.text_emotion import get_text_emotion
from recommendation.recommend import recommend_songs

app = Flask(__name__)
app.secret_key = 'super_secret_moodify_key'

db.init_db()

@app.before_request
def check_guest_sessions():
    if 'user_id' not in session:
        if 'guest_sessions' not in session:
            session['guest_sessions'] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login or register to access the dashboard.', 'error')
        return redirect(url_for('auth'))
    
    user_id = session['user_id']
    liked_songs = db.get_liked_songs(user_id)
    added_songs = db.get_added_songs(user_id)
    return render_template('dashboard.html', liked_songs=liked_songs, added_songs=added_songs)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if action == 'register':
            if db.register_user(username, password):
                flash('Registration successful! Please login.', 'success')
            else:
                flash('Username already exists.', 'error')
        elif action == 'login':
            user = db.authenticate_user(username, password)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials.', 'error')
    
    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/api/emotion/face', methods=['POST'])
def emotion_face():
    if not can_use_session(): return jsonify({'error': 'Guest session limit reached'}), 403
    
    data = request.json
    image_data = data.get('image')
    if not image_data:
        return jsonify({'error': 'No image provided'}), 400
        
    emotion = get_face_emotion(image_data)
    increment_guest_session()
    return jsonify({'emotion': emotion})

@app.route('/api/emotion/audio', methods=['POST'])
def emotion_audio():
    if not can_use_session(): return jsonify({'error': 'Guest session limit reached'}), 403
    
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
        
    audio_file = request.files['audio']
    
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'temp_audio.wav')
    audio_file.save(temp_path)
    
    emotion, text = get_speech_emotion(temp_path)
    increment_guest_session()
    return jsonify({'emotion': emotion, 'text': text})

@app.route('/api/emotion/text', methods=['POST'])
def emotion_text():
    if not can_use_session(): return jsonify({'error': 'Guest session limit reached'}), 403
    
    data = request.json
    text = data.get('text', '')
    emotion = get_text_emotion(text)
    increment_guest_session()
    return jsonify({'emotion': emotion})

@app.route('/playlist')
def playlist():
    emotion = request.args.get('emotion', 'Neutral')
    songs = recommend_songs(emotion)
    return render_template('playlist.html', emotion=emotion, songs=songs)

@app.route('/api/like_song', methods=['POST'])
def like_song():
    if 'user_id' not in session:
        return jsonify({'error': 'Must be logged in to like songs'}), 401
        
    data = request.json
    db.like_song(
        session['user_id'], 
        data.get('track_name'), 
        data.get('artist_name'), 
        data.get('youtube_query')
    )
    return jsonify({'success': True})

@app.route('/api/add_song', methods=['POST'])
def add_song():
    if 'user_id' not in session:
        return jsonify({'error': 'Must be logged in to add songs'}), 401
        
    data = request.json
    track_name = data.get('track_name')
    artist_name = data.get('artist_name')
    youtube_query = data.get('youtube_query')
    
    if not track_name or not artist_name:
        return jsonify({'error': 'Track name and artist name are required'}), 400
        
    if not youtube_query:
        youtube_query = f"{track_name} {artist_name}"
        
    db.add_song(
        session['user_id'],
        track_name,
        artist_name,
        youtube_query
    )
    return jsonify({'success': True})

@app.route('/api/remove_liked_song', methods=['POST'])
def remove_liked_song():
    if 'user_id' not in session:
        return jsonify({'error': 'Must be logged in'}), 401
        
    data = request.json
    song_id = data.get('song_id')
    if not song_id:
        return jsonify({'error': 'No song ID provided'}), 400
        
    db.remove_liked_song(session['user_id'], song_id)
    return jsonify({'success': True})

@app.route('/api/remove_added_song', methods=['POST'])
def remove_added_song():
    if 'user_id' not in session:
        return jsonify({'error': 'Must be logged in'}), 401
        
    data = request.json
    song_id = data.get('song_id')
    if not song_id:
        return jsonify({'error': 'No song ID provided'}), 400
        
    db.remove_added_song(session['user_id'], song_id)
    return jsonify({'success': True})

def can_use_session():
    if 'user_id' in session:
        return True
    return session.get('guest_sessions', 0) < 5

def increment_guest_session():
    if 'user_id' not in session:
        session['guest_sessions'] = session.get('guest_sessions', 0) + 1

if __name__ == '__main__':
    app.run(debug=True, port=5000)
