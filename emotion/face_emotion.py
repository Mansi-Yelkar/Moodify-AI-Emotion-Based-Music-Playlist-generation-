from fer.fer import FER
import cv2
import numpy as np
import base64

def get_face_emotion(image_data, is_base64=True):
    """
    Extract emotion from an image using the FER library.
    image_data: base64 encoded image string or raw numpy array.
    """
    try:
        if is_base64:
            # Decode base64 image
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            img_bytes = base64.b64decode(image_data)
            np_arr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        else:
            img = image_data
            
        detector = FER(mtcnn=True)
        emotion, score = detector.top_emotion(img)
        
        if not emotion:
            return "Neutral" # Fallback
            
        # Map FER output to PRD output
        emotion_map = {
            'happy': 'Happy',
            'sad': 'Sad',
            'angry': 'Angry',
            'surprise': 'Surprised',
            'neutral': 'Neutral',
            'fear': 'Surprised',
            'disgust': 'Angry'
        }
        
        return emotion_map.get(emotion.lower(), 'Neutral')
    except Exception as e:
        print(f"Error in face emotion detection: {e}")
        return "Neutral"
