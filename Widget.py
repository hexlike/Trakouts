import pygame
import ctypes
from pydub import AudioSegment

class Box:

	def __init__(self, *args):
		pygame.init()
		self.visible = True
		self.x = args[0]
		self.y = args[1]
		self.w = args[2]
		self.h = args[3]
		self.id = args[4]
		self.text = None
		self.font = None
		self.fontsize = None
		self.image = pygame.image.load("button.png")
		self.image = pygame.transform.scale(self.image, (self.w, self.h))
		self.rect = [self.x, self.y, self.w, self.h]
		if len(args) > 5 and args[5] != None:
			self.text = args[5]
			self.font = args[6]
			self.fontsize = args[7]
			self.fontObject = pygame.font.SysFont(self.font, self.fontsize)
			self.textObject = self.fontObject.render(self.text, True, (0, 0, 0))
			self.updateFont()

	def update(self):
		print("nothing")

	def render(self, screen):
		if self.visible:
			screen.blit(self.image, (self.x, self.y))
		if self.text != None:
			screen.blit(self.textObject, (self.fontX, self.fontY))

	def GetTextDimensions(self, text, points, font): #Returns font dimensions
	    class SIZE(ctypes.Structure):
	        _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

	    hdc = ctypes.windll.user32.GetDC(0)
	    hfont = ctypes.windll.gdi32.CreateFontA(-points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
	    hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)
	    size = SIZE(0, 0)
	    ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))
	    ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
	    ctypes.windll.gdi32.DeleteObject(hfont)
	    return (size.cx, size.cy)

	def getFontXY(self):
		w2, h2, = self.GetTextDimensions(self.text, 18, self.font)
		print(self.text)
		print(self.font) #Gets the text width and height of button text based on font and font size
		return ((self.w - w2) / 2) + self.x, ((self.h - h2) / 2) + self.y #Math to return the x and y of where the pygame font object should be placed

	def getFont(self):
		return self.font

	def getFontSize(self):
		return self.fontsize

	def getText(self):
		return self.text

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getW(self):
		return self.w

	def getH(self):
		return self.h

	def getWidgetInfo(self):
		return [self.x, self.y, self.w, self.h, self.id, self.text, self.font, self.fontsize]

	def setColor(self, red, green, blue):
		color = (red, green, blue, 0)
		self.image = self.image.copy()
		self.image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
		self.image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

	def updateFont(self):
		self.fontObject = pygame.font.SysFont(self.font, self.fontsize)
		self.textObject = self.fontObject.render(self.text, True, (0, 0, 0))
		self.fontX, self.fontY = self.getFontXY()

	def setVisibility(self, visible):
		self.visible = visible

	def setText(self, text, font, fontsize):
		self.text = text
		self.font = font
		self.fontsize = fontsize
		self.updateFont()

	def setID(self, ID):
		self.id = ID

	def getID(self):
		return self.id

	def getType(self):
		return "BasicBox"

	def setType(self, typ):
		self.type = typ

class BasicButton(Box):

	def __init__(self, *args):
		self.type = "BasicButton"
		super().__init__(*args)
		self.selected = pygame.image.load("buttonselected.png")
		self.selected = pygame.transform.scale(self.selected, (self.w, self.h))
		self.selectedv = False

	def rectCol(self, rect1, rect2):
		if self.visible and rect1[0] + rect1[2] > rect2[0] and rect1[0] < rect2[0] + rect2[2] and rect1[1] < rect2[1] + rect2[3] and rect1[1] + rect1[3] > rect2[1]:
			return True
		else:
			return False

	def rectMouse(self):
		mouse = pygame.mouse.get_pos()
		rect = self.rect
		return mouse[0] > rect[0] and mouse[0] < rect[0] + rect[2] and mouse[1] > rect[1] and mouse[1] < rect[1] + rect[3]

	#def updatePosition(self):
		#self.selected = pygame.transform.scale(self.selected, (pygame.mouse.get_pos()[0] - 20, 20))

	def update(self):
		self.selected = pygame.transform.scale(self.selected, (self.w, self.h))
		return self.rectMouse(self.rect)

	def render(self, screen):
		if self.visible:
			screen.blit(self.image, (self.x, self.y))
			if self.selectedv:
				screen.blit(self.selected, (self.x, self.y))
			if self.text != None:
				screen.blit(self.textObject, (self.fontX, self.fontY))

	def setSelected(self, selected):
		self.selectedv = selected

	def setVisibility(self, visible):
		self.visible = visible

	def getType(self):
		return "BasicButton"

class AudioButton(BasicButton):

	def __init__(self, *args):
		self.type = "AudioButton"
		super().__init__(*args)
		self.counter = 0
		self.audio = None
		self.filename = None
		self.started = False
		self.playing = None

	def update(self):
		if pygame.mixer.music.get_busy() == True and self.counter != 0:
			pygame.mixer.music.pause()
		elif pygame.mixer.music.get_busy() == False and self.counter != 0:
			pygame.mixer.music.unpause()
		if self.counter == 0:
			pygame.mixer.music.play()
			self.counter += 1
			#self.updatePosition()

	def addAudio(self, location, newLocation, filename):
		self.newLocation = newLocation
		convertedFileName = filename.replace(".wav", ".mp3")
		AudioSegment.from_file(location).export(convertedFileName, format="mp3")
		self.filename = newLocation + convertedFileName
		self.type = "AudioButton"

	def loadAudio(self):
		if self.filename != None:
			pygame.mixer.music.load(self.filename)

	def clickLoadAudio(self):
		if self.filename != None:
			if self.started == False:
				pygame.mixer.music.load(self.filename)
				pygame.mixer.music.play()
				self.started = True
				self.playing = True
			elif self.playing:
				print("the mixer is busy")
				pygame.mixer.music.pause()
				self.playing = False
			else:
				print("the mixer isnt busy")
				pygame.mixer.music.unpause()
				self.playing = True

	def getType(self):
		return "AudioButton"

class Widget:

	def basicBox(self, *args):
		return Box(*args)

	def basicButton(self, *args):
		return BasicButton(*args)

	def audioButton(self, *args):
		return AudioButton(*args)
