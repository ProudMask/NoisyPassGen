import sounddevice as sd
import numpy as np
import string

def generate_password_from_noise():
    # Set the duration for recording ambient noise (in seconds)
    duration = 5

    # Record ambient noise
    print("Recording ambient noise. Please stay silent for a few seconds.")
    noise = sd.rec(int(duration * 44100), samplerate=44100, channels=1, dtype=np.int16)
    sd.wait()

    # Convert the noise to a string of characters
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(characters[i % len(characters)] for i in noise.flatten())

    return password

# Example: Generate a password from ambient noise
ambient_password = generate_password_from_noise()
print("Your password generated from ambient noise:", ambient_password)
