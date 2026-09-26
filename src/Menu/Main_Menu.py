import lib.g2d as g2d

SPRITE = "assets/img/Logo.jpeg"
BACKGROUND = "assets/img/Background_MainMenu.jpg"

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

COLOR_BLACK  = (0, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE  = (255, 255, 255)
COLOR_BLUE   = (0, 0, 255)

def draw_menu():
    """Disegno gli elementi essenziali del menu principale"""
    g2d.clear_canvas()
    g2d.draw_text("PACMAN", COLOR_YELLOW, (150, 150), 60)

    g2d.draw_text("Premi SPAZIO per iniziare", COLOR_WHITE, (140, 350), 24)
    g2d.draw_text("Premi ESC per uscire", COLOR_WHITE, (170, 400), 20)

    g2d.set_color(COLOR_YELLOW)
    g2d.fill_circle((300, 260), 30)