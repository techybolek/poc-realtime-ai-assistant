import base64
import pyaudio
import wave
from openai import OpenAI
import threading
import pygame

def record_audio(filename, sample_rate=44100, channels=1, chunk=1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)

    print("Press Enter to start recording...")
    input()
    print("Recording... Press Enter to stop.")

    frames = []
    is_recording = True

    def record():
        while is_recording:
            data = stream.read(chunk)
            frames.append(data)

    record_thread = threading.Thread(target=record)
    record_thread.start()

    input()  # Wait for Enter to stop recording
    is_recording = False
    record_thread.join()

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def encode_audio(filename):
    with open(filename, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode('utf-8')

def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    print("Playing back the recording. Press Enter to stop playback.")
    pygame.mixer.music.play()
    input()  # Wait for Enter to stop playback
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def get_audio(audio_filename):
  while True:
    # Record audio
    record_audio(audio_filename)

    # Play back the recording
    play_audio(audio_filename)
    print("Send?")
    key = input()
    if key == "y":
        break

audio_filename = 'input_audio.wav'
get_audio(audio_filename)
# Encode the audio file
encoded_audio = encode_audio(audio_filename)

# Initialize OpenAI client
client = OpenAI()

# Send request to OpenAI
print("Sending request to OpenAI...")
completion = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {
            "role": "user",
            "content": [
                { 
                    "type": "text",
                    "text": "What is in this recording?"
                },
                {
                    "type": "audio",
                    "audio": {
                        "data": encoded_audio,
                        "format": "wav"
                    }
                }
            ]
        },
    ],
    max_tokens=300
)

print(completion.choices[0].message.content)
