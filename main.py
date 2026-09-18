import speech_recognition as sr
import webbrowser
import pyttsx3
import os
from gtts import gTTS
import pygame
import musicLibrary


# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 



def processCommand(c):
    c_lower = c.lower()

    # 1. Dynamic Website Opening
    if c_lower.startswith("open "):
        # Extract everything after "open "
        site_name = c_lower.replace("open ", "").strip()
        
        # Convert to a valid domain format
        # E.g., "stack overflow" -> "stackoverflow"
        # E.g., "wikipedia dot org" -> "wikipedia.org"
        domain = site_name.replace(" dot ", ".").replace(" ", "")
        
        # Default to .com if no extension was spoken
        if "." not in domain:
            domain += ".com"
            
        url = f"https://www.{domain}"
        
        speak(f"Opening {site_name}")
        webbrowser.open(url)

    elif c_lower.startswith("play"):
        song = c_lower.replace("play ", "").strip()
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak(f"Sorry, I couldn't find the song {song}.")






if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=4)
            word = r.recognize_google(audio)
            print("You said: " + word)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            print("Error; {0}".format(e))