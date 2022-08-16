import pygame, serial
from elements import Button, Gauge

WIDTH, HEIGHT = 1000, 650
NAME_WINDOW = 'Aeropêndulo: Controle'

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(NAME_WINDOW)

COLORS = {'WHITE': (255, 255, 255), 'BLUE': (100, 40, 255), 'RED': (255, 0, 0), 'PURPLE': (100, 40, 150), 'DARK_RED': (150, 50, 50),
          'GREEN': (0, 255, 0), 'DARK_GREEN': (50, 150, 50)}
BUTTON_DIMENTIONS = (200, 70)
X_ALIGN_BUTTONS = 400
Y_DISPLAY = 360
DISPLAY = Button(COLORS['WHITE'], X_ALIGN_BUTTONS, Y_DISPLAY, BUTTON_DIMENTIONS[0], BUTTON_DIMENTIONS[1])
START = Button(COLORS['BLUE'], X_ALIGN_BUTTONS, DISPLAY.y + BUTTON_DIMENTIONS[1] + 20, BUTTON_DIMENTIONS[0], BUTTON_DIMENTIONS[1], 'Start')
STOP = Button(COLORS['RED'], X_ALIGN_BUTTONS, START.y + BUTTON_DIMENTIONS[1], BUTTON_DIMENTIONS[0], BUTTON_DIMENTIONS[1], 'Stop')
FONT = pygame.font.SysFont('comicsans', 50)

GAUGE_ANGLE = Gauge(
        screen=WIN,
        FONT=FONT,
        x_cord= 500,
        y_cord=190,
        thickness=50,
        radius=150,
        circle_colour=(55, 77, 91),
        glow=False)

def redraw(input, output):
    WIN.fill([50,50,55])
    DISPLAY.draw(WIN)
    START.draw(WIN)
    STOP.draw(WIN)
    text = FONT.render(input, 1, (0, 0, 0))
    WIN.blit(text, (DISPLAY.x + 5, Y_DISPLAY))
    GAUGE_ANGLE.draw(percent=float(output))
    pygame.display.update()

def create_app():
    clock = pygame.time.Clock()
    user_input = '0'
    run = True
    esp_serial = serial.Serial('COM3', 115200, timeout=1)
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                if START.isOver(pos):
                    START.color = COLORS['DARK_GREEN']
                else:
                    START.color = COLORS['GREEN']
                if STOP.isOver(pos):
                    STOP.color = COLORS['DARK_RED']
                else:
                    STOP.color = COLORS['RED']
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START.isOver(pos):
                    esp_serial.write(user_input.encode())
                if STOP.isOver(pos):
                    esp_serial.write('-1'.encode())
            if event.type == pygame.KEYDOWN:
                if len(user_input) < 3:
                    if 47 < ord(event.unicode) < 58 or ord(event.unicode)==46 or event.unicode == '-':
                        if user_input == '0':
                            user_input = event.unicode
                        else:
                            user_input += event.unicode
                if ord(event.unicode) == 8:
                    if len(user_input) > 1:
                        user_input = user_input[:-1]
                    else:
                        user_input = '0'
        
        output = esp_serial.readline().decode('utf-8').replace('\r\n', '').split(',')[2]
        redraw(user_input, output)

if __name__ == "__main__":
    create_app()