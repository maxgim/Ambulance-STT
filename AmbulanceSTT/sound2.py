import sounddevice as sd
import soundfile as sf

sample_rate = 44100
channels = 1

print("Recording... Press Ctrl+C to stop.")

try:
    with sf.SoundFile(
        "recording.wav",
        mode="w",
        samplerate=sample_rate,
        channels=channels,
        subtype="PCM_16"
    ) as file:

        with sd.InputStream(
            device= 2,
            samplerate=sample_rate,
            channels=channels,
            callback=lambda indata, frames, time, status: file.write(indata)
        ):
            while True:
                sd.sleep(1000)

except KeyboardInterrupt:
    print("\nRecording stopped.")
    print("Saved as recording.wav")