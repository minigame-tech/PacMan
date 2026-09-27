import math
import random
import pygame
import lib.g2d as g2d
from pathlib import Path
from src.Giocatore import Giocatore, CELL       # CELL deve essere 16 (vedi nota sopra)
from src.Menu.Main_Menu import Main_Menu

# ===========================================================================
# COSTANTI
# ===========================================================================
FPS = 30

SPRITE     = "assets/img/pac-man.png"
BACKGROUND = "assets/img/pac-man-bg.png"

BASE_DIR  = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "assets" / "audio"

# ---------------------------------------------------------------------------
# Labirinto estratto da pac-man-bg.png (griglia 29x32, cella originale 8px,
# qui disegnata a CELL px/cella, cioè scala 2x se CELL=16).
# '#' = muro, '.' = corridoio, 'g' = casa fantasmi (vietata a Pac-Man).
#
# Perimetro chiuso su tutti i lati tranne la riga 20, l'unico vero tunnel
# orizzontale: lì sia il bordo sinistro sia quello destro restano '.', così
# il wrap-around di Giocatore.aggiorna() scatta solo in quel corridoio.
# ---------------------------------------------------------------------------
MAZE = [
    "#############################",
    "#.............#.............#",
    "#.............#.............#",
    "#..###..####..#..####..###..#",
    "#..###..####..#..####..###..#",
    "#...........................#",
    "#...........................#",
    "#..###..#..#######..#..###..#",
    "#.......#.....#.....#.......#",
    "#.......#.....#.....#.......#",
    "######..####..#..####..######",
    "######..#...........#..######",
    "######..#...........#..######",
    "######..#..##ggg##..#..######",
    "...........#ggggg#...........",
    "...........#ggggg#...........",
    "######..#..#######..#..######",
    "######..#...........#..######",
    "######..#...........#..######",
    "######..#..#######..#..######",
    "#.............#.............#",
    "#.............#.............#",
    "#..###..####..#..####..###..#",
    "#....#.................#....#",
    "#....#.................#....#",
    "###..#..#..#######..#..#..###",
    "#.......#.....#.....#.......#",
    "#.......#.....#.....#.......#",
    "#..#########..#..#########..#",
    "#...........................#",
    "#...........................#",
    "#############################",
]
MAZE_COLS = len(MAZE[0])
MAZE_ROWS = len(MAZE)
MAZE_PIXEL_W = MAZE_COLS * CELL   # 464 se CELL=16
MAZE_PIXEL_H = MAZE_ROWS * CELL   # 512 se CELL=16

HUD_H = 40
MAZE_OFFSET_X = 0
MAZE_OFFSET_Y = HUD_H

CANVAS_W = MAZE_PIXEL_W
CANVAS_H = MAZE_PIXEL_H + HUD_H

# Punto di partenza di Pac-Man (colonna/riga nella griglia)
START_COL, START_ROW = 14, 23

# Colori
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE  = (255, 255, 255)

# Coordinate di ritaglio nello sprite sheet (16x16 nativi) per i fantasmi:
# un frame statico per colore (riga dedicata, colonna 0)
GHOST_CLIPS = {
    "red":    (0, 4 * 16, 16, 16),
    "pink":   (0, 5 * 16, 16, 16),
    "cyan":   (0, 6 * 16, 16, 16),
    "orange": (0, 7 * 16, 16, 16),
}

DIREZIONI = {
    "su":       (0, -1),
    "giu":      (0, 1),
    "sinistra": (-1, 0),
    "destra":   (1, 0),
}


