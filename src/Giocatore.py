import lib.g2d as g2d
import pygame as pg

# Dimensione originale dello sprite sullo sprite sheet
SPRITE_SIZE = 16

# Dimensione desiderata a schermo (ingrandita)
CELL = 40  
SPRITE_PATH = "assets/img/pac-man.png"


class Giocatore:
    """Rappresenta Pac-Man controllato dal giocatore."""

    def __init__(self, x: float, y: float, canvas_w: int, canvas_h: int):
        self._x = x
        self._y = y
        self._start_x = x
        self._start_y = y
        self._w = CELL
        self._h = CELL
        self._velocita = 4

        self._canvas_w = canvas_w
        self._canvas_h = canvas_h

        # Tabella direzioni: (dx, dy)
        self._direzioni = {
            "ArrowLeft": (-1, 0),
            "ArrowRight": (1, 0),
            "ArrowUp": (0, -1),
            "ArrowDown": (0, 1),
            "Fermo": (0, 0),
        }

        self._dir_corrente = "Fermo"
        self._dir_successiva = "Fermo"
        self._vite = 3
        self._vivo = True

        # Carica e mantiene lo sprite originale
        self._sprite_sheet = pg.image.load(SPRITE_PATH)

    # ------------------------------------------------------------------
    # Proprietà di accesso
    # ------------------------------------------------------------------
    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def w(self) -> int:
        return self._w

    @property
    def h(self) -> int:
        return self._h

    @property
    def vite(self) -> int:
        return self._vite

    @property
    def vivo(self) -> bool:
        return self._vivo

    # ------------------------------------------------------------------
    # Input e Movimento
    # ------------------------------------------------------------------
    def gestisci_input(self) -> None:
        """Legge i tasti premuti e imposta la direzione desiderata."""
        if g2d.key_pressed("ArrowLeft"):
            self._dir_successiva = "ArrowLeft"
        elif g2d.key_pressed("ArrowRight"):
            self._dir_successiva = "ArrowRight"
        elif g2d.key_pressed("ArrowUp"):
            self._dir_successiva = "ArrowUp"
        elif g2d.key_pressed("ArrowDown"):
            self._dir_successiva = "ArrowDown"

    def aggiorna(self) -> None:
        """Aggiorna la posizione e gestisce il wrap del bordo."""
        if self._dir_successiva != "Fermo":
            self._dir_corrente = self._dir_successiva

        dx, dy = self._direzioni[self._dir_corrente]

        self._x += dx * self._velocita
        self._y += dy * self._velocita

        # Effetto Pac-Man sui bordi dello schermo
        raggio = self._w // 2
        if self._x > self._canvas_w + raggio:
            self._x = -raggio
        elif self._x < -raggio:
            self._x = self._canvas_w + raggio

        if self._y > self._canvas_h + raggio:
            self._y = -raggio
        elif self._y < -raggio:
            self._y = self._canvas_h + raggio

    def rettangolo(self) -> tuple[int, int, int, int]:
        """Restituisce il rettangolo di collisione (x, y, w, h)."""
        return (int(self._x - self._w // 2), int(self._y - self._h // 2), self._w, self._h)

    # ------------------------------------------------------------------
    # Disegno
    # ------------------------------------------------------------------
    def disegna(self) -> None:
        """Ritaglia il singolo frame 16x16, lo scala a 40x40 e lo disegna."""
        # 1. Taglia la singola cella 16x16 dallo sprite sheet (in alto a sinistra: 0, 0)
        sub_surface = self._sprite_sheet.subsurface((0, 0, SPRITE_SIZE, SPRITE_SIZE))

        # 2. Ingrandisce la tessera alla dimensione desiderata (CELL x CELL)
        scaled_sprite = pg.transform.scale(sub_surface, (self._w, self._h))

        # 3. Disegna la superficie ingrandita sul canvas di g2d
        canvas = g2d.drawing_surface()
        pos_x = int(self._x - self._w // 2)
        pos_y = int(self._y - self._h // 2)

        canvas.blit(scaled_sprite, (pos_x, pos_y))