import openai
import pyttsx3
import speech_recognition as sr

# Setting up API key
openai.api_key = "gpt-4-turbo"

# Initialize the text to speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print('Skipping unknown error:', e)

def generate_response(prompt):
    response = openai.Completion.create(
        engine="gpt-4-turbo",
        prompt=prompt,
        max_tokens=10000,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Say 'hello' to start recording")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "hello":
                    # Recording audio
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # Transform audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")
                        
                        # Generating response using GPT-4
                        response = generate_response(text)

                        print(f"GPT says: {response}")

                        speak_text(response)
            except Exception as e:
                print("An error has occurred:", e)

main()