# ===========================================================================
# MAPPA — adapter richiesto da Giocatore.aggiorna(mappa): espone e_muro(x, y)
# ===========================================================================
class Mappa:
    """Converte coordinate pixel (centro di Pac-Man) in cella della griglia
    e risponde se quella cella è un muro (o la casa dei fantasmi)."""

    def __init__(self, griglia: list, cell: int, offset_x: int, offset_y: int):
        self._griglia = griglia
        self._cell = cell
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._cols = len(griglia[0])
        self._rows = len(griglia)

    def e_muro(self, x: float, y: float) -> bool:
        col = int((x - self._offset_x) // self._cell)
        row = int((y - self._offset_y) // self._cell)
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            return False  # fuori griglia: lasciato passare (zona di tunnel/wrap)
        cella = self._griglia[row][col]
        return cella == "#" or cella == "g"  # Pac-Man non entra nella casa fantasmi

    def e_muro_per_fantasma(self, x: float, y: float) -> bool:
        col = int((x - self._offset_x) // self._cell)
        row = int((y - self._offset_y) // self._cell)
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            return False
        return self._griglia[row][col] == "#"


# ===========================================================================
# FANTASMI — pattugliamento con svolta casuale agli incroci (nessun Fantasma.py
# esistente nel progetto: implementato qui, sul modello di Veicolo/Piattaforma
# del Frogger)
# ===========================================================================
class Fantasma:
    def __init__(self, col: int, row: int, nome_colore: str, mappa: Mappa, speed: int = 2):
        self._x = MAZE_OFFSET_X + col * CELL
        self._y = MAZE_OFFSET_Y + row * CELL
        self._clip = GHOST_CLIPS[nome_colore]
        self._mappa = mappa
        self._speed = speed
        self._dir = random.choice(list(DIREZIONI.keys()))

    def _allineato(self) -> bool:
        return (self._x - MAZE_OFFSET_X) % CELL == 0 and (self._y - MAZE_OFFSET_Y) % CELL == 0

    def _cella_corrente(self) -> tuple:
        col = (self._x - MAZE_OFFSET_X) // CELL
        row = (self._y - MAZE_OFFSET_Y) // CELL
        return int(col), int(row)

    def aggiorna(self) -> None:
        if self._allineato():
            col, row = self._cella_corrente()
            opposta = {"su": "giu", "giu": "su", "sinistra": "destra", "destra": "sinistra"}[self._dir]
            possibili = []
            for nome, (dx, dy) in DIREZIONI.items():
                if nome == opposta:
                    continue
                nx = MAZE_OFFSET_X + (col + dx) * CELL
                ny = MAZE_OFFSET_Y + (row + dy) * CELL
                if not self._mappa.e_muro_per_fantasma(nx, ny):
                    possibili.append(nome)
            if not possibili:
                possibili = [opposta]
            self._dir = random.choice(possibili)

        dx, dy = DIREZIONI[self._dir]
        self._x += dx * self._speed
        self._y += dy * self._speed

        if self._x < MAZE_OFFSET_X - CELL:
            self._x = MAZE_OFFSET_X + MAZE_PIXEL_W
        elif self._x > MAZE_OFFSET_X + MAZE_PIXEL_W:
            self._x = MAZE_OFFSET_X - CELL

    def rettangolo(self) -> tuple:
        return (self._x, self._y, CELL, CELL)

    def disegna(self) -> None:
        cx, cy, cw, ch = self._clip
        g2d.draw_image(SPRITE, (self._x, self._y), (cx, cy), (cw, ch))


def _crea_fantasmi(mappa: Mappa) -> list:
    return [
        Fantasma(12, 14, "red",    mappa, 2),
        Fantasma(16, 14, "pink",   mappa, 2),
        Fantasma(12, 15, "cyan",   mappa, 2),
        Fantasma(16, 15, "orange", mappa, 2),
    ]


# ===========================================================================
# PALLINI
# ===========================================================================
def _crea_pallini() -> list:
    pallini = []
    for row in range(MAZE_ROWS):
        for col in range(MAZE_COLS):
            if MAZE[row][col] == ".":
                if (col, row) == (START_COL, START_ROW):
                    continue
                px = MAZE_OFFSET_X + col * CELL + CELL // 2
                py = MAZE_OFFSET_Y + row * CELL + CELL // 2
                pallini.append([px, py, True])
    return pallini


def _collide(a: tuple, b: tuple) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


# ===========================================================================
# STATO GLOBALE
# ===========================================================================
_stato:     str              = "menu"
_menu:      Main_Menu | None = None
_giocatore: Giocatore | None = None
_mappa:     Mappa | None     = None
_fantasmi:  list             = []
_pallini:   list             = []
_punteggio: int              = 0

_sfx_pallino:  pygame.mixer.Sound | None = None
_sfx_morte:    pygame.mixer.Sound | None = None
_sfx_vittoria: pygame.mixer.Sound | None = None


# ===========================================================================
# INIZIALIZZAZIONE
# ===========================================================================
def inizializza() -> None:
    """Crea canvas, carica risorse, istanzia mappa e menu. Chiamata una sola volta."""
    global _menu, _mappa, _sfx_pallino, _sfx_morte, _sfx_vittoria

    g2d.init_canvas((CANVAS_W, CANVAS_H))
    g2d.load_image(SPRITE)
    g2d.load_image(BACKGROUND)

    pygame.mixer.init()
    try:
        _sfx_pallino  = pygame.mixer.Sound(str(AUDIO_DIR / "sfx_pallino.wav"))
        _sfx_morte    = pygame.mixer.Sound(str(AUDIO_DIR / "sfx_morte.wav"))
        _sfx_vittoria = pygame.mixer.Sound(str(AUDIO_DIR / "sfx_vittoria.wav"))
        pygame.mixer.music.load(str(AUDIO_DIR / "sfx_main_theme.wav"))
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
    except Exception:
        pass  # audio non ancora presente: ci pensiamo dopo

    _mappa = Mappa(MAZE, CELL, MAZE_OFFSET_X, MAZE_OFFSET_Y)
    _menu = Main_Menu(CANVAS_W, CANVAS_H)


def _avvia_partita() -> None:
    global _giocatore, _fantasmi, _pallini, _punteggio, _stato
    cx = MAZE_OFFSET_X + START_COL * CELL + CELL // 2
    cy = MAZE_OFFSET_Y + START_ROW * CELL + CELL // 2
    _giocatore = Giocatore(cx, cy, CANVAS_W, CANVAS_H)
    _fantasmi  = _crea_fantasmi(_mappa)
    _pallini   = _crea_pallini()
    _punteggio = 0
    _stato     = "gioco"


def _torna_al_menu() -> None:
    global _stato
    _stato = "menu"


# ===========================================================================
# LOGICA DI GIOCO
# ===========================================================================
def _gestisci_pallini() -> None:
    global _punteggio
    for pallino in _pallini:
        if not pallino[2]:
            continue
        x, y, _ = pallino
        if abs(x - _giocatore.x) < CELL // 2 and abs(y - _giocatore.y) < CELL // 2:
            pallino[2] = False
            _punteggio += 10
            if _sfx_pallino:
                _sfx_pallino.play()


def _gestisci_collisioni_fantasmi() -> None:
    for f in _fantasmi:
        if _collide(_giocatore.rettangolo(), f.rettangolo()):
            if _sfx_morte:
                _sfx_morte.play()
            _giocatore.muori()
            return


def _controlla_vittoria() -> None:
    global _stato
    if all(not p[2] for p in _pallini):
        if _sfx_vittoria:
            _sfx_vittoria.play()
        _stato = "vinci"


def _controlla_game_over() -> None:
    global _stato
    if not _giocatore.vivo:
        _stato = "game_over"


def aggiorna_logica() -> None:
    _giocatore.gestisci_input()
    _giocatore.aggiorna(_mappa)
    for f in _fantasmi:
        f.aggiorna()

    _gestisci_pallini()
    _gestisci_collisioni_fantasmi()
    _controlla_vittoria()
    _controlla_game_over()


# ===========================================================================
# DISEGNO DI GIOCO
# ===========================================================================
def _disegna_sfondo() -> None:
    """Disegna lo sfondo scalando la superficie cachata da g2d alla
    dimensione reale del labirinto (MAZE_PIXEL_W x MAZE_PIXEL_H)."""
    try:
        raw = g2d._loaded[BACKGROUND]  # surface pygame già caricata da g2d.load_image
        scaled = pygame.transform.scale(raw, (MAZE_PIXEL_W, MAZE_PIXEL_H))
        canvas = g2d.drawing_surface()
        canvas.blit(scaled, (MAZE_OFFSET_X, MAZE_OFFSET_Y))
    except Exception:
        g2d.set_color((0, 0, 0))
        g2d.draw_rect((MAZE_OFFSET_X, MAZE_OFFSET_Y), (MAZE_PIXEL_W, MAZE_PIXEL_H))


def _disegna_pallini() -> None:
    g2d.set_color(COLOR_WHITE)
    for x, y, attivo in _pallini:
        if attivo:
            g2d.draw_circle((x, y), 2)


def _disegna_hud() -> None:
    g2d.set_color(COLOR_YELLOW)
    g2d.draw_text(f"Punteggio: {_punteggio}", (100, 20), 18)
    g2d.draw_text(f"Vite: {_giocatore.vite}", (CANVAS_W - 70, 20), 18)


def _disegna_schermata_finale(testo: str) -> None:
    g2d.set_color((0, 0, 0, 170))
    g2d.draw_rect((0, 0), (CANVAS_W, CANVAS_H))
    g2d.set_color((255, 220, 0))
    g2d.draw_text(testo, (CANVAS_W // 2, CANVAS_H // 2 - 20), 40)
    g2d.set_color(COLOR_WHITE)
    g2d.draw_text("R = Rigioca   •   M = Menu",
                  (CANVAS_W // 2, CANVAS_H // 2 + 30), 16)


def disegna_gioco() -> None:
    g2d.clear_canvas()
    _disegna_sfondo()
    _disegna_pallini()
    for f in _fantasmi:
        f.disegna()
    _giocatore.disegna()
    _disegna_hud()
    if _stato in ("game_over", "vinci"):
        label = "GAME  OVER" if _stato == "game_over" else "HAI  VINTO!"
        _disegna_schermata_finale(label)


# ===========================================================================
# TICK PRINCIPALE
# ===========================================================================
def tick() -> None:
    global _stato

    if _stato == "menu":
        _menu.aggiorna()
        _menu.disegna()
        if _menu.avvia:
            _avvia_partita()
        elif _menu.esci:
            g2d.close_canvas()

    elif _stato == "gioco":
        aggiorna_logica()
        disegna_gioco()

    else:  # "game_over" | "vinci"
        disegna_gioco()
        if g2d.key_pressed("r") or g2d.key_pressed("R"):
            _avvia_partita()
        elif g2d.key_pressed("m") or g2d.key_pressed("M"):
            _torna_al_menu()


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    inizializza()
    g2d.main_loop(tick, fps=FPS)