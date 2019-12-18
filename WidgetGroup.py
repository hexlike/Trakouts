import pygame
import os
from os import listdir, path
from os.path import isfile, join
import shutil
from Widget import Widget, BasicButton, AudioButton

class WidgetColumn:

	def __init__(self, *args):
		self.x = args[0]
		self.y = args[1]
		self.w = args[2]
		self.h = args[3]		
		self.length = args[4]
		print(args[5])
		self.spacing = args[5]
		self.widgets = []
		self.buttons = 0
		self.id = args[6]
		for x in range(0, self.length):
			self.widgets.append(Widget().basicBox(self.x, self.y, self.w, self.h, self.id))
			self.y += self.spacing + self.h
			self.id += 1
		self.newDirectory = ""

	def render(self, screen):
		for widget in self.widgets:
			widget.render(screen)

	def deleteWidgets(self, amount):
		for x in range(0, len(self.widgets) - amount):
			self.widgets.pop(0)

	def changeColumnType(self, typ):
		tempWidgets = []
		if typ == "BasicBox": 
			for widget in self.widgets:
			 	tempWidgets.append(Widget().basicBox(*widget.getWidgetInfo()))
		elif typ == "BasicButton":
			for widget in self.widgets:
				tempWidgets.append(Widget().basicButton(*widget.getWidgetInfo()))
				self.buttons += 1
		elif typ == "AudioButton":
			for widget in self.widgets:
				tempWidgets.append(Widget().audioButton(*widget.getWidgetInfo()))
				self.buttons += 1
		self.widgets = tempWidgets

	def changeColumnText(self, text, font, fontsize):
		for widget in self.widgets:
			widget.setText(text, font, fontsize)

	def setColumnFont(self, font, fontsize):
		for widget in self.widgets:
			widget.setFont(font, fontsize)

	def changeColumnTextByWidget(self, widgt, text, font, fontsize):
		for widget in self.widget:
			if widget == widgt:
				widget.setText(text, font, fontsize)

	def changeColumnTextByFolder(self, location, font, fontsize):
		allFiles = [f for f in listdir(location) if isfile(join(location, f)) and ".wav" in f]
		tempWidgets = []
		place = 0
		for file in (allFiles):
			self.widgets[place].setText(file, font, fontsize)
			tempWidgets.append(self.widgets[place])
			place += 1
		tempWidgets2 = []
		print(str(self.length - (self.length - len(tempWidgets))) + "hello")
		for x in range(self.length - (self.length - len(tempWidgets))):
			tempWidgets2.append(self.widgets[x])
		self.widgets = tempWidgets2

	def changeColumnTypeByWidget(self, widget, typ):
		for widgt in self.widgets:
			if widgt == widget:
				if typ == "BasicBox":
					widgt = Widget().basicBox(*widgt.getWidgetInfo())
					widgt.setType(typ)
				elif typ == "BasicButton":
					widgt = Widget().basicButton(*widgt.getWidgetInfo())
					widgt.setType(typ)
				elif typ == "AudioButton":
					widgt = Widget().audioButton(*widgt.getWidgetInfo())
					widgt.setType(typ)

	def changeColumnAudioByFolder(self, location):
		directories = open("Data/UntitledDirectories.txt", "r")
		directoryContent = ""
		self.newDirectory = ""
		if directories.read(1):
			directoryContent = directories.readlines()
			self.newDirectory = "UntitledFiles/Untitled" + str(len(directoryContent) + 1) + "/" 
		else:
			self.newDirectory = "UntitledFiles/Untitled1/"
		directories.close()
		directories = open("Data/UntitledDirectories.txt", "+a")
		directories.write(self.newDirectory + "\n")
		allFiles = [f for f in listdir(location) if isfile(join(location, f)) and ".wav" in f]
		for widget, file in zip(self.widgets, allFiles):
			print(file)
			widget.addAudio(location + "/" + file, self.newDirectory, file)
		os.mkdir(self.newDirectory)
		for file in allFiles:
			mp3File = file.replace(".wav", ".mp3")
			shutil.move(mp3File, self.newDirectory + mp3File)

			#tempWidgets.append(widget)
		#self.widgets = tempWidgets
	def getDirectory(self):
		return self.newDirectory

	def setTypeByPlace(self, place, typ):
		if typ == "BasicBox":
			self.widgets[place] = Widget().basicBox(*self.widgets[place].getWidgetInfo())
			self.widgets[place].setType(typ)
		elif typ == "BasicButton":
			self.widgets[place] = Widget().basicButton(*self.widgets[place].getWidgetInfo())
			self.widgets[place].setType(typ)
		elif typ == "AudioButton":
			self.widgets[place] = Widget().audioButton(*self.widgets[place].getWidgetInfo())
			self.widgets[place].setType(typ)

	def setTextByPlace(self, place, text, font, fontsize):
		self.widgets[place].setText(text, font, fontsize)

	def setAudioByPlace(self, place, filename):
		self.widgets[place].addAudio(filename)
		refresh()

	def getPlaceInList(self, widget):
		place = 0
		for widgt in self.widgets:
			if widgt == widget:
				return place
			place += 1

	def changeAudioByI(self, i, fileName):
		self.widgets[i].addAudio(fileName)

	def getWidgets(self):
		return self.widgets

	def getLength(self):
		return self.length

	def checkHover(self):
		for widget in self.widgets:
			if widget.rectMouse():
				return widget
		return False

	def getButtons(self):
		return self.buttons

