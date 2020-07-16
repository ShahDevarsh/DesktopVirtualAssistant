import pyttsx3         
import datetime
import wikipedia
import webbrowser as wb
import os
import pywhatkit as kit
import smtplib
import urllib.request
import urllib.parse
import re
import googlesearch
from googlesearch import search
import speech_recognition as sr
from googleapiclient.discovery import build

#dictionary of mails 
emails = {"vishal":"vishalgautamcsl@gmail.com","devarsh":"shahdevarsh2019@gmail.com","rishabh":"rishabhkumar405@gmail.com","suryansh":"rathoresuryansh196@gmail.com"}

#To open stuffs in chrome
chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
wb.register('chrome', None,wb.BackgroundBrowser(chrome_path))
api_key = 'AIzaSyA8jJ1dW_EKq_y4qTMsFX_gfZpxEwkuVNw' #youtube api key

#for voice you can choose either male or female as you wish
engine = pyttsx3.init('sapi5') 
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):

    """ Voice which is speaking is due to this function """
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wishme():

    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour <12:
        speak("Good Morning Sir\n")
    elif hour>=12 and hour<=18:
        speak("Good Afternoon Sir\n")
    else:
        speak("Good Evening Sir\n")

    speak("I am Jarvis. Please tell me How may i Help you?\n")

def takeCommand():

    """ It takes voice input from user and returns string value """
    user = sr.Recognizer()
    
    with sr.Microphone() as src:
        print("Listening...")
        user.pause_threshold = 1
        audio = user.listen(src)
    try :
        print("Recognizing...")
        query =  user.recognize_google(audio, language='en-in')
        print(f"User said : {query}\n")  
    
    except Exception as e:
        print(e)
        print("Please say that again...\n")
        return "None"
    return query 

def sendEmail(to,content):

    """To send mail implemented using smtp library"""
    server = smtplib.SMTP('smtp.gmail.com', 587)  #stmp library to send mails
    server.ehlo()
    server.starttls()
    textfile = open("file.txt")
    password = textfile.read()
    textfile.close()
    server.login('u17co049@coed.svnit.ac.in', password)
    server.sendmail('u17co049@coed.svnit.ac.in',to,content)
    server.close()

def goto(linenum):
    global line
    line = linenum

 
if __name__ == "__main__":
    
    wishme()
    
    while True:       #continue until user don't say quit

        query = takeCommand().lower()

        if 'wikipedia' in query:

            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:

            speak('\n Sure can you provide the details what you want to search')
            user_string = takeCommand()
            youtube = build(serviceName = 'youtube',version = 'v3',developerKey = api_key)
            
            jsonData = youtube.search().list(
                part = 'snippet',
                q = user_string,
                type = 'video',
                order = 'viewCount'
            )

            response = jsonData.execute()
            secret = ""

            for item in response['items']:
                secret = item['id']['videoId']
                break
            
            speak("Here\'s your request sir")

            wb.get('chrome').open_new_tab('http://www.youtube.com/watch?v=' + secret)

        elif 'open google' in query:

            speak('What do you want me to search sir?')
            string = takeCommand()
            url = "https://www.google.co.in/search?q=" + string + "&oq="+ string +"&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
            speak('Opening your request sir')
            wb.get('chrome').open(url)

        elif 'play music' in query:

            music_dir = 'C:\\Users\\Devarsh\\Music\\Favourites'
            songs = os.listdir(music_dir)
            speak('Playing from your favourite songs')
            for item in songs:
                os.startfile(os.path.join(music_dir, item))
        
        elif 'time' in query:

            currTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(currTime)
            speak(f"Current Time is {currTime}")


        
        elif 'email' in query:

            try:
                speak("Whom do you want to send the email?")
                to = takeCommand()
                to = to.lower()
                present = ""
                if to in emails:
                    present = emails[to]
                if present == "":
                    speak("Sorry such name is not in the list")
                    break
                speak("What should I say?")
                content = takeCommand()
                sendEmail(present,content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry some error occured")
        
        elif 'open whatsapp' in query:

            speak('What message would you like to send')
            msg = takeCommand()
            countrycode = "+"
            speak('Please provide the country code you want to send message')
            countrycode = countrycode + str(takeCommand())
            speak('Please provide the user number you want to send the message')
            num = takeCommand()
            num.replace(" ","")
            num = countrycode + num

            speak('please provide according to 24 hr format at what hour you want to send the message')
            hrs = takeCommand()
            speak('please provide at what minute you want to send the message')
            mins = takeCommand()
            
            hrs.replace(" ","")
            mins.replace(" ","")
            
            if len(hrs) == 1:
                hrs = '0' + hrs
            if len(mins) == 1:
                mins = '0' + mins

            hr = int(hrs)
            mi = int(mins)

            speak('Okay, sending the message ' + 'at ' + str(hr) + ':' + str(mi))
            kit.sendwhatmsg(num,msg,hr,mi)

        elif 'quit' in query:
            speak('Okay Sir have a good day')
            break