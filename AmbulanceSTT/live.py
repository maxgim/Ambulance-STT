import sounddevice as sd
import queue
import json

from vosk import Model, KaldiRecognizer


SAMPLE_RATE = 16000
INPUT_DEVICE = 2


model = Model("vosk-model-small-en-in-0.4")  # en-us model also installed

print("Model loaded!")
print("Speak into the microphone.")

audio_queue = queue.Queue()

def callback(indata, frames, time, status):

    if status:
        print(status)

    audio_queue.put(bytes(indata))


recognizer = KaldiRecognizer(model, SAMPLE_RATE)


# microphone
with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=4000,
    device=INPUT_DEVICE,
    dtype="int16",
    channels=1,
    callback=callback
):

    while True:

        data = audio_queue.get()

        # auto pharse complete
        if recognizer.AcceptWaveform(data):

            result = json.loads(recognizer.Result())

            text = result.get("text", "")

            if text:
                print("\nFINAL:", text)

        # Still speaking
        else:

            partial = json.loads(recognizer.PartialResult())

            text = partial.get("partial", "")

            if text:
                print("\rLIVE: " + text, end="")