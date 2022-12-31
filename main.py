from colorama import Fore, Style, init, Back
import os
import pyperclip
import sounddevice as sd
import soundfile as sf
import threading
import time
import tkinter as tk
h1, h2, h3 = "f2", "f8", "f9"

window = tk.Tk()
window.title("Save copy v0.1")
window.geometry("420x100")

window.resizable(False, False)
window.iconbitmap("files/icon.ico")

canvas = tk.Canvas(window, width=50, height=50)
canvas.create_oval(10, 10, 40, 40, fill="red", tags=("oval",))
canvas.pack(side="left")

switch_value = tk.IntVar()
switch = tk.Checkbutton(window, text="On/Off",  variable=switch_value)
switch.pack(side="left")

rswitch_value = tk.IntVar()
rswitch = tk.Checkbutton(window, text="Reverse", variable=rswitch_value)
rswitch.pack(side="left")
up=0
def start_calibration():
    global up
    if up == 1:
        up=0
        calibration_button.configure(bg='white')
        sound("canceld")
    else:
        canvas.itemconfigure(canvas.find_withtag("oval"), fill="cyan")
        sound('calibration')
        up=1
        calibration_button.configure(bg='#00BFFF')
        pyperclip.copy("")
calibration_button = tk.Button(window, text="Calibrate", command=start_calibration)
calibration_button.pack(side="left", padx=10)
calibration_button.configure(bg='white')

def clear():
    os.system('cls')

clear_button = tk.Button(window, text="Clear log", command=clear)
clear_button.pack(side="left", padx=10)
clear_button.configure(bg='white')

def hot_key():
    print(f"Hotkeys:\n{Fore.YELLOW + h1 + Style.RESET_ALL } =>", Fore.GREEN + "ON" + Style.RESET_ALL + "/" + Fore.RED + "OFF" + Style.RESET_ALL + " program")
    print(f"{Fore.YELLOW + h2 + Style.RESET_ALL } =>", Fore.GREEN + "ON" + Style.RESET_ALL + "/" + Fore.RED + "OFF" + Style.RESET_ALL + " reverse")
    print(f"{Fore.YELLOW + h3 + Style.RESET_ALL } =>", Fore.CYAN + "Calibration" + Style.RESET_ALL)

hot_button = tk.Button(window, text="Hotkey", command=hot_key)
hot_button.pack(side="left", padx=10)
hot_button.configure(bg='white')

# Load the MP3 file
rev_letter_mapping={}
def calibration(string):
    global rev_letter_mapping
    rev_letter_mapping.clear()
    # Create an empty dictionary to store the mappings
    letter_mapping = {
        'a': 'а',
        'c': 'с',
        'e': 'е',
        'i': 'і',
        'o': 'о',
        'p': 'р',
        'x': 'х',
        'y': 'у',
    }
    # Iterate over the string
    for char in string:
        # Check if the character is in the mapping dictionary
        if char in letter_mapping:
            # If it is, add the mapping to the new dictionary
            rev_letter_mapping[letter_mapping[char]] = char
def sound(name):
    data, fs = sf.read("files/" + name + ".mp3")
    sd.play(data, fs)
def modify_clipboard_text(text):
    # Create a dictionary mapping English letters to Russian letters
    letter_mapping = {
        'a': 'а',
        'c': 'с',
        'e': 'е',
        'i': 'і',
        'o': 'о',
        'p': 'р',
        'x': 'х',
        'y': 'у',
    }

    # Initialize an empty result string
    result = ""

    # Iterate through each character in the text
    for char in text:
        # If the character is an English letter, replace it with the corresponding Russian letter
        if char.lower() in letter_mapping:
            result += letter_mapping[char.lower()]
            print(f"{Fore.CYAN + char + Style.RESET_ALL}", end="")
        # Otherwise, just append the character to the result string as is
        else:
            result += char
            print(char, end="")
    return result
def reverse_modify_clipboard_text(text):
    # Create a dictionary mapping English letters to Russian letters

    # Initialize an empty result string
    result = ""

    # Iterate through each character in the text
    for char in text:
        # If the character is an English letter, replace it with the corresponding Russian letter
        if char.lower() in rev_letter_mapping:
            result += rev_letter_mapping[char.lower()]
            print(f"{Fore.CYAN + char + Style.RESET_ALL}", end="")
        # Otherwise, just append the character to the result string as is
        else:
            result += char
            print(char, end="")
    return result
