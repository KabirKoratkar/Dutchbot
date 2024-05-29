import openai
import requests
import time
from config import OPENAI_API_KEY, ASSEMBLYAI_API_KEY, ELEVENLABS_API_KEY

openai.api_key = OPENAI_API_KEY

def transcribe_audio(file_path):
    headers = {'authorization': ASSEMBLYAI_API_KEY}
    response = requests.post(
        'https://api.assemblyai.com/v2/upload',
        headers=headers,
        files={'file': open(file_path, 'rb')}
    )
    audio_url = response.json()['upload_url']

    transcribe_request = {'audio_url': audio_url}
    response = requests.post(
        'https://api.assemblyai.com/v2/transcript',
        json=transcribe_request,
        headers=headers
    )
    transcript_id = response.json()['id']

    while True:
        response = requests.get(
            f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
            headers=headers
        )
        result = response.json()
        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'failed':
            raise Exception('Transcription failed')
        time.sleep(1)

def generate_response(prompt, language='nl'):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.9
    )
    message = response.choices[0].text.strip()
    return message

def text_to_speech(text, language='nl'):
    headers = {
        'xi-api-key': ELEVENLABS_API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.75, "similarity_boost": 0.75},
        "voice": "Dutch Voice Name"  # Use the appropriate voice name from Eleven Labs
    }
    response = requests.post(
        'https://api.elevenlabs.io/v1/text-to-speech',
        headers=headers,
        json=payload
    )
    audio_content = response.content
    with open('response.mp3', 'wb') as audio_file:
        audio_file.write(audio_content)
    return 'response.mp3'

def chatbot(audio_input_path):
    try:
        start_time = time.time()
        
        # Convert speech to text
        user_input = transcribe_audio(audio_input_path)
        print(f"User said: {user_input}")

        # Generate response
        response_text = generate_response(user_input)
        print(f"Chatbot responds: {response_text}")

        # Convert text to speech
        response_audio_path = text_to_speech(response_text)
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"Response generated in {duration:.2f} seconds")

        return response_audio_path

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    audio_path = 'path_to_your_audio_file.wav'  # Provide the path to an audio file
    response_audio = chatbot(audio_path)
    if response_audio:
        print(f"Response audio saved at: {response_audio}")
