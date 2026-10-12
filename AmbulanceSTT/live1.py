import sounddevice as sd
import soundfile as sf
import numpy as np
import queue
import json
import os
from datetime import datetime

from vosk import Model, KaldiRecognizer


SAMPLE_RATE = 16000
INPUT_DEVICE = 2

model = Model("vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

print("Model loaded!")
print("Speak into the microphone.")

audio_queue = queue.Queue()
recorded_audio = []
transcript_lines = []


def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))


try:
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=4000,
        device=INPUT_DEVICE,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        print("Recording...")
        print("Press CTRL+C to stop.")

        while True:
            # Timeout lets Ctrl+C interrupt reliably (especially on Windows)
            try:
                data = audio_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            # Store microphone audio
            recorded_audio.append(data)

            # Vosk
            if recognizer.AcceptWaveform(data):
                text = json.loads(recognizer.Result()).get("text", "")
                if text:
                    print("\rFINAL: " + text + " " * 30)
                    transcript_lines.append(text)
            else:
                text = json.loads(recognizer.PartialResult()).get("partial", "")
                if text:
                    print("\rLIVE: " + text + " " * 30, end="", flush=True)

except KeyboardInterrupt:
    print("\n\nStopping recording...")

# Flush any speech Vosk is still holding
final_text = json.loads(recognizer.FinalResult()).get("text", "")
if final_text:
    print("FINAL:", final_text)
    transcript_lines.append(final_text)

# Nothing recorded -> nothing to save
if not recorded_audio:
    print("No audio recorded.")
    raise SystemExit

# Timestamped names so old files are never overwritten
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
wav_path = os.path.abspath(f"recording_{stamp}.wav")
txt_path = os.path.abspath(f"transcript_{stamp}.txt")

# Convert raw bytes -> int16 numpy array, then save WAV
audio_array = np.frombuffer(b"".join(recorded_audio), dtype=np.int16)
sf.write(wav_path, audio_array, SAMPLE_RATE, subtype="PCM_16")

# Save transcription
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("\n".join(transcript_lines))

print("Number of audio chunks:", len(recorded_audio))
print("Total samples:", len(audio_array))
print("\nRecording saved!")
print("Audio:     ", wav_path)
print("Transcript:", txt_path)