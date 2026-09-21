import lib.g2d as g2d
import pygame as pg

# Dimensione originale dello sprite sullo sprite sheet
SPRITE_SIZE = 16

# Dimensione desiderata a schermo
CELL = 40  
SPRITE_PATH = "assets/img/pac-man.png"

#Velocità di animazione
ANIM_SPEED = 6

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

        #Gestione animazione
        self._frame_index = 0
        self._anim_timer = 0

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

        #Gestione animazione
        if self._dir_corrente != "Fermo":
            self._anim_timer += 1
            if self._anim_timer >= ANIM_SPEED:
                self._anim_timer = 0
                self._frame_index = 1 if self._frame_index == 0 else 0 #Alterno tra frame 0 e 1

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
        """Disegno il frame selezionato, ruotato/riflesso in base alla direzione"""
        #Calcolo la colonna dello sprite sheet
        clip_x = self._frame_index * SPRITE_SIZE
        clip_y = 0

        #Ritaglio la tessera 16x16
        sub_surface = self._sprite_sheet.subsurface((clip_x, clip_y, SPRITE_SIZE, SPRITE_SIZE))

        #Rotazione in base alla direzione
        if self._dir_corrente == "ArrowLeft":
            sub_surface = pg.transform.flip(sub_surface, True, False)
        elif self._dir_corrente == "ArrowUp":
            sub_surface = pg.transform.rotate(sub_surface, 90)
        elif self._dir_corrente == "ArrowDown":
            sub_surface = pg.transform.rotate(sub_surface, 270)

        #Scalo lo sprite alle dimensioni 40x40
        scaled_sprite = pg.transform.scale(sub_surface, (self._w, self._h))

        #Disegno a schermo
        canvas = g2d.drawing_surface()
        pos_x = int(self._x - self._w // 2)
        pos_y = int(self._y - self._h // 2)

        canvas.blit(scaled_sprite, (pos_x, pos_y))