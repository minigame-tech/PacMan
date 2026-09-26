from src.Giocatore import Giocatore
from src.Menu.Main_Menu import Main_Menu
import lib.g2d as g2d

LARGHEZZA = 800
ALTEZZA = 600

# Inizializzazione
menu = Main_Menu(LARGHEZZA, ALTEZZA)
giocatore = Giocatore(LARGHEZZA // 2, ALTEZZA // 2, LARGHEZZA, ALTEZZA)

stato_gioco = "MENU"

def tick():
    global stato_gioco

    if stato_gioco == "MENU":
        menu.aggiorna()
        if menu.avvia:
            stato_gioco = "GIOCO"
        elif menu.esci:
            g2d.close_canvas()
            return
        menu.disegna()

    elif stato_gioco == "GIOCO":
        giocatore.gestisci_input()
        giocatore.aggiorna()
        g2d.clear_canvas()
        giocatore.disegna()

def main():
    g2d.init_canvas((LARGHEZZA, ALTEZZA))
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()