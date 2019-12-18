import pygame
import os
from os import listdir
from os.path import isfile, join
from Widget import Widget

class WidgetColumn:

	def __init__(self, x, y, w, h, length, spacing):
		self.x = x
		self.y = y
		self.w = w
		self.h = h		
		self.length = length
		self.spacing = args[4]
		self.widgets = []
		for x in range(0, self.length):
			self.widgets.append(Widget().basicBox(self.x, self.y, self.w, self.h))
			self.y += self.spacing + self.h

	def render(self, screen):
		for widget in self.widgets:
			widget.render(screen)

	def changeColumnType(self, typ):
		if typ == "BasicBox": 
			for widget in self.widgets:
			 	widget = Widget().basicBox(widget.getWidgetInfo()) 
		elif typ == "BasicButton":
			for widget in self.widgets:
				widget = Widget().basicButton(widget.getWidgetInfo())
		elif typ == "AudioButton":
			for widget in self.widgets:
				widget = Widget().audioButton(widget.getWidgetInfo())

	def changeColumnText(self, *text):
		for widget in self.widgets:
			widget.setText(text)

class WidgetOverlayColumn:

	def __init__(self, Top, Bottom):
		self.top = top
		self.bottom = bottom

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
				self.spacingr args[7]

			x = self.x
			y = self.y

			self.columns = []

			for column in self.r:
				


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