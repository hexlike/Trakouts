import pygame
import os
from os import listdir, path
from os.path import isfile, join
import sys
import tempfile
import shutil
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from Widget import Widget, Box, BasicButton, AudioButton
from WidgetGroup import WidgetGroup

#Columns and overlay columns for main screen
global openedTracksColumn 
global clickToOpenTracksColumn
global tracksOverlayColumn

#creates a Tkinter window
root = tk.Tk()
embed = tk.Frame(root, width = 1280, height = 720)
embed.grid(columnspan = (1280), rowspan = 720)
embed.pack(side = LEFT)
embed.winfo_toplevel().title("Trakouts")
buttonwin = tk.Frame(root, width = 0, height = 720)
buttonwin.pack(side = LEFT)
os.environ["SDL_WINDOWID"] = str(embed.winfo_id())
os.environ["SDL_VIDEODRIVER"] = "windib"

#Runs when the open file option button is selected. Adds a top column for the loading files column
def openFile():
	pygame.display.update()
	fileName = filedialog.askdirectory()
	tracksOverlayColumn.setTopV(True)
	tracksOverlayColumn.changeColumnTextByFolderTop(fileName, "Comic Sans MS", 18)
	tracksOverlayColumn.changeColumnAudioByFolderTop(fileName)
	tracksOverlayColumn.updateColumns()
	#tracksOverlayColumn.changeColumnAudioByFolderTop(fileName)
	root.update()

def openRecent():
	print("openrecent")

def saveAs():
	fileName = filedialog.asksaveasfilename()
	tracksOverlayColumn.saveAs(fileName + "/")

def new():
	print("new")

#Creates the main menu bar in the Tkinter window
menuBar = Menu(root)
fileMenu = Menu(menuBar, tearoff = 0)
fileMenu.add_command(label = "New", command = new)
fileMenu.add_separator()

openMenu = Menu(menuBar, tearoff = 0)
openMenu.add_command(label = "Open Files", command = openFile)
openMenu.add_separator()
openMenu.add_command(label = "Open Project")
openMenu.add_separator()
openMenu.add_command(label = "Open Recent", command = openRecent)

saveMenu = Menu(menuBar, tearoff = 0)
saveMenu.add_command(label = "Save As", command = saveAs)

fileMenu.add_cascade(label = "Open", menu = openMenu)
fileMenu.add_separator()
fileMenu.add_cascade(label = "Save", menu = saveMenu)

menuBar.add_cascade(label = "File", menu = fileMenu)

editMenu = Menu(menuBar, tearoff = 0)

root.config(menu = menuBar)

#Inits pygame 
pygame.display.set_caption("TraktrainPackager")

screen = pygame.display.set_mode((1280, 720))

pygame.display.init()
pygame.display.update()

def draw():
	pygame.display.update()
	button1 = Button(buttonwin, text = 'Draw', command = draw)
	button1.pack(side = LEFT)
	root.update()

background = pygame.image.load("background.png")

x = 17
y = 17

previousFileName = ""

#Detects if a previous session has been opened, will open previous session or if not will create a new one
if previousFileName == "":
	clickToOpenTracksColumn = WidgetGroup().widgetColumn(17, 17, 560, 20, 9, 17, 0)
	clickToOpenTracksColumn.changeColumnText("Click to add a track", "Comic Sans MS", 18)
	clickToOpenTracksColumn.changeColumnType("BasicButton")
	openedTracksColumn = WidgetGroup().widgetColumn(17, 17, 560, 20, 9, 17, 9)
	openedTracksColumn.changeColumnType("AudioButton")
	tracksOverlayColumn = WidgetGroup().widgetOverlayColumn(clickToOpenTracksColumn, openedTracksColumn, True, False)

running = True

#Main while loop
while running:

	pygame.display.update()

	screen.blit(background, (0, 0))

	tracksOverlayColumn.render(screen) #Renders the overlay column for the open tracks buttons

	root.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			click = tracksOverlayColumn.checkHover()
			if click != False:
				if click[1] > 8:
					tracksOverlayColumn.widgetClickByID(click[1])
			#elif isinstance(clickToOpenTracks, BasicButton):
				#fileName = filedialog.askopenfilename()
				#place = tracksOverlayColumn.getPlaceInListBottom(clickToOpenTracks)
				#tracksOverlayColumn.setBottomTextByPlace(place, fileName, "Comic Sans MS", 18)
				#tracksOverlayColumn.setBottomTypeByPlace(place, "AudioButton")
				#tracksOverlayColumn.setBottomAudioByPlace(place, fileName)

		elif event.type == pygame.MOUSEMOTION:
			tracksOverlayColumn.checkHover()

	