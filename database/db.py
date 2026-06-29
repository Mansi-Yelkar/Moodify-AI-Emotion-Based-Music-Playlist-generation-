import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS liked_songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                track_name TEXT NOT NULL,
                artist_name TEXT NOT NULL,
                youtube_query TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                playlist_name TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS added_songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                track_name TEXT NOT NULL,
                artist_name TEXT NOT NULL,
                youtube_query TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    conn.close()

def register_user(username, password):
    conn = get_db()
    hashed = generate_password_hash(password)
    try:
        with conn:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        return dict(user)
    return None

def like_song(user_id, track_name, artist_name, youtube_query):
    conn = get_db()
    with conn:
        conn.execute('''
            INSERT INTO liked_songs (user_id, track_name, artist_name, youtube_query)
            VALUES (?, ?, ?, ?)
        ''', (user_id, track_name, artist_name, youtube_query))
    conn.close()

def get_liked_songs(user_id):
    conn = get_db()
    songs = conn.execute('SELECT * FROM liked_songs WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return [dict(s) for s in songs]

def add_song(user_id, track_name, artist_name, youtube_query):
    conn = get_db()
    with conn:
        conn.execute('''
            INSERT INTO added_songs (user_id, track_name, artist_name, youtube_query)
            VALUES (?, ?, ?, ?)
        ''', (user_id, track_name, artist_name, youtube_query))
    conn.close()

def get_added_songs(user_id):
    conn = get_db()
    songs = conn.execute('SELECT * FROM added_songs WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return [dict(s) for s in songs]

def remove_liked_song(user_id, song_id):
    conn = get_db()
    with conn:
        conn.execute('DELETE FROM liked_songs WHERE user_id = ? AND id = ?', (user_id, song_id))
    conn.close()

def remove_added_song(user_id, song_id):
    conn = get_db()
    with conn:
        conn.execute('DELETE FROM added_songs WHERE user_id = ? AND id = ?', (user_id, song_id))
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
