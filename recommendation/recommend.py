import pandas as pd
import os

def load_data():
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'clustered_data.csv')
    return pd.read_csv(data_path)

def map_emotion_to_cluster(emotion):
    """
    Map emotion to cluster ID based on the model characteristics.
    """
    # 0: Neutral (Moderate energy/valence)
    # 1: Calm (Low energy, moderate valence)
    # 2: Angry/Surprised (High energy, high tempo)
    # 3: Sad (Low energy, low valence)
    # 4: Happy (High energy, high valence)

    mapping = {
        'Happy': 4,
        'Sad': 3,
        'Angry': 2,
        'Surprised': 2,
        'Calm': 1,
        'Neutral': 0
    }
    
    return mapping.get(emotion, 0)

def recommend_songs(emotion, n=10):
    """
    Recommend N songs based on the emotion.
    """
    df = load_data()
    cluster_id = map_emotion_to_cluster(emotion)
    
    cluster_songs = df[df['cluster'] == cluster_id]
    
    if len(cluster_songs) < n:
        n = len(cluster_songs)
        
    recommended = cluster_songs.sample(n=n, random_state=None)
    
    results = []
    for _, row in recommended.iterrows():
        track_name = row.get('track_name', 'Unknown Track')
        artist_name = row.get('artist_name', 'Unknown Artist')
        youtube_query = f"{track_name} {artist_name} audio"
        results.append({
            'track_name': track_name,
            'artist_name': artist_name,
            'youtube_query': youtube_query,
            'cluster': int(row['cluster'])
        })
        
    return results
