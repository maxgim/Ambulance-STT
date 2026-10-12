from faster_whisper import WhisperModel

model = WhisperModel(
    "small.en",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe("recording.wav")

for segment in segments:
    print(segment.text)