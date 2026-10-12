import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel

fs = 16000  # 16000 Hz or 16khz
duration = 30

print(sd.query_devices())
sd.default.device = [2, 5]  # input and output device
print(sd.default.device)
print("Recording...")

audio = sd.rec(
    int(duration * fs),
    samplerate=fs,
    channels=1,
    dtype="float32"
)

sd.wait()

sf.write("recording.wav", audio, fs)

print("Playing recording...")
audio, fs = sf.read("recording.wav")

sd.play(audio, fs)
sd.wait()

print("Finished!")