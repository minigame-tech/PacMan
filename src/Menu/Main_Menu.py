import lib.g2d as g2d

# ---------------------------------------------------------------------------
# Risorse e Costanti Grafiche
# ---------------------------------------------------------------------------
SPRITE = "assets/img/Logo.jpeg"
BACKGROUND = "assets/img/Background_MainMenu.jpg"

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Colori Pac-Man
COLOR_BLACK = (0, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_PINK = (255, 184, 255)
COLOR_ORANGE = (255, 184, 82)
COLOR_GRAY = (120, 120, 120)

# Dimensioni area cliccabile dei bottoni
_BTN_W, _BTN_H = 280, 48

#Posizioni Y dei centri dei 3 bottoni
_BTN0_CY = 250 # GIOCA
_BTN1_CY = 320 # COME SI GIOCA
_BTN2_CY = 390 # ESCI

_BTNS = [_BTN0_CY, _BTN1_CY, _BTN2_CY]