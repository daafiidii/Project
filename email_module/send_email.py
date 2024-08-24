import pyttsx3
import speech_recognition as sr
import pyaudio
import sounddevice as sd
import soundfile as sf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


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
            speak("Sorry, my speech service is down. Would you like to start again or exit?")
            while True:
                choice = listen()
                if choice:
                    choice = choice.lower().strip()
                    if "start again" in choice:
                        return "start again"
                    elif "exit" in choice:
                        return "exit"
                    else:
                        speak("Sorry, I did not understand that. Please say start again or exit.")
            return None

def spell_out_email():
    while True:
        speak("Welcome to our Send email option, Hope you have a lovely time!Please spell out the recipient's email address, letter by letter.")
        email_username = ""
        while True:
            speak("Say the next letter or say 'done' to finish.")
            response = listen()
            if response:
                response = response.lower().strip()
                if response == 'done':
                    break
                elif response.startswith('letter'):
                    parts = response.split()
                    if len(parts) == 2:
                        letter = parts[1]
                        email_username += letter
                        speak(f"Added {letter}")
                elif response == "start again":
                    return "start again"
                elif response == "exit":
                    return "exit"
        return email_username

def choose_domain():
    speak("Choose the domain. Say 1 for gmail, 2 for yahoo, 3 for outlook, or 4 for icloud.")
    while True:
        domain_choice = listen()
        if domain_choice:
            domains = {
                'one': 'gmail.com',
                'two': 'yahoo.com',
                'three': 'outlook.com',
                'four': 'icloud.com'
            }
            if domain_choice in domains:
                return domains[domain_choice]
            else:
                speak("Sorry, I did not understand that. Please say 1 for gmail, 2 for yahoo, 3 for outlook, or 4 for icloud.")

def record_audio(filename):
    speak("This recording will last 30 seconds. Please speak into the microphone. Recoding starts now.")
    duration = 30  
    fs = 44100  
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  
    sf.write(filename, myrecording, fs)
    speak("Recording complete.")

def send_email():
    sender_email = "adeoyed7@gmail.com"  
    password = "oolg wyzx xqbv rhnk"  

    while True:
        recipient_username = spell_out_email()
        if recipient_username == "start again":
            continue
        elif recipient_username == "exit":
            return

        domain = choose_domain()
        recipient_email = f"{recipient_username}@{domain}"

        speak("What is the subject of your email?")
        subject = listen()
        if subject == "exit":
            return
        
        speak("Do you want to send the message as a text or audio?")
        speak("Say number 1 for text message or number 2 for audio message.")
        message_type = listen()
        
        if "one" in message_type:  
            speak("What is the message?")
            message = listen()
            if message == "exit":
                return

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                server.close()
                speak("Email sent successfully.")
            except Exception as e:
                speak(f"Failed to send email. Error: {str(e)}")
            break

        elif "two" in message_type: 
            filename = "audio_message.wav"
            record_audio(filename)

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Attach the audio file
            attachment = open(filename, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                server.close()
                speak("Email with audio attachment sent successfully.")
            except Exception as e:
                speak(f"Failed to send email. Error: {str(e)}")
            break

        else:
            speak("Sorry, I did not understand that. Please say number 1 for text message or number 2 for audio message.")
            continue

        speak("Say exit to exit or start again.")
        if listen() == "exit":
            return
