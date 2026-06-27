import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import time
import smtplib
from email.message import EmailMessage

engine = pyttsx3.init()
voices = engine.getProperty('voices')       # getting details of current voice
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def command():
    content = " "
    while content == " ":
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
           print("Say something!")
           r.adjust_for_ambient_noise(source, duration=1)
           print("Listening...")
           audio = r.listen(source, timeout=6, phrase_time_limit=6)
        try:
           content =  r.recognize_google(audio, language='en-Ur')
        except:
           try:
              content = r.recognize_google(audio, language='en-Ur')              
           except Exception as e:
              print("Voice not recognized!")
              speak("I could not understand. Please type your command.")
              content = input("Type your command here: ")
        print("You said................ =  " + content)
    return content

def main_process():
    
        request = command().lower().strip()
        if "hello" in request:
            speak("Wellcome, How can i help you.")

        elif "say time" in request: 
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("current time is " + str(now_time))
        
        elif "say date" in request: 
            now_time = datetime.datetime.now().strftime("%d:%m")
            speak("current date is " + str(now_time))
        
        elif "new task" in request:
            task = request.replace("new task" , "").strip()
            if task != "":
                with open ("todo.txt", "a") as file:
                    file.write(task + "\n")
                print("Task added:", task)
                speak("Task added successfully")
        
        elif "show task" in request:
            with open ("todo.txt", "r") as file:
                tasks = file.read()
            print(tasks)
            speak("Work we have to do is : ")
            speak(tasks)
        
        elif "show work" in request:
            with open ("todo.txt", "r") as file:
                tasks = file.read()
            notification.notify(
                title = "Today's work",
                message = tasks
            )

        elif "open" in request:
            query = request.replace("open","")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")

        elif "wikipedia" in request:
            request = request.replace("jarvis","")
            request = request.replace("wikipedia ","").strip()
            result = wikipedia.summary(request, sentences=2)
            speak(result)
            print(result)
                    
        elif "youtube" in request:
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            search_query = request.replace("youtube", "").strip()
            # agar sirf youtube bola ho
            if search_query == "":
                webbrowser.get(chrome_path).open("https://www.youtube.com")
            # warna search karo
            else:
                url = f"https://www.youtube.com/results?search_query={search_query}"
                print("Opening:", url)
                webbrowser.get(chrome_path).open(url)

        elif "chat" in request and "gpt" in request:
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            # chatgpt word remove
            question = request.replace("chat", "")
            question = question.replace("gpt", "")
            question = question.strip()
            speak("Opening ChatGPT")
            webbrowser.get(chrome_path).open("https://chatgpt.com")
            # page load wait
            time.sleep(8)
            # browser focus
            pyautogui.click(500, 50)
            time.sleep(2)
            # input box click
            pyautogui.click(760,420)
            time.sleep(1)
            # agar question diya hua ho
            if question != "":
                speak("Sending your question")
                pyautogui.write(question)
                time.sleep(2)
                pyautogui.press("enter")
            else:
                speak("What do you want to ask")
                question = command()
                pyautogui.write(question, interval=0.05)
                pyautogui.press("enter") 
                
        elif "google" in request:
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            # google word remove
            search_query = request.replace("google", "")
            search_query = search_query.strip()
            speak("Opening Google")
            if search_query != "":
                url = "https://www.google.com/search?q=" + search_query
                webbrowser.get(chrome_path).open(url)
            else:
                webbrowser.get(chrome_path).open("https://www.google.com")
                speak("What do you want to search")
                search_query = command()
                url = "https://www.google.com/search?q=" + search_query
                webbrowser.get(chrome_path).open(url)
                
        elif "whatsapp" in request or "whatsaap" in request:
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            speak("Enter phone number with country code")
            number = input("Enter number: ")
            speak("Enter your message")
            message = input("Enter message: ")
            speak("Enter hour in 24 hour format")
            hour = int(input("Enter hour: "))
            speak("Enter minute")
            minute = int(input("Enter minute: "))
            message = message.replace(" ", "%20")
            url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
            speak("Opening WhatsApp")
            webbrowser.get(chrome_path).open(url)
            time.sleep(20)
            now = datetime.datetime.now()
            target_time = now.replace(hour=hour, minute=minute, second=0)
            if target_time < now:
                target_time += datetime.timedelta(days=1)
            wait_seconds = (target_time - now).total_seconds()
            print("Waiting for", wait_seconds, "seconds")
            time.sleep(wait_seconds)
            pyautogui.press("enter")
            speak("Message sent successfully")
            
        elif "email" in request or "send mail" in request:
            try:
                speak("Enter receiver email address")
                receiver_email = input("Receiver Email: ")
                speak("Enter subject")
                subject = input("Subject: ")
                speak("Enter your message")
                body = input("Message: ")
                sender_email = "yourgmail@gmail.com"
                sender_password = "your_app_password"
                msg = EmailMessage()
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = receiver_email
                msg.set_content(body)
                speak("Sending email")
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(sender_email, sender_password)
                    smtp.send_message(msg)
                print("Email sent successfully")
                speak("Email sent successfully")
            except Exception as e:
                print("Error:", e)
                speak("Unable to send email")
                                
while True:
    main_process()
