import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000
INPUT_DEVICE = 2
CHUNK_DURATION = 3  # seconds


# Load Whisper model
model = WhisperModel(
    "small.en",
    device="cpu",
    compute_type="int8"
)

print("Model loaded!")
print("Speak into the microphone.")


while True:

    print("\nListening...")

    # Record a short chunk
    audio = sd.rec(
        int(CHUNK_DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        device=INPUT_DEVICE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    # Convert from (samples, 1) to (samples,)
    audio = audio.flatten()

    # Transcribe
    segments, info = model.transcribe(
        audio,
        language="en",
        beam_size=1
    )

    text = ""

    for segment in segments:
        text += segment.text

    text = text.strip()

    if text:
        print("TEXT:", text)