class WidgetOverlayColumn():

	def __init__(self, bottom, top, bottomv, topv):
		self.audioLoaded = False

		self.currentWidgets = []

		self.bottom = bottom
		self.currentBottom = bottom.getWidgets()
		self.bottomv = bottomv

		self.top = top
		self.currentTop = top.getWidgets()
		self.topv = topv

		self.layers = []

		self.currentButton = None

		if self.topv == True:
			self.deleteWidgetsBottom()
			self.currentWidgets = self.currentTop + self.currentBottom
		else: 
			self.currentWidgets = self.currentBottom

		self.refresh()

	def refresh(self):
		self.currentBottom = self.bottom.getWidgets()
		self.currentTop = self.top.getWidgets()
		self.layers = []

	def deleteWidgetsBottom(self, amount):
		for x in range(0, amount):
			self.currentBottom.pop(0)

	def updateColumns(self):
		print("Length of widgets deleted: " + str(len(self.currentBottom) - (len(self.currentBottom) - len(self.currentTop))))
		self.deleteWidgetsBottom(len(self.currentBottom) - (len(self.currentBottom) - len(self.currentTop)))
		if self.topv == True:
			self.currentWidgets = self.currentTop + self.currentBottom
		else:
			self.currentWidgets = self.currentBottom

	def setBottomColumn(self, column):
		self.bottom = column
		self.currentBottom = column.getWidgets()
		self.refresh()

	def setTopColumn(self, column):
		self.top = column
		self.currentTop = column.getWidgets()
		self.refresh()

	def setBottomV(self, bottomv):
		self.bottomv = bottomv
		self.refresh()

	def setTopV(self, topv):
		self.topv = topv
		self.refresh()

	def changeColumnTypeBottom(self, typ):
		self.bottom.changeColumnType(typ)
		self.refresh()

	def changeColumnTypeTop(self, typ):
		self.top.changeColumnType(typ)
		self.refresh()

	def changeColumnTextBottom(self, text, font, fontsize):
		self.bottom.changeColumnText(text, font, fontsize)
		self.refresh()

	def changeColumnTextTop(self, text, font, fontsize):
		self.top.changeColumnText(text, font, fontsize)
		self.refresh()

	#def setColumnFontBottom(self, font, fontsize):

	#def setColumnFontTop():

	def changeColumnTextByFolderBottom(self, location, font, fontsize):
		self.bottom.changeColumnTextByFolder(location, font, fontsize)
		self.refresh()

	def changeColumnTextByFolderTop(self, location, font, fontsize):
		self.top.changeColumnTextByFolder(location, font, fontsize)
		self.refresh()

	def changeColumnAudioByFolderBottom(self, location):
		self.bottom.changeColumnAudioByFolder(location)
		self.refresh()

	def changeColumnAudioByFolderTop(self, location):
		self.top.changeColumnAudioByFolder(location)
		self.refresh()

	def getPlaceInListBottom(self, widget):
		place = 0
		for widgt in self.currentBottom:
			if widgt == widget:
				return place
			place += 1

	def getPlaceInListTop(self, widget):
		place = 0
		for widgt in self.currentTop:
			if widgt == widget:
				return place
			place += 1

	def setBottomTextByPlace(self, place, text, font, fontsize):
		self.bottom.setTextByPlace(place, text, font, fontsize)
		refresh()

	def setTopTextByPlace(self, place, text, font, fontsize):
		self.top.setTextByPlace(place, text, font, fontsize)
		refresh()

	def setBottomTypeByPlace(self, place, typ):
		self.bottom.setTypeByPlace(place, typ)
		refresh()

	def setTopTypeByPlace(self, place, typ):
		self.bottom.setTypeByPlace(place, typ)
		refresh()

	def setBottomAudioByPlace(self, place, fileName):
		self.bottom.addAudio(fileName)
		refresh()

	def setTopAudioByPlace(self, place, fileName):
		self.top.addAudio(fileName)
		refresh()

	def widgetClickByID(self, ID):
		print("looking for widget with id " + str(ID))
		for widget in self.currentWidgets:
			if widget.getID() == ID and widget.getType() == "AudioButton":
				print("loading audio into mixer")
				widget.clickLoadAudio()

	def update(self):
		if self.audioLoaded == True:
			pygame.mixer.music.play()

	def checkHover(self):
		place = 0
		for widget in self.currentWidgets:
			if widget.getType() == "BasicButton"and widget.rectMouse():
				widget.setSelected(True)
				return widget.getType(), widget.getID()
			elif widget.getType() == "AudioButton" and widget.rectMouse():
				widget.setSelected(True)
				return widget.getType(), widget.getID()
			else:
				widget.setSelected(False)
			place += 0
		return False

	def render(self, screen):
		for widget in self.currentWidgets:
			widget.render(screen)

	def saveAs(self, location):
		newDirectory = self.bottom.getDirectory()
		os.mkdir(location)
		allFiles = [f for f in listdir(newDirectory) if isfile(join(newDirectory, f)) and ".mp3" in f]
		for file in allFiles:
			shutil.move(file, location + file)


