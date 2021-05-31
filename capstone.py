"""
Control the Mouse and Keyboard using voice commands
"""

import speech_recognition as sr
import pyautogui as pag
from typing import Dict, List
# mouse command keyword dictionary
COMMAND_MOUSE = {"move": pag.moveTo, "click": pag.click,
                "double": pag.doubleClick, "hold": pag.mouseDown,
                "release": pag.mouseUp, "scroll": pag.scroll}
# keyboard command keyword dictionary
COMMAND_KEY = {"hold": pag.keyDown, "release": pag.keyUp, "press": pag.press,
                "shortcut": pag.hotkey, "type": pag.typewrite}

KEYBOARD_KEYS = {'\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
                     ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
                     '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
                     'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                     'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                     'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                     'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                     'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                     'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                     'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                     'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                     'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                     'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                     'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                     'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                     'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                     'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                     'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                     'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                     'command', 'option', 'optionleft', 'optionright'}


DURATION = 1
INTERVAL = 0.05

# function to capture the speech from microphone
def read_mic_input(r: sr.Recognizer, mic: sr.Microphone) -> Dict:
    with mic as source:
        # adjust the recognizer sensitivity to account for ambient noise
        r.adjust_for_ambient_noise(source, duration=0.3)
        # Record voice input from microhpone
        audio = r.listen(source)

    transcription = ""
    error = ""
    # Attempt to recognize speech in the recording
    try:
        transcription = r.recognize_google(audio).lower()

        # clean up the transcription of coordinates and measurements
        transcription = transcription.replace("-", " ")
        transcription = transcription.replace("/", " ")
        transcription = transcription.replace("\\", " ")
        transcription = transcription.replace(" 00", " 0 0")

    except sr.RequestError:
        error = "Error occurred with the API request."
    except sr.UnknownValueError:
        error = "Unable to recognize speech."

    return [transcription, error]

# command abstract class
class Command:
    def __init__(self, parsed):
        self.parsed = parsed

    def execute(self) -> None:
        return

# Mouse command inherit from command class. 
# Mouse command include mouse move up/down/left/right; mouse move to; mouse left/right/double click; 
#                       mouse scroll up/down; mouse hold/release.
class Mouse(Command):
    def __init__(self, parsed):
        super().__init__(parsed)
        
    def move_relative(self, dir, dist) -> None:
        print(dir)
        if dir == "up":
            pag.moveRel(0, -dist, duration=DURATION)
        elif dir == "down":
            pag.moveRel(0, dist, duration=DURATION)
        elif dir == "left":
            pag.moveRel(-1*dist, 0, duration=DURATION)
        elif dir == "right":
            pag.moveRel(dist, 0, duration=DURATION)
        else:
            throw("invalid direction")
    
    def execute(self) -> bool:
        x,y = pag.position()
        parsed = self.parsed
        action = parsed[0]
        if not all([x.isnumeric() for x in parsed[2:]]):
            return False
        if len(parsed) == 4 and parsed[0] == "move" and parsed[1] == "to":
            COMMAND_MOUSE[action](int(parsed[2]), int(parsed[3]), duration=DURATION)
        elif parsed[0] == "move" and len(parsed) == 3:
            try:
                self.move_relative(parsed[1], int(parsed[2]))
            except:
                return False
        elif parsed[0] == "double" and len(parsed) == 2:
            COMMAND_MOUSE[action](x, y)
        elif parsed[1] == "click" and len(parsed) == 2:
            COMMAND_MOUSE[parsed[1]](x, y, button=parsed[0])
        elif (parsed[0] == "hold" or parsed[0] == "release") and len(parsed) == 2:
            COMMAND_MOUSE[action](x, y, parsed[1])
        elif parsed[0] == "scroll" and len(parsed) == 3:
            if parsed[1] == "up":
                COMMAND_MOUSE[action](int(parsed[2]))
            else:
                COMMAND_MOUSE[action](-int(parsed[2]))
        else:
            return False
        return True

# keyboard command inherit from command class.
# Keyboard command include keyboard type key; keyboard hold/release/press key; keyboard shortcut; quit program.
class Keyboard(Command):
    def __init__(self, parsed):
        super().__init__(parsed)
    
    def shortcut(self, keys) -> None:
        for k in keys:
            pag.keyDown(k)
        keys.reverse()
        for k in keys:
            pag.keyUp(k)
        
    def execute(self) -> bool:
        parsed = self.parsed
        action = parsed[0]
        if parsed[0] == "type" and len(parsed) > 2:
            COMMAND_KEY[action](" ".join(parsed[2:]), interval=INTERVAL)
        elif parsed[1] == "shortcut" and len(parsed) > 2 and all([key in KEYBOARD_KEYS for key in parsed[2:]]):
            self.shortcut(parsed[2:])
        elif parsed[0] in COMMAND_KEY.keys() and len(parsed) == 2 and parsed[1] in KEYBOARD_KEYS:
            COMMAND_KEY[action](parsed[1])
        else:
            return False
        return True

def correct_key_names(keys: List[str]) -> List[str]:
    """
    Return a List of strings containing the key name with keys converted to proper format
    which can be used by pyautogui functions.
    """
    
    joined = " ".join(keys)
    print(joined)
    joined = joined.replace('control', 'ctrl')
    joined = joined.replace("page down", "pagedown")
    joined = joined.replace("page up", "pageup")
    joined = joined.replace("volume down", "volumedown")
    joined = joined.replace("volume up", "volumeup")
    joined = joined.replace("page down", "pagedown")
    joined = joined.replace("print screen", "printscreen")
   
    return joined.split()

    if parsed[0] == "quit" and parsed[1] == "program":
        print("You said: quit program. Now quitting...")
        COMMANDS["quit program"][0]()

def run_command(transcription):
    if transcription:
        transcript = correct_key_names(transcription.split())
            
        if transcript[0] == "quit" and transcript[1] == "program":
            return False

        if len(transcript) < 3:
            print("{} is an invalid command. Please try another one!".format(transcription))
            return True
            
        command_type = transcript[0]
        parsed = transcript[1:]
        if command_type == "mouse":
            command = Mouse(parsed)
        else:
            command = Keyboard(parsed)

        success = command.execute()

        if success:
            print("You said: {}. Executing command...".format(transcription))
        else:
            print("{} is an invalid command. Please try another one!".format(transcription))
        
        return True

if __name__ == '__main__':
    pag.FAILSAFE = False

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        print("Please say a voice command!")
        command = read_mic_input(recognizer, microphone)
        transcription = command[0]
        error = command[1]
        if error != "":
            print(error)
            continue

        if error:
            print("{} Please say that again.".format(error))
            continue

        if run_command(transcription) == False:
            break
        