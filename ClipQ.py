##
##  @title = ClipQ
##  @version = 1.1
##  @author = Kyle Murphey
##  @date = 02/19/2023
##  @summary = ClipQ is a specialized clipboard designed in a queue-like fashion
##

from tkinter import filedialog
import keyboard
import pyperclip
import pyautogui
import time
from tkinter import *
import tkinter.scrolledtext
import tkinter.messagebox
from Icon import Icon

clipboard = []              # clipboard that holds all the elements in a queue
default_keys = True         # flag for alt or shift keybinding - True is alt, False is shift
running = False             # flag to see if application is actively listening for hotkeys or not
icon = Icon.createIcon()    # construct the icon from the Icon class - returns "" on fail



# copies text to the clipboard and adds it to the queue
def copy():
    global clipboard
    global clipboard_text

    #check default keybind
    if (default_keys):
        #stay in loop until the keys are released on the keyboard
        while True:
            if (keyboard.is_pressed('ctrl') or 
                keyboard.is_pressed('alt') or
                keyboard.is_pressed('c')):
                while True:
                    if not (keyboard.is_pressed('ctrl') and 
                            keyboard.is_pressed('alt') and
                            keyboard.is_pressed('c')):
                        break
                break
    #check alternate keybind
    else:
        #stay in loop until the keys are released on the keyboard
        while True:
            if (keyboard.is_pressed('ctrl') or 
                keyboard.is_pressed('shift') or
                keyboard.is_pressed('c')):
                while True:
                    if not (keyboard.is_pressed('ctrl') and 
                            keyboard.is_pressed('shift') and
                            keyboard.is_pressed('c')):
                        break
                break
    #send ctrl + c to copy highlighted text
    with pyautogui.hold('ctrl'):
        pyautogui.press(['c'])

    time.sleep(0.02)                        #give computer time to add text to clipboard
    clipboard.append(pyperclip.paste())     #add copied text to queue
    #print(clipboard) #debugging

    #update GUI
    clipboard_text.configure(state='normal')
    clipboard_text.insert(END, str(clipboard[len(clipboard) - 1]) + "\n")
    clipboard_text.configure(state='disabled')


# copies text from queue into the clipboard, then pastes texts from the clipboard and removes last element from the queue
def paste():
    global clipboard
    global clipboard_text

    #ensure there is something to paste from the queue
    try:
        pyperclip.copy(clipboard[len(clipboard) - 1])
    except(IndexError):
        tkinter.messagebox.showinfo('Empty Queue', 'Your clipboard queue is empty - nothing can be pasted.')
        #print("Empty Clipboard") #debugging
        return
    
    #check default keybind
    if (default_keys):
        #stay in loop until the keys are released on the keyboard
        while True:
            if (keyboard.is_pressed('ctrl') or 
                keyboard.is_pressed('alt') or
                keyboard.is_pressed('v')):
                while True:
                    if not (keyboard.is_pressed('ctrl') and 
                            keyboard.is_pressed('alt') and
                            keyboard.is_pressed('v')):
                        break
                break
    #check alternate keybind
    else:
        #stay in loop until the keys are released on the keyboard
        while True:
            if (keyboard.is_pressed('ctrl') or 
                keyboard.is_pressed('shift') or
                keyboard.is_pressed('v')):
                while True:
                    if not (keyboard.is_pressed('ctrl') and 
                            keyboard.is_pressed('shift') and
                            keyboard.is_pressed('v')):
                        break
                break
    ##send ctrl + c to paste text
    with pyautogui.hold('ctrl'):
        pyautogui.press(['v'])

    time.sleep(0.01)        #give computer time to paste text from clipboard
    clipboard.pop()         #remove laste element from queue
    #print(clipboard) #debugging

    #update GUI
    clipboard_text.configure(state='normal')
    clipboard_text.delete(float(len(clipboard) + 1), END)
    if (len(clipboard) != 0):
        clipboard_text.insert(END, "\n")
    clipboard_text.configure(state='disabled')


# enable the global hotkeys
def start():
    global running

    #print(clipboard)    #debugging

    #register the hotkeys if not already running
    if not running:
        if (default_keys):
            keyboard.add_hotkey('ctrl + alt + c', lambda: copy())
            keyboard.add_hotkey('ctrl + alt + v', lambda: paste())
        else:
            keyboard.add_hotkey('ctrl + shift + c', lambda: copy())
            keyboard.add_hotkey('ctrl + shift + v', lambda: paste())
    running = True


