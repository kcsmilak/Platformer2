import pgzrun
import pygame


color = 0, 100, 255

class Meter:
  def __init__(self):
    self.values = []
    self.max = 100

  def addValue(self,val):
      self.values.append(val);
      if len(self.values) > self.max:
        self.values.pop(0)


  
  def drawVal(self, screen):
    if (len(self.values) <=0): return
    font = pygame.font.SysFont(None, 24)

    text = str(str(self.values[0]) + ":"+str(self.values[int(len(self.values)/2)]) + ":" +str(self.values[len(self.values)-1]) + ":" )
    
    img = font.render(text, True, (255,0,0))
    #screen.blit(img, (20,24*5))  
    for i in range(0, len(self.values)):
      #print("len=" +str (len(self.values)) + ":" + str(val))
      #box = Rect((0,0), (50,50))
      #box = ((0,0), (50,50))
      #surface = pygame.display
      #pygame.draw.rect(surface, color, pygame.Rect(30, 30, 60, 60),  2)
      v = self.values[i] 
      x = i + 300
      screen.draw.rect(pygame.Rect(x, 100, x+3, 100-v), color)

      
      #screen.draw.rect(box, color)
    