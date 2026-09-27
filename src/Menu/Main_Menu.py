import math
import pygame
import lib.g2d as g2d

BACKGROUND = "assets/img/Backgound_MainMenu.jpeg"

COLOR_BLACK  = (0, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE  = (255, 255, 255)
COLOR_BLUE   = (0, 0, 255)
COLOR_RED    = (255, 0, 0)
COLOR_CYAN   = (0, 255, 255)
COLOR_PINK   = (255, 184, 255)
COLOR_ORANGE = (255, 184, 82)
COLOR_GRAY   = (120, 120, 120)

_GHOST_SWING_AMPL = 12
_GHOST_SWING_SPEED = 0.08

class Main_Menu:
    def __init__(self, canvas_w: int, canvas_h: int):
        self._cw = canvas_w
        self._ch = canvas_h

        self._voce_sel = 0  # 0=GIOCA, 1=COME SI GIOCA, 2=ESCI
        self._anim_tick = 0
        self._mostra_istruzioni = False

        self._avvia = False
        self._esci = False

        self._btn_w = int(self._cw * 0.70)
        self._btn_h = 42
        
        self._btns_y = [
            int(self._ch * 0.46),
            int(self._ch * 0.58),
            int(self._ch * 0.70),
        ]

    @property
    def avvia(self) -> bool:
        return self._avvia

    @property
    def esci(self) -> bool:
        return self._esci

    def aggiorna(self) -> None:
        self._avvia = False
        self._esci = False
        self._anim_tick += 1

        if self._mostra_istruzioni:
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
        up = g2d.key_pressed("Up") or g2d.key_pressed("ArrowUp") or g2d.key_pressed("w") or g2d.key_pressed("W")
        down = g2d.key_pressed("Down") or g2d.key_pressed("ArrowDown") or g2d.key_pressed("s") or g2d.key_pressed("S")
        enter = g2d.key_pressed("Enter") or g2d.key_pressed("Return") or g2d.key_pressed("Spacebar") or g2d.key_pressed(" ")

        if up:
            self._voce_sel = (self._voce_sel - 1) % 3
        elif down:
            self._voce_sel = (self._voce_sel + 1) % 3

        if enter:
            self._conferma()

    def _gestisci_mouse(self) -> None:
        if not g2d.mouse_clicked():
            return

        mx, my = g2d.mouse_pos()
        bx = self._cw // 2 - self._btn_w // 2
        for i, cy in enumerate(self._btns_y):
            if bx <= mx <= bx + self._btn_w:
                if cy - self._btn_h // 2 <= my <= cy + self._btn_h // 2:
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

    def disegna(self) -> None:
        g2d.clear_canvas()
        self._disegna_sfondo()
        self._disegna_logo()
        self._disegna_sottotitolo()
        self._disegna_bottone("GIOCA", self._btns_y[0], self._voce_sel == 0)
        self._disegna_bottone("COME SI GIOCA", self._btns_y[1], self._voce_sel == 1)
        self._disegna_bottone("ESCI", self._btns_y[2], self._voce_sel == 2)
        self._disegna_cursore_pacman()
        self._disegna_decorazioni_basse()

        if self._mostra_istruzioni:
            self._disegna_schermata_istruzioni()

    def _disegna_sfondo(self) -> None:
        try:
            raw = g2d._loaded[BACKGROUND]
            scaled = pygame.transform.scale(raw, (self._cw, self._ch))
            canvas = g2d.drawing_surface()
            canvas.blit(scaled, (0, 0))
            g2d.set_color((0, 0, 0, 180))
            g2d.draw_rect((0, 0), (self._cw, self._ch))
        except Exception:
            g2d.set_color(COLOR_BLACK)
            g2d.draw_rect((0, 0), (self._cw, self._ch))

    def _disegna_logo(self) -> None:
        cx = self._cw // 2
        y = int(self._ch * 0.15)
        g2d.set_color(COLOR_BLACK)
        g2d.draw_text("PACMAN", (cx + 2, y + 2), 48)
        g2d.set_color(COLOR_YELLOW)
        g2d.draw_text("PACMAN", (cx, y), 48)

    def _disegna_sottotitolo(self) -> None:
        g2d.set_color(COLOR_CYAN)
        g2d.draw_text("Frecce / WASD • INVIO", (self._cw // 2, int(self._ch * 0.28)), 16)

    def _disegna_bottone(self, label: str, cy: int, selezionato: bool) -> None:
        cx = self._cw // 2
        bx = cx - self._btn_w // 2
        by = cy - self._btn_h // 2

        alpha = 220 if selezionato else 140
        g2d.set_color((0, 0, 0, alpha))
        g2d.draw_rect((bx, by), (self._btn_w, self._btn_h))

        border = COLOR_YELLOW if selezionato else COLOR_BLUE
        g2d.set_color(border)
        g2d.draw_line((bx, by), (bx + self._btn_w, by), 2)
        g2d.draw_line((bx + self._btn_w, by), (bx + self._btn_w, by + self._btn_h), 2)
        g2d.draw_line((bx + self._btn_w, by + self._btn_h), (bx, by + self._btn_h), 2)
        g2d.draw_line((bx, by + self._btn_h), (bx, by), 2)

        dot_color = COLOR_YELLOW if selezionato else COLOR_GRAY
        g2d.set_color(dot_color)
        g2d.draw_circle((bx - 12, cy), 5)
        g2d.draw_circle((bx + self._btn_w + 12, cy), 5)

        testo_color = COLOR_YELLOW if selezionato else COLOR_WHITE
        g2d.set_color(testo_color)
        g2d.draw_text(label, (cx, cy), 20)

    def _disegna_cursore_pacman(self) -> None:
        cy = self._btns_y[self._voce_sel]
        offset_x = 3 if (self._anim_tick // 10) % 2 == 0 else 0
        rx = self._cw // 2 - self._btn_w // 2 - 28 + offset_x

        g2d.set_color(COLOR_BLACK)
        g2d.draw_circle((rx, cy), 12)
        g2d.set_color(COLOR_YELLOW)
        g2d.draw_circle((rx, cy), 10)
        g2d.set_color(COLOR_WHITE)
        g2d.draw_circle((rx + 14, cy), 3)

    def _disegna_decorazioni_basse(self) -> None:
        bottom_y = self._ch - 30
        fantasmi = [COLOR_RED, COLOR_PINK, COLOR_CYAN, COLOR_ORANGE]

        shift = int(_GHOST_SWING_AMPL * math.sin(self._anim_tick * _GHOST_SWING_SPEED))
        spacing = 50
        gruppo_w = spacing * (len(fantasmi) - 1)
        start_x = self._cw // 2 - gruppo_w // 2

        margin = 20
        for i, color in enumerate(fantasmi):
            fx = start_x + i * spacing + shift
            fx = max(margin, min(self._cw - margin, fx))

            g2d.set_color(COLOR_BLACK)
            g2d.draw_circle((fx, bottom_y), 12)
            g2d.set_color(color)
            g2d.draw_circle((fx, bottom_y), 10)

            g2d.set_color(COLOR_WHITE)
            g2d.draw_circle((fx - 3, bottom_y - 2), 3)
            g2d.draw_circle((fx + 3, bottom_y - 2), 3)
            g2d.set_color(COLOR_BLUE)
            g2d.draw_circle((fx - 3, bottom_y - 2), 1)
            g2d.draw_circle((fx + 3, bottom_y - 2), 1)

    def _disegna_schermata_istruzioni(self) -> None:
        g2d.set_color((0, 0, 0, 235))
        g2d.draw_rect((0, 0), (self._cw, self._ch))

        box_w, box_h = int(self._cw * 0.88), int(self._ch * 0.82)
        box_x = self._cw // 2 - box_w // 2
        box_y = self._ch // 2 - box_h // 2
        
        g2d.set_color((5, 5, 25, 245))
        g2d.draw_rect((box_x, box_y), (box_w, box_h))

        g2d.set_color(COLOR_BLUE)
        g2d.draw_line((box_x, box_y), (box_x + box_w, box_y), 3)
        g2d.draw_line((box_x + box_w, box_y), (box_x + box_w, box_y + box_h), 3)
        g2d.draw_line((box_x + box_w, box_y + box_h), (box_x, box_y + box_h), 3)
        g2d.draw_line((box_x, box_y + box_h), (box_x, box_y), 3)

        cx = self._cw // 2

        # Titolo
        g2d.set_color(COLOR_YELLOW)
        g2d.draw_text("COME SI GIOCA", (cx, box_y + 35), 26)

        # Controlli disposti in due colonne bilanciate
        righe = [
            ("↑ / W", "Spostati Su"),
            ("↓ / S", "Spostati Giu"),
            ("← / A", "Spostati a Sinistra"),
            ("→ / D", "Spostati a Destra"),
        ]
        y0 = box_y + 90
        for i, (tasto, desc) in enumerate(righe):
            y = y0 + i * 36
            g2d.set_color(COLOR_CYAN)
            g2d.draw_text(tasto, (box_x + int(box_w * 0.30), y), 20)
            g2d.set_color(COLOR_WHITE)
            g2d.draw_text(desc, (box_x + int(box_w * 0.70), y), 18)

        # Obiettivi
        g2d.set_color(COLOR_YELLOW)
        g2d.draw_text("Mangia tutti i pallini!", (cx, box_y + box_h - 100), 20)
        g2d.set_color(COLOR_RED)
        g2d.draw_text("Ed evita i fantasmi!", (cx, box_y + box_h - 70), 20)

        # Footer
        g2d.set_color(COLOR_GRAY)
        g2d.draw_text("Premi INVIO o Clicca per uscire", (cx, box_y + box_h - 30), 14)