previous_clipboard = ""
current_clipboard = ""
def change_clipboard_text():
    global up
    previous_clipboard = ""
    while True:
        current_clipboard = pyperclip.paste()
        if up==1 and current_clipboard != previous_clipboard and len(current_clipboard)>0:
            calibration(current_clipboard)
            up=0
            print("New dictionary:\n")
            for char in rev_letter_mapping:
                print(f"\'{Fore.GREEN + char + Style.RESET_ALL}\' : \'{Fore.CYAN + rev_letter_mapping[char] + Style.RESET_ALL}\'")
            print()
            calibration_button.configure(bg='white')
            if rswitch_value.get() == 1:
                canvas.itemconfigure(canvas.find_withtag("oval"), fill="yellow")
            else:
                if switch_value.get():
                    canvas.itemconfigure(canvas.find_withtag("oval"), fill="lime")
                else:
                    canvas.itemconfigure(canvas.find_withtag("oval"), fill="red")
            sound("finished")
            pyperclip.copy("")
        elif current_clipboard != previous_clipboard and switch_value.get() and not rswitch_value.get():
            #print(Fore.MAGENTA + f"Old text(Reverse OFF): " + Style.RESET_ALL + f"{current_clipboard}")
            if len(current_clipboard)>0: print(Fore.MAGENTA + f"Old text(Reverse" + Fore.RED + " OFF" + Fore.MAGENTA +"): " + Style.RESET_ALL + f"{current_clipboard}")
            current_clipboard=current_clipboard.lower()
            if len(current_clipboard)>0: print(Fore.BLUE + f"New text(Reverse" + Fore.RED + " OFF" + Fore.BLUE +"): " + Style.RESET_ALL, end="")
            # Clipboard content has changed, so call the function
            modified_text = modify_clipboard_text(current_clipboard)
            pyperclip.copy(modified_text)
            previous_clipboard = modified_text
            print("\n")
        elif current_clipboard != previous_clipboard and switch_value.get():
            if len(current_clipboard)>0: print(Fore.MAGENTA + f"Old text(Reverse" + Fore.GREEN + " ON" + Fore.MAGENTA +"): " + Style.RESET_ALL + f"{current_clipboard}")
            current_clipboard=current_clipboard.lower()
            if len(current_clipboard)>0: print(Fore.BLUE + f"New text(Reverse" + Fore.GREEN + " ON" + Fore.BLUE +"): " + Style.RESET_ALL, end="")
            # Clipboard content has changed, so call the function
            modified_text = reverse_modify_clipboard_text(current_clipboard)
            pyperclip.copy(modified_text)
            previous_clipboard = modified_text
            print("\n")
        time.sleep(0.5)

# Create a new thread
thread = threading.Thread(target=change_clipboard_text)

# Start the thread
thread.start()
# Create the main window
def update_status():
    global previous_clipboard
    global current_clipboard
    pyperclip.copy("")
    if switch_value.get() == 1:
        if rswitch_value.get() == 1:
            canvas.itemconfigure(canvas.find_withtag("oval"), fill="yellow")
        else:
            canvas.itemconfigure(canvas.find_withtag("oval"), fill="lime")
        # Change the oval to green
        print(Fore.GREEN + "Program is On" + Style.RESET_ALL)
        sound("ON")
    else:
        # Change the oval back to red
        canvas.itemconfigure(canvas.find_withtag("oval"), fill="red")
        print(Fore.RED + "Program is Off" + Style.RESET_ALL)
        sound("OFF")
    pyperclip.copy("")
def rev_update_status():
    global previous_clipboard
    previous_clipboard=""
    if rswitch_value.get() == 1:
        print(Back.GREEN + "Reverse is On" + Style.RESET_ALL)
        if switch_value.get() == 0:
            canvas.itemconfigure(canvas.find_withtag("oval"), fill="yellow")
            switch.invoke()
            sound('both')
            pyperclip.copy("")
        else:
            canvas.itemconfigure(canvas.find_withtag("oval"), fill="yellow")
            sound("reverse on")
            pyperclip.copy("")
    else:
        if switch_value.get():
            canvas.itemconfigure(canvas.find_withtag("oval"), fill="lime")
        else:
            canvas.itemconfigure(canvas.find_withtag("oval"), fill="red")
        print(Back.RED + "Reverse is Off" + Style.RESET_ALL)
        sound("reverse off")
    pyperclip.copy("")

# Bind the update_status function to the toggle switch's "command" event
switch.config(command=update_status)
rswitch.config(command=rev_update_status)
def key_bind():
    global current_clipboard
    from pynput.keyboard import Key, Listener


    def on_press(key):
        global current_clipboard
        if str(key)=="Key.f2":
            switch.invoke()
        if str(key)=="Key.f8":
            rswitch.invoke()
        if str(key)=="Key.f9":
            calibration_button.invoke()

    with Listener(on_press=on_press) as listener:
        listener.join()
thread1 = threading.Thread(target=key_bind)

# Start the thread
thread1.start()
def on_closing():
    os.system('taskkill /f /im Python.exe')

# Bind the on_closing function to the "WM_DELETE_WINDOW" event
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