# unregister hotkeys
def stop():
    global running

    if (running):
        keyboard.remove_all_hotkeys()
    running = False


# clear the queue and GUI
def clear():
    global clipboard

    clipboard = []

    clipboard_text.configure(state='normal')
    clipboard_text.delete(0.0, END)
    clipboard_text.configure(state='disabled')

    #print(clipboard) #debugging


# save the contents from the queue to a text file
def save():
    global clipboard_text

    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    #cancel is pressed
    if file is None:
        return
    output = str(clipboard_text.get(1.0, END))
    file.write(output)
    file.close()


# open a file and load it into the queue line by line
def openFile():
    global clipboard
    global clipboard_text

    clipboard = []  #clear the queue

    f = filedialog.askopenfile(mode='r')
    #cancel is pressed
    if f is None:
        return

    #clear the GUI
    clipboard_text.configure(state='normal')
    clipboard_text.delete(1.0, END)

    #add lines from file to queue
    while True:
        line = f.readline()
        if not line:
            break
        clipboard.append(line.strip())
        clipboard_text.insert(END, str(clipboard[len(clipboard) - 1]) + "\n")

    #add the last element loaded from the file to the clipboard
    try:
        pyperclip.copy(clipboard[len(clipboard) - 1])
    except(IndexError):
        tkinter.messagebox.showinfo('Empty Queue', 'Your clipboard queue is empty - nothing added to clipboard.')
        #print("Empty Clipboard")
        return
    
    clipboard_text.configure(state='disabled')

    f.close()
    #print(clipboard) #debugging


# toggle the hotkeys from 'ctrl + atl' to 'ctrl + shift' or vice versa
def swapKeys():
    global default_keys_text
    global default_keys
    global file_menu

    #hotkeys are currently active
    if (running):
        keyboard.remove_all_hotkeys()
        #toggle between alt and shift
        if (default_keys):
            keyboard.add_hotkey('ctrl + shift + c', lambda: copy())
            keyboard.add_hotkey('ctrl + shift + v', lambda: paste())
            default_keys_text.set("Shift")
            default_keys = False
            file_menu.entryconfigure(3, label='Swap hotkey from: ' + default_keys_text.get())
        else:
            keyboard.add_hotkey('ctrl + alt + c', lambda: copy())
            keyboard.add_hotkey('ctrl + alt + v', lambda: paste())
            default_keys_text.set("Alt")
            default_keys = True
            file_menu.entryconfigure(3, label='Swap hotkey from: ' + default_keys_text.get())
    #hotkeys aren't active yet
    else:
        if (default_keys):
            default_keys_text.set("Shift")
            default_keys = False
            file_menu.entryconfigure(3, label='Swap hotkey from: ' + default_keys_text.get())
        else:
            default_keys_text.set("Alt")
            default_keys = True
            file_menu.entryconfigure(3, label='Swap hotkey from: ' + default_keys_text.get())


# The about window display
def aboutWindow():
    global root

    aboutWindow = Toplevel(root)
    aboutWindow.wm_title('About')
    aboutWindow.geometry("350x185+30+30")

    if (icon == ""):
        aboutWindow.iconbitmap()
    else:
        aboutWindow.iconbitmap(icon)

    Message(aboutWindow, justify=CENTER, width=335, text="ClipQ v1.1\n\nClipQ is a specialized clipboard designed in a queue-like fashion.\n" +
    "It is intented to store multiple strings of text that are to be pasted in order into another application upon the triggering of set global hotkeys." +
    "\n\n\n\n Author: Kyle Murphey\nIcon from: https://icons8.com").grid()
    

