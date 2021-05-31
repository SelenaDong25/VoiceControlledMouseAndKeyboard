import speech_recognition as sr
import pyautogui as pg
import capstone
import time


# obtain the audio file (*.wav) as the audio source 
from os import path
AUDIO_FILE1 = path.join(path.dirname(path.realpath(__file__)), "..\AudioFile-part1.wav")
AUDIO_FILE2 = path.join(path.dirname(path.realpath(__file__)), "..\AudioFile-part2.wav")

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE1) as source1:
    audio1 = r.record(source1)  # read part1 audio file
with sr.AudioFile(AUDIO_FILE2) as source2:
    audio2 = r.record(source2)  # read part2 audio file

audio_command1 = r.recognize_google(audio1).lower()
audio_command2 = r.recognize_google(audio2).lower()
audio_command = audio_command1 + " " + audio_command2


# use the audio file as the audio source
# remove special characters which are captured by Speech Recognition
# r = sr.Recognizer()
# with sr.AudioFile(AUDIO_FILE) as source:
#     audio = r.record(source)  # read the entire audio file
    
# audio_command = r.recognize_google(audio).lower()
audio_command = audio_command.replace("-", " ")
audio_command = audio_command.replace("/", " ")
audio_command = audio_command.replace("\\", " ")
audio_command = audio_command.replace(" 00", " 0 0")
audio_command = audio_command.replace("moved", "move")
audio_command = audio_command.replace("process", "press s")
audio_command = audio_command.split() # split string block to individual words

#print(audio_command)

# create an empty list
# use "mouse" and "keyboard" as keywords to create a list of command

command_list = []
s = ""
for word in audio_command:
    if word == "mouse" or word == "keyboard":
        if s != "":
            command_list.append(s)
        s = word
    else:
        s += " " + word
if s != "":
    command_list.append(s)

# run command and giving duration 3s bwteen each command
for command in command_list:
    capstone.run_command(command)
    time.sleep(5)



