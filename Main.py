import pyttsx3
import speech_recognition as sr
from email_module.send_email import send_email
from email_module.read_emails import read_emails

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer()

def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't get that. Please choose again.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None

def main():
    speak("Welcome to Auditory-Based Email System!")
    
    while True:
        speak("What would you like to do today?")
        speak("Say number 1 to send an email.")
        speak("Say number 2 to read emails.")
        speak("Say number 3 to listen to audio.")
        speak("Say number 4 to exit.")

        while True:
            choice = recognize_speech()
            if choice is None:
                continue  
            elif choice == "number one":
                send_email()
                break
            elif choice == "number two":
                read_emails()
                break
            elif choice == "number three":
                speak("Listening to audio feature is under development.")
                break
            elif choice == "number four":
                speak("Exiting the program. Goodbye!")
                return
            else:
                speak("Sorry, I didn't understand that. Please choose again.")
                continue

if __name__ == "__main__":
    main()
