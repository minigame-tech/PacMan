from src import Giocatore
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
    giocatore.aggiorna()
    giocatore.disegna()

def main():
    g2d.init_canvas((LARGHEZZA, ALTEZZA))

    g2d.main_loop(tick)

if __name__ == "__main__":
    main()