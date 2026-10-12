import wave
import json
from vosk import Model, KaldiRecognizer

model = Model("vosk-model-small-en-in-0.4")

audio = wave.open("recording.wav", "rb")

recognizer = KaldiRecognizer(
    model,
    audio.getframerate()
)

while True:
    data = audio.readframes(4000)

    if len(data) == 0:
        break

    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        print(result["text"])

result = json.loads(recognizer.FinalResult())

print("FINAL:")
print(result["text"])