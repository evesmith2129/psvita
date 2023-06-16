import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")

    else:
        speak("Good Evening Sir!")

    speak("I am Jarvis, How may I help you?")
    
def takeCommand():
    # It takes microphone input from user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"

    return query

if __name__ == "__main__":
    wishMe()
while True:
    query = takeCommand().lower()
    if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

    elif 'open youtube' in query:
            speak("Opening Youtube")
            webbrowser.open("youtube.com")

    elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")


    elif 'open github' in query:
            speak("Opening Github")
            webbrowser.open("github.com")

    elif 'open facebook' in query:
            speak("Opening Facebook")
            webbrowser.open("facebook.com")

    elif 'open instagram' in query:
            speak("Opening Instagram")
            webbrowser.open("instagram.com")

    elif 'open whatsapp' in query:
            speak("Opening Whatsapp")
            webbrowser.open("web.whatsapp.com")

    elif 'open gmail' in query:
            speak("Opening Gmail")
            webbrowser.open("gmail.com")

    elif 'open amazon' in query:
            speak("Opening Amazon")
            webbrowser.open("amazon.in")

    elif 'open flipkart' in query:
            speak("Opening Flipkart")
            webbrowser.open("flipkart.com")

    elif 'open snapdeal' in query:
            speak("Opening Snapdeal")
            webbrowser.open("snapdeal.com")

    elif 'open myntra' in query:
            speak("Opening Myntra")
            webbrowser.open("myntra.com")

    elif 'open ajio' in query:
            speak("Opening Ajio")
            webbrowser.open("ajio.com")

    elif 'open club factory' in query:
            speak("Opening Club Factory")
            webbrowser.open("clubfactory.com")

    elif 'open shein' in query:
            speak("Opening Shein")
            webbrowser.open("shein.in")

    elif 'open olx' in query:
            speak("Opening Olx")
            webbrowser.open("olx.in")

    elif 'open naukri' in query:
            speak("Opening Naukri")
            webbrowser.open("naukri.com")

    elif 'open indeed' in query:
            speak("Opening Indeed")
            webbrowser.open("indeed.co.in")
        
    else: 'exit' in query
    exit()