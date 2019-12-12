import pygame
from pygame.locals import *
from os import listdir
from os.path import isfile, join
import os
import sys
from Button import Button
import tkinter as tk
from tkinter import *
from tkinter import filedialog

fileName = "C:/Users/Ethan/Desktop/Everything/Work/Traktrain/rodeo/Trackout" #File location of the Traktrain folder

pygame.init()

pygame.display.set_caption("TraktrainPackager")

screen = pygame.display.set_mode((1280, 720))

background = pygame.image.load("background.png")

progname = sys.argv[0]
progdir = os.path.dirname(progname)
sys.path.append(os.path.join(progdir,'gamelib'))

from popup_menu import NonBlockingPopupMenu
from popup_menu import PopupMenu

file = (
	'File',
	'Open Folder',
	'Save',
)

folders = (
    'Folders',
    (
        'Open Folder',
    )
)

menu = NonBlockingPopupMenu(file, (0, 0), True)

clock = pygame.time.Clock()

root = tk.Tk()
root.withdraw()

def handle_menu(e):
	global menu
	if e.name == 'File':
		print("file")
		if e.text == 'Open Folder':
			file_path = filedialog.askdirectory()
	elif e.name == 'Open Folder':
		file_path = filedialog.askdirectory()
		pass

allFiles = [f for f in listdir(fileName) if isfile(join(fileName, f))] #Returns file names of all files in Traktrain folder

#for files in allFiles: #Prints the files in the trackout folder 
	#print(files)

audioButtons = []
randomButton = Button(400, 500, 400, 400, "Fart", "Comic Sans MS", 50)
randomButton.setColor(120, 230, 15)
randomButton.addAudio(fileName + "/Piano.wav")

windowButtons = []
windowButtons.append(Button(0, 0, 30, 20, "File", "Comic Sans MS", 18))

x = 20
y = 100

for file in allFiles: #Creates AudioButton instances for the files in the Traktrain folder
	audioButtons.append(Button(20, y, 560, 20, file, "Comic Sans MS", 18))
	y += 40

running = True

while running:
	screen.blit(background, (0, 0))

	for audioButton in audioButtons:
		audioButton.render(screen)

	randomButton.render(screen)

	menu.draw()

	pygame.display.flip()

	for event in menu.handle_events(pygame.event.get()):
		if event.type == pygame.QUIT:
			running = False
		if event.type == MOUSEBUTTONUP:
			menu.show()
		elif event.type == USEREVENT:
			if event.code == 'MENU':
				handle_menu(event)
				menu.show()
		if event.type == pygame.MOUSEBUTTONDOWN:
			randomButton.update()
			for button in windowButtons:
				button.update()


	clock.tick(60)

	