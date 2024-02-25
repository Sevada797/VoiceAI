import os
import requests
import speech_recognition as sr
from gtts import gTTS

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=2)  # Listen for 2 seconds
            try:
                print("Recognizing...")
                query = recognizer.recognize_google(audio)
                #print("User said:", query)
                response = askAI(query)
                speak(response)
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand what you said.")
                #listen()
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                return ""
        except sr.WaitTimeoutError:
            print("No speech detected after 2 seconds.")
            listen()
    

def speak(text):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.energy_threshold = 600  # Adjust this value (default is 300)    
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("ffmpeg -i output.mp3 output.wav -y && aplay output.wav")
    listen()

def askAI(text):
    # URL of the endpoint
    url = 'https://talkai.info/chat/send/'

    # Request headers
    headers = {
        'authority': 'talkai.info',
        'accept': 'application/json, text/event-stream',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'DWUmEg=mEDMSoWJiGtFTYLOjkNfzPrlwKCcga; mEDMSoWJiGtFTYLOjkNfzPrlwKCcga=dfca0557d43262553879028afcd5e2ef-1708864148; _csrf-front=eee0fdefc5c377b0316ea317b9d39f58a9b131dde6e8ef2c0a094022f6ad5cd9a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22_csrf-front%22%3Bi%3A1%3Bs%3A32%3A%22Yz_w-NAJhDbNWl0-9v_L2bAwP1s9HCz7%22%3B%7D; _ym_uid=1708864150873778270; _ym_d=1708864150; fpestid=UfU5kjJEkQVGxVRBBxKtnhJCFTLo1gNwXh7Uqs6tuR2Q3SpbmzpCfPkJMXo3mltEPpH14A; _ym_isad=2; _ga=GA1.1.702753271.1708864153; _ym_visorc=b; __gads=ID=c7ec5acd12a2dd96:T=1708864153:RT=1708864153:S=ALNI_MbcSPxs-2S4mLD31Pjs9vyjmMO3og; __gpi=UID=00000d61ceaf221e:T=1708864153:RT=1708864153:S=ALNI_Mafauu6mQL8I7O1xNDVOKqRtcbwCw; __eoi=ID=780f4f610f439451:T=1708864153:RT=1708864153:S=AA-AfjYVf0wPcQD0peUwqhWlwxZE; DWUmEg_hits=2; FCNEC=%5B%5B%22AKsRol9lMwY_jFC_xhEDkFhIr3Fih9fSMne8BXRLkVyeG4kF2T8aDe9zhoHjhvnpy79cN8SmVMTG30ep3cwtsDSSaVAfPjF2_1Ouo6oZMOJSnXFqhnhAA9M8c_PaD4WJ9LGBcuvKtoFnr9bKw23qaHsNQurZcx7qxA%3D%3D%22%5D%5D; _ga_FB7V9WMN30=GS1.1.1708864152.1.1.1708864341.0.0.0',
        'origin': 'https://talkai.info',
        'referer': 'https://talkai.info/chat/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    # Request data
    data = {
        "type": "chat",
        "messagesHistory": [
            {
                "id": "4afa8651-11a7-4d9d-8014-04f10e53e842",
                "from": "you",
                "content": text
            }
        ]
    }

    # Send the request
    response = requests.post(url, headers=headers, json=data)

    # Print the response
    #print(response.text[0:(response.text.find('event: trylimit'))].replace("data: ", "").replace("\n", ""))
    speak(response.text[0:(response.text.find('event: trylimit'))].replace("data: ", "").replace("\n", ""))
listen()