class WidgetGrid:

	def __init__(self, *args):

		if len(args) == 1:
			print("reading file")
		else:
			self.c = args[1]
			self.r = args[2]
			self.x = args[2]
			self.y = args[3]
			self.w = args[4]
			self.h = args[5]
			if len(args) < 7:
				self.spacingc = 0
				self.spacingr = 0
			else:
				self.spacingc = args[6]
				self.spacingr = args[7]

			x = self.x
			y = self.y

			self.columns = []

	def updateGrid(self, *args):
		x = self.x
		y = self.y
		for row in range(0, self.c):
			widgets = []
			for widget in range(0, self.r):
				widgets.append(Widget().basicBox(x, y, self.w, self.h))
				y += self.h + self.spaceRows
			self.columns.append(widgets)
			self.x += self.spaceColumns
		if len(args) > 0:
			for row in range(0, self.c):
				for widget in range(0, self.r):
					widget.updateFont()

	def render(self, screen):
		for row in self.columns:
			for widget in row:
				widget.render(screen)

	def changeColumnText(self, column, text, font, fontsize):
		x = self.x
		y = self.y
		self.columns = []
		for row in range(0, self.c):
			widgets = []
			for widget in range(0, self.r):
				widgets.append(Widget().basicBox(x, y, self.w, self.h, text, font, fontsize))
				y += self.h + self.spaceRows
			self.columns.append(widgets)
			self.x += self.spaceColumns
	
	def changeColumnTextByFolder(self, column, location, font, fontsize):
		allFiles = [f for f in listdir(location) if isfile(join(location, f))]
		for widget, file in zip(self.columns[column], allFiles):
			widget.setFont(font)
			widget.setFontSize(size)
			widget.setText(file)
		self.updateGrid()

	def changeXY(self, *args):
		if len(args) < 2:
			self.x = x
		else:
			self.y = y
		self.updateGrid()

	def addRowSpacing(self, space):
		self.spaceRows = space
		self.updateGrid()

class WidgetLayered(WidgetGrid):

	def __init__(self, *args):
		super().__init__(*args)

class WidgetGroup:

	def widgetGrid(self, *args):
		return WidgetGrid(*args)

	def widgetColumn(self, *args):
		return WidgetColumn(*args)

	def widgetOverlayColumn(self, *args):
		return WidgetOverlayColumn(*args)