import re

def get_text_emotion(text):
    """
    Map text to emotion using keyword-based analysis.
    """
    text = text.lower()
    
    keywords = {
        'Happy': ['happy', 'joy', 'excited', 'wonderful', 'amazing', 'great', 'good', 'love', 'fantastic', 'awesome', 'party', 'fun'],
        'Sad': ['sad', 'depressed', 'down', 'crying', 'unhappy', 'tears', 'heartbreak', 'lonely', 'sorrow', 'miss', 'gloomy'],
        'Angry': ['angry', 'mad', 'furious', 'hate', 'rage', 'annoyed', 'irritated', 'frustrated', 'terrible', 'awful'],
        'Surprised': ['wow', 'omg', 'surprised', 'shocked', 'unexpected', 'unbelievable', 'crazy'],
        'Calm': ['calm', 'peaceful', 'relax', 'chill', 'soothing', 'quiet', 'breeze', 'serene', 'sleep', 'tired']
    }
    
    emotion_scores = {e: 0 for e in keywords}
    
    words = re.findall(r'\w+', text)
    for word in words:
        for emotion, kw_list in keywords.items():
            if word in kw_list:
                emotion_scores[emotion] += 1
                
    # Get emotion with max score
    max_emotion = max(emotion_scores, key=emotion_scores.get)
    
    # If no keywords found or tie at 0, return Neutral
    if emotion_scores[max_emotion] == 0:
        return 'Neutral'
        
    return max_emotion