# The help window display
def helpWindow():
    global root

    helpWindow = Toplevel(root)
    helpWindow.wm_title('Help')
    helpWindow.geometry("500x600+30+30")
    helpWindow.resizable(FALSE, TRUE)

    if (icon == ""):
        helpWindow.iconbitmap()
    else:
        helpWindow.iconbitmap(icon)

    frame = Frame(helpWindow, width="500", height="600")
    frame.pack(fill=BOTH,expand=1)

    canvas = Canvas(frame, width="400", height="600")
    canvas.pack(side=LEFT,fill=BOTH,expand=1)

    y_scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    y_scrollbar.pack(side=RIGHT,fill=Y)

    canvas.configure(yscrollcommand=y_scrollbar.set)
    canvas.bind("<Configure>",lambda x: canvas.config(scrollregion=canvas.bbox(ALL))) 

    display_frame = Frame(canvas, width="400", height="600")
    canvas.create_window((0,0), window=display_frame, anchor="nw")


    Label(display_frame, text="Keybindings").grid()

    Message(display_frame, justify=LEFT, width=450, text="""The default keybindings for this application are as follows:
    \tcopy to queue:\t\t\'ctrl + alt + c\'\n\tpaste from queue:\t\'ctrl + alt + v\'\n""").grid()

    Message(display_frame, justify=LEFT, width=450, text="""The alternate keybindings for this application are as follows:
    \tcopy to queue:\t\t\'ctrl + shift + c\'\n\tpaste from queue:\t\'ctrl + shift + v\'\n""").grid()

    Message(display_frame, justify=LEFT, width=450, text="""Keybinding are toggleable via the File cascade menu on the menu bar:
    \t\tFile->Swap hotkey from: Alt\n\t\tFile->Swap hotkey from: Shift""").grid()

    Message(display_frame, justify=LEFT, width=475, text="\nYou may have to swap keybindings based on the application you are trying to copy and paste from. " +
    "For example, you cannot copy from Word with ctrl + alt + c, but you can with ctrl + shift + c. With Notepad, pasting with ctrl + shift + v will paste " +
    "the text twice whereas ctrl + alt + v will work as desired. If both the alt and shift keybindings are already in use by the application you are trying to " +
    "send/grab text to/from, you may not be able to use ClipQ or end up with undesired results.\n\n").grid()


    Label(display_frame, text="Functionality").grid()

    Message(display_frame, justify=LEFT, width=475, text="This application is intented to copy multiple strings of text into a clipboard queue. " +
    "Copying with the set ClipQ keybinding will copy selected text to the clipboard and add the string to the queue. " +
    "Pasting with the set ClipQ keybinding will load the most recent string of copied text into the clipboard, paste it where your cursor is, and " +
    "and remove it from the queue. The pasted string will continue be in the clipboard on your computer until you paste again from ClipQ or another string is copied. " +
    "\n\nFiles loaded into ClipQ via the Open option on the menu bar are meant to be .txt files, each desired clipboard string on a separate line. " + 
    "Loading files of a different extension will either not work or give undesired results. \n\nSaving your clipboard queue via the Save option on the menu bar " +
    "will save your queue as a .txt file.\n\nSwapping your keybinding from Alt to Shift or vice versa can be done via the Swap hotkey from: option on the menu bar\n\n" +
    "The Clear option on the menu bar will clear out your clipboard queue. The clipboard on your computer will remain unchanged.\n\nThe Start and Stop buttons each " +
    "only have one function. Start will activate the global hotkeys for ClipQ and begin listening for them, and Stop will disable these hotkeys and ClipQ will " +
    "stop listening for them. Opening/Saving/Clearing/Swapping will not change the active/inactive state of this application; that functionality is solely toggled via " +
    "the Start and Stop buttons.").grid()





############################
## Creating the UI elements
############################
root = Tk()
root.title("ClipQ")
root.geometry('500x320') #500x300 without icon
root.resizable(FALSE, FALSE)

#ensure icon decoded properly from Icon class
if (icon == ""):
    root.iconbitmap()
    root.geometry('500x300')
else:
    root.iconbitmap(icon)
    


default_keys_text = StringVar(root, "Alt")

frame = tkinter.Frame(root)
frame.grid()


#the menu bar
menubar = Menu(root)
root.config(menu=menubar)

file_menu = Menu(menubar)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=openFile)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Swap hotkey from: ' + default_keys_text.get(), command=swapKeys)
file_menu.add_command(label='Clear', command=clear)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

help_menu = Menu(menubar)
menubar.add_cascade(label="About", menu=help_menu)
help_menu.add_command(label="About", command=aboutWindow)
help_menu.add_command(label="Help", command=helpWindow)

#frame around the clipboard queue
label_frame = tkinter.LabelFrame(frame, text=' Clipboard Queue ')
label_frame.grid(pady=5, padx=10)

#clipboard queue
clipboard_text = tkinter.scrolledtext.ScrolledText(label_frame, height=13.5, width=55, wrap = WORD)
clipboard_text.grid(pady=5, padx=5)
clipboard_text.configure(state='disabled')

#start button
start_button = Button(root, text='Start', width=10, command=start)
start_button.grid(ipadx=5)
start_button.place(x=355, y=267)

#stop button
stop_button = Button(root, text='Stop', width=5, command=stop)
stop_button.grid(ipadx=5, ipady=10)
stop_button.place(x=440, y=267)

root.mainloop()

Icon.removeIcon()   # remove temporary icon file