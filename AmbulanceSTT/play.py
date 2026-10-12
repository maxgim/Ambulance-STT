import sounddevice as sd
import soundfile as sf

filename = "recording.wav"

output_device = 5

data, sample_rate = sf.read(filename)

print("Playing recording...")
print("Press Ctrl+C to stop.")

try:
    sd.play(data, sample_rate, device=output_device)
    sd.wait()

except KeyboardInterrupt:
    sd.stop()
    print("\nPlayback stopped.")