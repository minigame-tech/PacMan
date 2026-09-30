import logging
import random
import pygame
from typing import List, Tuple, Dict, Any, Optional

import lib.g2d as g2d
from src.Giocatore import Giocatore
from src.Menu.Main_Menu import Main_Menu
from src.settings import (
    FPS, CELL, SPRITE, BACKGROUND, MENU_BG, AUDIO_DIR,
    MAZE, MAZE_COLS, MAZE_ROWS, MAZE_PIXEL_W, MAZE_PIXEL_H,
    HUD_H, MAZE_OFFSET_X, MAZE_OFFSET_Y, CANVAS_W, CANVAS_H,
    START_COL, START_ROW, COLOR_YELLOW, COLOR_WHITE,
    GHOST_CLIPS, DIREZIONI
)

# Configurazione Logging Professionale
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class Mappa:
    """Converte coordinate pixel in celle della griglia e rileva i muri."""

    def __init__(self, griglia: List[str], cell: int, offset_x: int, offset_y: int):
        self._griglia = griglia
        self._cell = cell
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._cols = len(griglia[0])
        self._rows = len(griglia)

    def e_muro(self, x: float, y: float) -> bool:
        """Controlla se la coordinata corrisponde a un muro o alla casa dei fantasmi (per Pac-Man)."""
        col = int((x - self._offset_x) // self._cell)
        row = int((y - self._offset_y) // self._cell)
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            return False  # Zona di tunnel / wrap
        cella = self._griglia[row][col]
        return cella == "#" or cella == "g"  # Pac-Man non entra nella casa dei fantasmi

    def e_muro_per_fantasma(self, x: float, y: float) -> bool:
        """Controlla se la coordinata corrisponde a un muro (i fantasmi passano per 'g')."""
        col = int((x - self._offset_x) // self._cell)
        row = int((y - self._offset_y) // self._cell)
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            return False
        return self._griglia[row][col] == "#"


class Fantasma:
    """Rappresenta un nemico (Fantasma) con logica di movimento autonomo."""

    def __init__(self, col: int, row: int, nome_colore: str, mappa: Mappa, speed: int = 2):
        self._x = MAZE_OFFSET_X + col * CELL
        self._y = MAZE_OFFSET_Y + row * CELL
        self._clip = GHOST_CLIPS[nome_colore]
        self._mappa = mappa
        self._speed = speed
        self._dir = random.choice(list(DIREZIONI.keys()))

    def _allineato(self) -> bool:
        return (self._x - MAZE_OFFSET_X) % CELL == 0 and (self._y - MAZE_OFFSET_Y) % CELL == 0

    def _cella_corrente(self) -> Tuple[int, int]:
        col = (self._x - MAZE_OFFSET_X) // CELL
        row = (self._y - MAZE_OFFSET_Y) // CELL
        return int(col), int(row)

    def aggiorna(self) -> None:
        """Aggiorna la posizione e la direzione del fantasma."""
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

        # Gestione del tunnel ai lati dello schermo
        if self._x < MAZE_OFFSET_X - CELL:
            self._x = MAZE_OFFSET_X + MAZE_PIXEL_W
        elif self._x > MAZE_OFFSET_X + MAZE_PIXEL_W:
            self._x = MAZE_OFFSET_X - CELL

    def rettangolo(self) -> Tuple[float, float, int, int]:
        """Restituisce il bounding box per le collisioni."""
        return (self._x, self._y, CELL, CELL)

    def disegna(self) -> None:
        """Disegna il fantasma a schermo."""
        cx, cy, cw, ch = self._clip
        g2d.draw_image(SPRITE, (self._x, self._y), (cx, cy), (cw, ch))


class PacManGame:
    """Manager principale del ciclo di vita e stato del gioco."""
    
    def __init__(self):
        self.stato = "menu"
        self.punteggio = 0
        self.idx_sound = 0
        
        self.menu: Optional[Main_Menu] = None
        self.giocatore: Optional[Giocatore] = None
        self.mappa: Optional[Mappa] = None
        self.fantasmi: List[Fantasma] = []
        self.pallini: List[List[Any]] = []
        
        # Effetti audio
        self.sfx_eat_dots: List[pygame.mixer.Sound] = []
        self.sfx_morte: Optional[pygame.mixer.Sound] = None
        self.sfx_vittoria: Optional[pygame.mixer.Sound] = None

    def inizializza(self) -> None:
        """Configura il canvas, carica le risorse grafiche e audio."""
        logger.info("Inizializzazione motore grafico (g2d)...")
        g2d.init_canvas((CANVAS_W, CANVAS_H))
        
        # Caricamento assets
        g2d.load_image(SPRITE)
        g2d.load_image(BACKGROUND)
        try:
            g2d.load_image(MENU_BG)
        except Exception as e:
            logger.warning(f"Immagine menu non trovata: {e}")

        logger.info("Inizializzazione motore audio (pygame.mixer)...")
        pygame.mixer.init()
        try:
            # Effetti sonori
            self.sfx_eat_dots = [
                pygame.mixer.Sound(str(AUDIO_DIR / "eat_dot_0.wav")),
                pygame.mixer.Sound(str(AUDIO_DIR / "eat_dot_1.wav"))
            ]
            self.sfx_morte = pygame.mixer.Sound(str(AUDIO_DIR / "death_0.wav"))
            
            # Colonna sonora (volume basso)
            pygame.mixer.music.load(str(AUDIO_DIR / "start.wav"))
            pygame.mixer.music.set_volume(0.15)
            pygame.mixer.music.play(-1)
        except Exception as e:
            logger.error(f"Errore caricamento risorse audio: {e}. Il gioco continuerà senza suoni.")

        # Inizializzazione entità di base
        self.mappa = Mappa(MAZE, CELL, MAZE_OFFSET_X, MAZE_OFFSET_Y)
        self.menu = Main_Menu(CANVAS_W, CANVAS_H)
        logger.info("Gioco inizializzato con successo.")

    def _crea_fantasmi(self) -> List[Fantasma]:
        """Inizializza i 4 fantasmi principali nelle loro posizioni di spawn."""
        return [
            Fantasma(12, 14, "red",    self.mappa, 2),
            Fantasma(16, 14, "pink",   self.mappa, 2),
            Fantasma(12, 15, "cyan",   self.mappa, 2),
            Fantasma(16, 15, "orange", self.mappa, 2),
        ]

    def _crea_pallini(self) -> List[List[Any]]:
        """Scansiona la mappa e posiziona i pallini nei percorsi."""
        pallini = []
        for row in range(MAZE_ROWS):
            for col in range(MAZE_COLS):
                if MAZE[row][col] == ".":
                    if (col, row) == (START_COL, START_ROW):
                        continue
                    px = MAZE_OFFSET_X + col * CELL + CELL // 2
                    py = MAZE_OFFSET_Y + row * CELL + CELL // 2
                    pallini.append([px, py, True])  # True = Attivo
        return pallini

    def _collide(self, a: Tuple[float, float, int, int], b: Tuple[float, float, int, int]) -> bool:
        """Verifica l'intersezione tra due rettangoli."""
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    def _avvia_partita(self) -> None:
        """Prepara le variabili e avvia una nuova sessione di gioco."""
        logger.info("Avvio nuova partita...")
        cx = MAZE_OFFSET_X + START_COL * CELL + CELL // 2
        cy = MAZE_OFFSET_Y + START_ROW * CELL + CELL // 2
        
        self.giocatore = Giocatore(cx, cy, CANVAS_W, CANVAS_H)
        self.fantasmi = self._crea_fantasmi()
        self.pallini = self._crea_pallini()
        self.punteggio = 0
        self.stato = "gioco"

        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    def _torna_al_menu(self) -> None:
        """Ritorna alla schermata del menu principale."""
        logger.info("Ritorno al menu principale.")
        self.stato = "menu"
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    def _gestisci_pallini(self) -> None:
        """Controlla se il giocatore ha mangiato dei pallini e aggiorna il punteggio."""
        for pallino in self.pallini:
            if not pallino[2]:
                continue
            x, y, _ = pallino
            if abs(x - self.giocatore.x) < CELL // 2 and abs(y - self.giocatore.y) < CELL // 2:
                pallino[2] = False
                self.punteggio += 10
                
                if self.sfx_eat_dots:
                    self.sfx_eat_dots[self.idx_sound].play()
                    self.idx_sound = (1 - self.idx_sound)

    def _gestisci_collisioni_fantasmi(self) -> None:
        """Verifica se il giocatore è stato catturato da un fantasma."""
        for f in self.fantasmi:
            if self._collide(self.giocatore.rettangolo(), f.rettangolo()):
                self.giocatore.muori()
                return

    def _controlla_vittoria(self) -> None:
        """Verifica se il giocatore ha raccolto tutti i pallini per vincere la partita."""
        if all(not p[2] for p in self.pallini):
            logger.info("Vittoria raggiunta!")
            if self.sfx_vittoria:
                self.sfx_vittoria.play()
            self.stato = "vinci"

    def _controlla_game_over(self) -> None:
        """Controlla se le vite sono terminate e gestisce il Game Over."""
        if not self.giocatore.vivo:
            logger.info("Game Over - Vite terminate.")
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            if self.sfx_morte:
                self.sfx_morte.play()
            self.stato = "game_over"

    def _aggiorna_logica(self) -> None:
        """Esegue l'aggiornamento frame per frame della logica (modello)."""
        self.giocatore.gestisci_input()
        self.giocatore.aggiorna(self.mappa)
        
        for f in self.fantasmi:
            f.aggiorna()

        self._gestisci_pallini()
        self._gestisci_collisioni_fantasmi()
        self._controlla_vittoria()
        self._controlla_game_over()

    def _disegna_sfondo(self) -> None:
        try:
            raw = g2d._loaded[BACKGROUND]
            scaled = pygame.transform.scale(raw, (MAZE_PIXEL_W, MAZE_PIXEL_H))
            canvas = g2d.drawing_surface()
            canvas.blit(scaled, (MAZE_OFFSET_X, MAZE_OFFSET_Y))
        except Exception:
            g2d.set_color((0, 0, 0))
            g2d.draw_rect((MAZE_OFFSET_X, MAZE_OFFSET_Y), (MAZE_PIXEL_W, MAZE_PIXEL_H))

    def _disegna_pallini(self) -> None:
        g2d.set_color(COLOR_WHITE)
        for x, y, attivo in self.pallini:
            if attivo:
                g2d.draw_circle((x, y), 2)

    def _disegna_hud(self) -> None:
        g2d.set_color((0, 0, 0))
        g2d.draw_rect((0, 0), (CANVAS_W, HUD_H))

        g2d.set_color(COLOR_YELLOW)
        g2d.draw_text(f"Punteggio: {self.punteggio}", (80, HUD_H // 2), 18)
        g2d.draw_text(f"Vite: {self.giocatore.vite}", (CANVAS_W - 80, HUD_H // 2), 18)

    def _disegna_schermata_finale(self, testo: str) -> None:
        """Mostra l'overlay semi-trasparente per Game Over o Vittoria."""
        g2d.set_color((0, 0, 0, 170))
        g2d.draw_rect((0, 0), (CANVAS_W, CANVAS_H))
        g2d.set_color((255, 220, 0))
        g2d.draw_text(testo, (CANVAS_W // 2, CANVAS_H // 2 - 20), 40)
        g2d.set_color(COLOR_WHITE)
        g2d.draw_text("R = Rigioca   •   M = Menu",
                      (CANVAS_W // 2, CANVAS_H // 2 + 30), 16)

    def _disegna_gioco(self) -> None:
        """Effettua il rendering grafico completo del gioco."""
        g2d.clear_canvas()
        self._disegna_hud()
        self._disegna_sfondo()
        self._disegna_pallini()
        
        for f in self.fantasmi:
            f.disegna()
            
        self.giocatore.disegna()
        
        if self.stato in ("game_over", "vinci"):
            label = "GAME  OVER" if self.stato == "game_over" else "HAI  VINTO!"
            self._disegna_schermata_finale(label)

    def tick(self) -> None:
        """Funzione principale chiamata ad ogni frame dal motore g2d."""
        if self.stato == "menu":
            self.menu.aggiorna()
            self.menu.disegna()
            if self.menu.avvia:
                self._avvia_partita()
            elif self.menu.esci:
                logger.info("Chiusura del gioco dal menu principale.")
                g2d.close_canvas()

        elif self.stato == "gioco":
            self._aggiorna_logica()
            self._disegna_gioco()

        else:  # "game_over" o "vinci"
            self._disegna_gioco()
            if g2d.key_pressed("r") or g2d.key_pressed("R"):
                self._avvia_partita()
            elif g2d.key_pressed("m") or g2d.key_pressed("M"):
                self._torna_al_menu()


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    game = PacManGame()
    game.inizializza()
    g2d.main_loop(game.tick, fps=FPS)