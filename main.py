from src.Giocatore import Giocatore
from src.Menu import Main_Menu
import lib.g2d as g2d

LARGHEZZA = 800
ALTEZZA = 600

giocatore = Giocatore(
    400,
    300,
    LARGHEZZA,
    ALTEZZA
)

def tick():
    #Lancio il main menu
    Main_Menu.draw_menu()

    # 1. Gestione dell'input del giocatore
    giocatore.gestisci_input()

    # 2. Aggiornamento della logica
    giocatore.aggiorna()

    # 3. Disegno a schermo
    g2d.clear_canvas()
    giocatore.disegna()

def main():
    g2d.init_canvas((LARGHEZZA, ALTEZZA))
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()