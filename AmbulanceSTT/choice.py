print("Which program do you want to run?")

while(True):
    print("1. Device List")
    print("2. Sound Testing")
    print("3. STT Whisper model")
    print("4. STT2 Vosk model en-in")
    print("5. STT3 Vosk model en-us")
    print("6. Live transcription Vosk")
    print("7. Live transcription Whisper")
    print("8. Stop program")

    choice = input("Enter your choice: ")

    if choice == "1":
        exec(open("devicelist.py").read())

    elif choice == "2":
        exec(open("sound.py").read())

    elif choice == "3":
        exec(open("stt.py").read())

    elif choice == "4":
        exec(open("stt2.py").read())

    elif choice == "6":
        exec(open("live.py").read())

    elif choice == "7":
        exec(open("live2.py").read())

    elif choice == "8":
        break

    else:
        print("Invalid choice")



