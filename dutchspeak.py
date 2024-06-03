import openai
import elevenlabs as el
import assemblyai as aai
from pydub import AudioSegment
import os

# Set your API keys
openai.api_key = 'sk-proj-jffHwYYYmzOoXNtdo10UT3BlbkFJ0Gs1PFNG1UMkg4WdoihF'
el.api_key = '711e2400a2276b4cf9bedb8edc15a493'
aai.settings.api_key = 'a88e375d7b0d46f5a16bfbb9a8caa49e'

# Function to get a response from ChatGPT
def get_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that speaks Dutch."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0]['message']['content'].strip()

# Function to convert text to speech using ElevenLabs
def text_to_speech(text, save_path=None):
    audio = el.TextToSpeech.synthesize(text=text, voice="your_preferred_voice")  # Adjust this line based on actual ElevenLabs API method
    if save_path:
        with open(save_path, 'wb') as f:
            f.write(audio)  # Save the audio file
    el.TextToSpeech.play(audio)  # Adjust this line based on actual ElevenLabs API method to play audio

# Function to convert speech to text using Assembly AI
def speech_to_text(audio_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    
    if isinstance(transcript, aai.transcriber.Transcript) and transcript.text:
        return transcript.text
    else:
        print("Unexpected transcript format:", type(transcript))
        return None

# Function to process audio input and provide verbal response
def process_audio_input(audio_path):
    # Convert speech to text
    prompt = speech_to_text(audio_path)
    if prompt is None:
        print("Transcription failed.")
        return
    
    print("Transcribed Text:", prompt)
    
    # Get response from ChatGPT
    response = get_response(prompt)
    print("ChatGPT Response:", response)
    
    # Convert response text to speech and save it as a file
    text_to_speech(response, save_path="response_audio.wav")

# Example usage
if __name__ == "__main__":
    # Specify the path to your audio file
    audio_path = r'C:\Users\kabir\OneDrive\Documents\Sound Recordings\leaderofnether.wav'
    
    # Ensure the audio file is in the correct format
    audio = AudioSegment.from_file(audio_path)
    audio.export("converted_audio.wav", format="wav")
    
    # Process the audio input
    process_audio_input("converted_audio.wav")

    # Optionally, delete the converted file if not needed
    os.remove("converted_audio.wav")
