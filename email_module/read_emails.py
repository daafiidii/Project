import imaplib
import email
from email.header import decode_header
import pyttsx3
import speech_recognition as sr
import os
import webbrowser

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None

def save_attachment(part, download_folder="attachments"):
    if not os.path.isdir(download_folder):
        os.makedirs(download_folder)
    filename = part.get_filename()
    filepath = os.path.join(download_folder, filename)
    with open(filepath, "wb") as f:
        f.write(part.get_payload(decode=True))
    return filepath

def read_emails():
    username = "adeoyed7@gmail.com"
    password = "oolg wyzx xqbv rhnk"
    server = imaplib.IMAP4_SSL("imap.gmail.com")
    server.login(username, password)
    server.select("inbox")

    status, messages = server.search(None, "ALL")
    email_ids = messages[0].split()

    speak("Welcome, your account is logged in. I will read the first 5 recent emails you got.")
    
    for i in range(5):
        email_id = email_ids[-(i+1)]
        status, msg_data = server.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
            
                sender, encoding = decode_header(msg.get("From"))[0]
                if isinstance(sender, bytes):
                    sender = sender.decode(encoding if encoding else "utf-8")
                # Decode email subject
                subject, encoding = decode_header(msg.get("Subject"))[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                speak(f"Email {i+1}. From: {sender}. Subject: {subject}.")
                
                while True:
                    speak("Would you like to open this email? Say 'open email' to open, 'next email' to go to the next email, or 'exit' to leave the system.")
                    user_input = listen()
                    if user_input and user_input.lower() == "open email":
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    speak(part.get_payload(decode=True).decode())
                                elif part.get_content_maintype() == "audio":
                                    filepath = save_attachment(part)
                                    speak(f"Audio attachment {part.get_filename()} has been saved.your receieved audio file will be played now.")
                                    engine.stop()  # Stop any further speech synthesis
                                    webbrowser.open(filepath)
                                    server.logout()
                                    return
                        else:
                            speak(msg.get_payload(decode=True).decode())
                        break
                    elif user_input and user_input.lower() == "next email":
                        break
                    elif user_input and user_input.lower() == "exit":
                        speak("Exiting the email reading process. Goodbye!")
                        server.logout()
                        return
                    else:
                        speak("Sorry, I did not understand that.")
                        continue

    speak("You have reached the end of the recent emails.")
    server.logout()
