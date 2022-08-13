import pygame
import pygame.gfxdraw
import math

pygame.font.init()

class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
class Gauge():
    def __init__(self, screen, FONT, x_cord, y_cord, thickness, radius, circle_colour, glow=True):
        self.screen = screen
        self.Font = FONT
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.thickness = thickness
        self.radius = radius
        self.circle_colour = circle_colour
        self.glow = glow

    def draw(self, percent):
        fill_angle = int(percent*270/90)
        per=percent
        if per <=40:
            per=0
        if per > 100:
            per = 100
        ac = [int(255-per*255/100), 255, int(per*255/100)]
        for indexi in range(len(ac)):
            if ac[indexi] < 0:
                ac[indexi] = 0
            if ac[indexi] > 255:
                ac[indexi] = 255
        # print(ac)

        pertext = self.Font.render(str(percent) + "°", True, ac)
        pertext_rect = pertext.get_rect(center=(int(self.x_cord), int(self.y_cord)))
        self.screen.blit(pertext, pertext_rect)

        for i in range(0, self.thickness):
            
            pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, 270 - 225, self.circle_colour)
            if percent >4:
                pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, fill_angle - 225-8, ac)

        if percent < 4:
            return

        if self.glow:
            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius + i, -225, fill_angle - 225-8, ac)

            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius -self.thickness - i, -225, fill_angle - 225-8, ac)

            angle_r = math.radians(fill_angle-225-8)
            lx,ly = int((self.radius-self.thickness/2)*math.cos(angle_r)), int( (self.radius-self.thickness/2)*math.sin(angle_r))
            ac[3] = 255
            lx = int(lx+self.x_cord)
            ly = int(ly + self.y_cord)

            pygame.draw.circle(self.screen,ac,(lx,ly),int(self.thickness/2),0)


            for i in range(0,10):
                ac [3] = int(150 - i*15)
                pygame.gfxdraw.arc(self.screen, int(lx), int(ly), (self.thickness//2)+i , fill_angle -225-10, fill_angle - 225-180-10, ac)