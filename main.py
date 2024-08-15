import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import pywhatkit
from googlesearch import search





# from openai import OpenAI



load_dotenv()
# Load environment variables from .env file


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsApi_key = os.getenv('newsApi')
weatherApi_key = os.getenv('weatherApi')
unsplashApi_key= os.getenv('unsplashApi')
# openApi_key =os.getenv('openApi')




def speak(text):
    engine.say(text)
    engine.runAndWait()

# def aiProcess(command):
#     client = OpenAI(api_key=openApi,
# )

#     completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google cloud"},
#         {"role": "user", "content": command}
#     ]
#     )

#     return(completion.choices[0].message.content)


def searchGoogle(query):
    try:
        # Strip "jarvis" and "google search" if present
        query = query.lower().replace("jarvis", "").replace("google search", "").strip()
        
        # Inform the user that the search is starting
        speak(f"Searching Google for {query}")
        
        # Perform the search and open in the browser
        pywhatkit.search(query)
        
    except Exception as e:
        speak("Sorry, I couldn't perform the search.")
        print("Error:", e)


def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"The current time is {current_time}."

def getWeather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherApi_key}"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "404":
            main = data["main"]
            weather = data["weather"][0]
            temperature = main["temp"]
            humidity = main["humidity"]
            description = weather["description"]

            weather_report = f"The temperature in {city} is {temperature}°C with {description}. Humidity is {humidity}%."
            return weather_report
        else:
            return "City not found."
    except Exception as e:
        return "Unable to fetch weather data at the moment."
    
def searchUnsplash(query):
    try:
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id={unsplashApi_key}"
        response = requests.get(url)
        data = response.json()

        if data["total"] > 0:
            first_image = data["results"][0]
            image_url = first_image["urls"]["regular"]
            webbrowser.open(image_url)    # Open the image URL in the web browser
            
            return f"Showing an image of {query}."
        else:
            return f"No images found for {query}."
    except Exception as e:
        return "Unable to fetch images at the moment."    
    


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com") 
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")   
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")   
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]    
        webbrowser.open(link)

    elif "hello" in c.lower():
        speak("Hello sir, how are you ?")
    elif "i am fine" in c.lower():
        speak("that's great, sir")
    elif "how are you" in c.lower():
        speak("Perfect, sir")
    elif "thank you" in c.lower():
        speak("you are welcome, sir")    

    elif "google" in c.lower():
        searchGoogle(c)
           

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApi_key}")
        if r.status_code == 200:
            # parse the JSON response
            data = r.json()

            # extract the articles
            articles = data.get('articles',[])

            # Print the headlines
            for article in articles:
                speak(article['title']) 

    elif "show me an image of" in c.lower():
        query = c.lower().replace("show me an image of", "").strip()
        message = searchUnsplash(query)
        speak(message)           

    elif "weather" in c.lower():
        city = c.lower().replace("weather in", "").strip()
        weather_report = getWeather(city)
        speak(weather_report)     

    elif "what time is it" in c.lower() or "tell me the time" in c.lower():
        time_info = getCurrentTime()
        speak(time_info)
 
                     
    else:
        # let openAi handle the request  
        # output = aiProcess(c)
        output = "not findable"
        speak(output)
                         

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
        

        # recognize speech using google
        print("recognizing...")
        try:
            with sr.Microphone() as source:
              print("Listening...")
              audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("ya")
                # Listen for command
                with sr.Microphone() as source:
                  print("Jarvis Active...")
                  audio = r.listen(source)
                  command = r.recognize_google(audio)
                  print(f"You Said: {command}\n")

                  processCommand(command)
        
        except Exception as e:
            print("Error; {0}".format(e))

