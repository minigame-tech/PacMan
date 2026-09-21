import lib.g2d as g2d

class Giocatore:
    def __init__(self, x, y, larghezza_finestra, altezza_finestra):
        self._x = x
        self._y = y
        self.raggio = 20
        self.velocita = 4
        self.direzioni = {
            "FrecciaSinistra": (-1, 0),
            "FrecciaSu": (0, -1),
            "FrecciaGiu": (0, 1),
            "Fermo": (0, 0)
        }
        self.direzione_corrente = "Fermo"
        self.direzione_successiva = "Fermo"
        self.larghezza_finestra = larghezza_finestra
        self.altezza_finestra = altezza_finestra

    def cambia_direzione(self, tasto_premuto: str):
        if tasto_premuto in self.direzioni:
            self.direzione_successiva = tasto_premuto

    def aggiorna(self):
        if self.direzione_successiva != "Fermo":
            self.direzione_corrente = self.direzione_successiva
        dx, dy = self.direzioni[self.direzione_corrente]

        self._x += dx * self.velocita
        self._y += dy * self.velocita
        if self._x > self.larghezza_finestra + self.raggio:
            self._x = -self.raggio
        elif self._x < -self.raggio:
            self._x = self.larghezza_finestra + self.raggio
        if self._y > self.altezza_finestra + self.raggio:
            self._y = -self.raggio
        elif self._y < -self.raggio:
            self._y = self.altezza_finestra + self.raggio

    def disegna(self):
        g2d.set_color((255, 255, 0))
        g2d.draw_circle((int(self._x), int(self._y)), self.raggio)