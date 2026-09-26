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

# Posizioni Y dei centri dei 3 bottoni
_BTN0_CY = 250 # GIOCA
_BTN1_CY = 320 # COME SI GIOCA
_BTN2_CY = 390 # ESCI

_BTNS = [_BTN0_CY, _BTN1_CY, _BTN2_CY]

# Classe principale
class MainMenu:
    def __init__(self, canvas_w: int = SCREEN_WIDTH, canvas_h: int = SCREEN_HEIGHT):
        self._cw = canvas_w
        self._ch = canvas_h

        self._voce_sel  = 0 # 0=GIOCA, 1=COME SI GIOCA, 2=ESCI
        self._anim_tich = 0
        self._mostra_istruzioni = False

        # Segali letti dal loop principale
        self._avvia = False
        self._esci  = False

    # ---------------------------------------------------------------------------
    # Segnali pubblici
    # ---------------------------------------------------------------------------
    @property
    def avvia(self) -> bool:
        return self._avvia

    @property
    def esci(self) -> bool:
        return self._esci

    # ---------------------------------------------------------------------------
    # Aggiornamento Logic
    # ---------------------------------------------------------------------------
    def aggiorna(self) -> None:
        self._avvia = False
        self._esci  = False
        self._anim_tich += 1

        if self._mostra_istruzioni:
            # Qualsiasi tasto o click chiude la schermata istruzioni
            if (
                g2d.key_pressed("Enter")
                or g2d.key_pressed("Escape")
                or g2d.key_pressed("Spacebar")
                or g2d.mouse_clicked()
            ):
                self._mostra_istruzioni = False
            else:
                self._gestisci_tastiera()
                self._gestisci_mouse()

    def _gestisci_tastiera(self) -> None:
        if g2d.key_pressed("ArrowUp") or g2d.key_pressed("w"):
            self._voce_sel = (self._voce_sel - 1) % 3
        elif g2d.key_pressed("ArrowDown") or g2d.key_pressed("s"):
            self._voce_sel = (self._voce_sel + 1) % 3

        if (
            g2d.key_pressed("Enter")
            or g2d.key_pressed("Spacebar")
        ):
            self._conferma()

    def _gestisci_mouse(self) -> None:
        if not g2d.mouse_clicked():
            return

        mx, my = g2d.mouse_pos()
        bx = self._cw // 2 - _BTN_W // 2
        for i, cy in enumerate(_BTNS):
            if bx <= mx <= bx + _BTN_W:
                if cy - _BTN_H // 2 <= my <= cy + _BTN_H // 2:
                    self._voce_sel = i
                    self._conferma()
                    return

    def _conferma(self) -> None:
        if self._voce_sel == 0:
            self._avvia = True
        elif self._voce_sel == 1:
            self._mostra_istruzioni = True
        else:
            self._esci = True

    # ---------------------------------------------------------------------------
    # Disegno
    # ---------------------------------------------------------------------------
    def disegna(self) -> None:
        g2d.clear_canvas()
        self._disegna_sfondo()
        self._disegna_logo()
        self._disegna_sottotitolo()
        self._disegna_decorazione_pallini()
        self._disegna_bottone("  GIOCA  ", _BTN0_CY, self._voce_sel == 0)
        self._disegna_bottone(" COME SI GIOCA ", _BTN1_CY, self._voce_sel == 1)
        self._disegna_bottone("   ESCI   ", _BTN2_CY, self._voce_sel == 2)
        self._disegna_cursore_pacman()
        self._disegna_decorazioni_basse()

        if self._mostra_istruzioni:
            self._disegna_schermata_istruzioni()

    def _disegna_sfondo(self) -> None:
        # Se presente l'immagine di sfondo la disegna, altrimenti sfondo nero
        try:
            g2d.draw_image(BACKGROUND, (0, 0))
            g2d.set_color((0, 0, 0, 160))
            g2d.draw_rect((0, 0), (self._cw, self._ch))
        except Exception:
            g2d.set_color(COLOR_BLACK)
            g2d.draw_rect((0, 0), (self._cw, self._ch))

    def _disegna_logo(self) -> None:
        cx = self._cw // 2
        g2d.set_color(COLOR_YELLOW)
        g2d.draw_text("PACMAN", (cx, 80), 55)
    
    def _disegna_sottotitolo(self) -> None:
        g2d.set_color(COLOR_CYAN)
        g2d.draw_text(
           "Usa le frecce • INVIO per confermare", (self._cw // 2, 135), 18
        )

    def _disegna_decorazione_pallini(self) -> None:
        """Disegna una fila di pallini decorativi sotto il titolo"""
        y = 175
        for i in range(11):
            x = 60 + i * 48
            g2d.set_color(COLOR_WHITE)
            g2d.fill_circle((x, y), 4)

    def _disegna_bottone(self, label: str, cy: int, selezionato: bool) -> None:
        cx = self._cw // 2
        bx = cx - _BTN_W // 2
        by = cy - _BTN_H // 2

        alpha = 200 if selezionato else 100
        g2d.set_color((0, 0, 0, alpha))
        g2d.set_color((bx, by), (_BTN_W, _BTN_H))

        # Bordo del bottone
        border = COLOR_YELLOW if selezionato else COLOR_BLUE
        g2d.set_color(border)
        g2d.draw_line((bx, by), (bx + _BTN_W, by), 3)
        g2d.draw_line((bx + _BTN_W, by), (bx + _BTN_W, by + _BTN_H), 3)
        g2d.draw_line((bx + _BTN_W, by + _BTN_H), (bx, by + _BTN_H), 3)
        g2d.draw_line((bx, by + _BTN_H), (bx, by), 3)

        # Icone/Pallini ai lati dei bottoni
        dot_color = COLOR_YELLOW if selezionato else COLOR_GRAY
        g2d.set_color(dot_color)
        g2d.fill_circle((bx - 15, cy), 6)
        g2d.fill_circle((bx + _BTN_W + 15, cy), 6)

        text_color = COLOR_YELLOW if selezionato else COLOR_WHITE
        g2d.set_color(text_color)
        g2d.draw_text(label, (cx, cy), 24)

    def _disegna_cursore_pacman(self) -> None:
        """Disegna un Pac-Man stilizzato vicino alla
        voce selezionata con animazione"""
        cy = _BTNS[self._voce_sel]
        offset_x = 5 if (self._anim_tick // 10) % 2 == 0 else 0
        rx = self._cw // 2 - _BTN_W // 2 - 40 + offset_x

        # Pac-man corpo
        g2d.set_color(COLOR_YELLOW)
        g2d.fill_circle((rx, cy), 16)

        # Pallino 'cibo' che punta al menu
        g2d.set_color(COLOR_WHITE)
        g2d.fill_circle((rx + 22, cy), 4)

    def _disegna_decorazioni_basse(self) -> None:
        """Disegna una piccola parata di fantasmini nella parte bassa"""
        bottom_y = self._ch - 40
        fantasmi = [COLOR_RED, COLOR_PINK, COLOR_CYAN, COLOR_ORANGE]

        for i, color in enumerate(fantasmi):
            fx = 120 + i * 110
            g2d.set_color(color)
            g2d.fill_circle((fx, bottom_y), 15)

            # Occhi fantasma
            g2d.set_color(COLOR_WHITE)
            g2d.fill_circle((fx - 5, bottom_y - 3), 4)
            g2d.fill_circle((fx + 5, bottom_y - 3), 4)
            g2d.set_color(COLOR_BLUE)
            g2d.fill_circle((fx - 5, bottom_y - 3), 2)
            g2d.fill_circle((fx + 5, bottom_y - 3), 2)

    def _disegna_schermata_istruzioni(self) -> None:
        """Overlay semitrasparente con le istruzioni di Pac-Man"""
        # Sfondo scuro semitrasparente
        g2d.set_color((0, 0, 0, 230))
        g2d.draw_rect((0, 0), (self._cw, self._ch))

        # Riquadro centrale bordato di blu
        box_w, box_h = 480, 360
        box_x = self._cw // 2 - box_w // 2
        box_y = self._ch // 2 - box_h // 2
        g2d.set_color((0, 0, 30, 240))
        g2d.draw_rect((box_x, box_y), (box_w, box_h))

        # Bordo Blu Neonato Stile Maze
        g2d.set_color(COLOR_BLUE)
        g2d.draw_line((box_x, box_y), (box_x + box_w, box_y), 3)
        g2d.draw_line((box_x + box_w, box_y), (box_x + box_w, box_y + box_h), 3)
        g2d.draw_line((box_x + box_w, box_y + box_h), (box_x, box_y + box_h), 3)
        g2d.draw_line((box_x, box_y + box_h), (box_x, box_y), 3)

        cx = self._cw // 2

        # Titolo
        g2d.set_color(COLOR_YELLOW)
        g2d.draw_text("COME SI GIOCA", (cx, box_y + 35), 28)

        # Controlli
        righe = [
            ("↑ / W", "Spostati verso l'Alto"),
            ("↓ / S", "Spostati verso il Basso"),
            ("← / A", "Spostati a Sinistra"),
            ("→ / D", "Spostati a Destra"),
        ]
        y0 = box_y + 90
        for i, (tasto, desc) in enumerate(righe):
            y = y0 + i * 38
            g2d.set_color(COLOR_CYAN)
            g2d.draw_text(tasto, (box_x + 120, y), 20)
            g2d.set_color(COLOR_WHITE)
            g2d.draw_text(desc, (box_x + 310, y), 18)

        # Obiettivo
        g2d.set_color(COLOR_YELLOW)
        g2d.draw_text(
            "Obiettivo: Mangia tutti i pallini", (cx, box_y + 260), 18
        )
        g2d.set_color(COLOR_RED)
        g2d.draw_text(
            "ed evita i fanstasmi per vincere!", (cx, box_y + 285), 18
        )

        # Messaggio di chiusura
        g2d.set_color(COLOR_GRAY)
        g2d.draw_text(
            "Premi INVIO, ESC o clicca per tornare", (cx, box_y + 330), 15
        )