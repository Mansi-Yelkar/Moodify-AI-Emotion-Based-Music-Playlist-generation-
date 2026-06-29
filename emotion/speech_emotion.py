import speech_recognition as sr
from .text_emotion import get_text_emotion

def get_speech_emotion(audio_file_path):
    """
    Convert audio file to text using SpeechRecognition and then map text to emotion.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized text: {text}")
            return get_text_emotion(text), text
    except sr.UnknownValueError:
        print("SpeechRecognition could not understand audio")
        return "Neutral", ""
    except sr.RequestError as e:
        print(f"Could not request results from SpeechRecognition service; {e}")
        return "Neutral", ""
    except Exception as e:
        print(f"Error in speech processing: {e}")
        return "Neutral", ""
