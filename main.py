import speech_recognition as sr
import webbrowser
import pyttsx3
import os
from gtts import gTTS
import pygame
import musicLibrary
import time
import requests
from openai import OpenAI, OpenAIError
from client import client  # Import the Groq OpenAI client from client.py


# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "46339643de9e4361920338456f070113"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    time.sleep(1)  # IMPORTANT (file save hone do)

    pygame.mixer.init()

    try:
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print("Error:", e)

    finally:
        pygame.mixer.music.unload()
        os.remove("temp.mp3")

def aiProcess(command: str) -> str:
    """Processes the command using Groq's free API."""
    if not command.strip():
        return "Please provide a valid command."

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # Fast, highly capable, and free model on Groq
            messages=[
                {
                    "role": "system", 
                    "content": "You are a virtual assistant named Jarvis, skilled in general tasks. Give short, concise responses suitable for speech output."
                },
                {"role": "user", "content": command}
            ],
            max_tokens=100,  # Keep it short for a voice assistant
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except OpenAIError as e:
        print(f"Groq API Error: {e}")
        return "Sorry, I encountered an AI service error."
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return "An unexpected error occurred."

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
        print(f"Opening {url}")
        speak(f"Opening {site_name}")
        webbrowser.open(url)

    #    # 2. Check for play commands
    elif c_lower.startswith("play"):
        song = c_lower.replace("play ", "").strip()
        lower_music = {k.lower(): v for k, v in musicLibrary.music.items()}
        if song in lower_music:
            link = lower_music[song]
            webbrowser.open(link)
            print(f"Playing {song}")
            speak(f"Playing {song}")
        else:
            speak(f"Sorry, I couldn't find the song {song}.")


     # 3. Check for news commands
    elif "news" in c_lower:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                
                if not articles:
                    speak("I couldn't find any news at the moment.")
                    return

                speak("Here are the top headlines.")
                for i, article in enumerate(articles[:3]):
                    speak(f"Headline {i+1}: {article['title']}")
            else:
                speak("Sorry, there was an issue fetching the news.")
        except Exception as e:
            print(f"News error: {e}")
            speak("I encountered an error while fetching the news.")

    # 4. Let OpenAI handle everything else
    else:
        output = aiProcess(c)
        speak(output)
        print(f"Jarvis: {output}")
        







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
                    print(f"Command: {command}")


                    # --- EXIT CONDITION ---
                    if "bye" in command.lower() or "exit" in command.lower() or "stop" in command.lower():
                        speak("Goodbye! Have a nice day.")
                        break  # This breaks the while loop and ends the program

                    processCommand(command)


        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except Exception as e:
            print("Error; {0}".format(e))