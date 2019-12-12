import pygame
import ctypes

class Button():

	def __init__(self, *args):
		self.type = "Button"
		self.x = args[0]
		self.y = args[1]
		self.w = args[2]
		self.h = args[3]
		self.text = None
		self.image = pygame.image.load("button.png")
		self.image = pygame.transform.scale(self.image, (self.w, self.h))
		self.selected = pygame.image.load("buttonselected.png")
		self.selected = pygame.transform.scale(self.selected, (0, self.h))
		self.rect = [self.x, self.y, self.w, self.h]
		if len(args) > 4:
			self.text = args[4]
			self.font = args[5]
			self.fontsize = args[6]
			self.fontObject = pygame.font.SysFont(self.font, self.fontsize)
			self.textObject = self.fontObject.render(self.text, True, (0, 0, 0))
			self.fontX, self.fontY = self.getFontXY()
			print("ButtonX: " + str(self.x) + " ButtonY: " + str(self.y) + " TextX: " + str(self.fontX) + " TextY: " + str(self.fontY))

	def rectCol(self, rect1, rect2):
		if rect1[0] + rect1[2] > rect2[0] and rect1[0] < rect2[0] + rect2[2] and rect1[1] < rect2[1] + rect2[3] and rect1[1] + rect1[3] > rect2[1]:
			return True
		else:
			return False

	def rectMouse(self, rect):
		mouse = pygame.mouse.get_pos()
		return mouse[0] > rect[0] and mouse[0] < rect[0] + rect[2] and mouse[1] > rect[1] and mouse[1] < rect[1] + rect[3]

	#def updatePosition(self):
		#self.selected = pygame.transform.scale(self.selected, (pygame.mouse.get_pos()[0] - 20, 20))

	def update(self):
		if self.rectMouse(self.rect):
			if self.type == "AudioButton":
				if pygame.mixer.music.get_busy() == True and self.counter != 0:
					pygame.mixer.music.pause()
				elif pygame.mixer.music.get_busy() == False and self.counter != 0:
					pygame.mixer.music.unpause()
				if self.counter == 0:
					pygame.mixer.music.play()
					self.counter += 1
			#self.updatePosition()

	def render(self, screen):
		screen.blit(self.image, (self.x, self.y))
		screen.blit(self.selected, (self.x, self.y))
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
		w2, h2, = self.GetTextDimensions(self.text, 18, self.font) #Gets the text width and height of button text based on font and font size
		return ((self.w - w2) / 2) + self.x, ((self.h - h2) / 2) + self.y #Math to return the x and y of where the pygame font object should be placed

	def setColor(self, red, green, blue):
		color = (red, green, blue, 0)
		self.image = self.image.copy()
		self.image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
		self.image.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

	def addAudio(self, filename):
		self.audio = pygame.mixer.music.load(filename)
		self.type = "AudioButton"
		self.counter = 0






