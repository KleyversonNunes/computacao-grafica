import tkinter as tk

class ClippingGUI:
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8
    def __init__(self, master, main_menu_callback=None): # Modificado
        self.master = master
        self.master.title("Visualizador de Algoritmos de Recorte")
        self.main_menu_callback = main_menu_callback # Modificado

        self.draw_mode = tk.StringVar(value="line")
        self.line_points, self.polygon_points = [], []
        self.polygon_closed = False
        self.xw_min, self.yw_min = 150, 100
        self.xw_max, self.yw_max = 450, 400

        controls_frame = tk.Frame(master)
        controls_frame.pack(pady=5)
        tk.Radiobutton(controls_frame, text="Desenhar Linha", variable=self.draw_mode, value="line", command=self.reset_drawing).pack(side=tk.LEFT)
        tk.Radiobutton(controls_frame, text="Desenhar Polígono", variable=self.draw_mode, value="polygon", command=self.reset_drawing).pack(side=tk.LEFT, padx=10)
        self.close_poly_button = tk.Button(controls_frame, text="Fechar Polígono", command=self.close_polygon_and_clip, state=tk.DISABLED)
        self.close_poly_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = tk.Button(controls_frame, text="Limpar Tudo", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Botão para voltar ao menu principal (Modificado)
        if self.main_menu_callback:
            self.back_button = tk.Button(controls_frame, text="Voltar ao Menu", command=self._go_back)
            self.back_button.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(master, width=600, height=500, bg='white')
        self.canvas.pack(pady=10, padx=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.draw_clipping_window()

    def _go_back(self): # Modificado
        self.master.destroy()
        self.main_menu_callback()

    def reset_drawing(self):
        self.line_points, self.polygon_points = [], []
        self.polygon_closed = False
        state = tk.NORMAL if self.draw_mode.get() == "polygon" else tk.DISABLED
        self.close_poly_button.config(state=state)

    def draw_clipping_window(self):
        self.canvas.create_rectangle(self.xw_min, self.yw_min, self.xw_max, self.yw_max, outline='blue', dash=(4, 2), tags="clip_window")

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        mode = self.draw_mode.get()
        if mode == "line":
            self.line_points.append((x, y))
            if len(self.line_points) == 2:
                p1, p2 = self.line_points
                self.canvas.create_line(p1, p2, fill='gray', dash=(2,2), width=1, tags="original")
                self.cohen_sutherland_clip(p1[0], p1[1], p2[0], p2[1])
                self.line_points = []
        elif mode == "polygon" and not self.polygon_closed:
            self.polygon_points.append((x, y))
            if len(self.polygon_points) > 1:
                p1, p2 = self.polygon_points[-2], self.polygon_points[-1]
                self.canvas.create_line(p1, p2, fill='gray', width=2, tags="original")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_clipping_window()
        self.reset_drawing()

    def _compute_outcode(self, x, y):
        code = self.INSIDE
        if x < self.xw_min: code |= self.LEFT
        elif x > self.xw_max: code |= self.RIGHT
        if y < self.yw_min: code |= self.BOTTOM
        elif y > self.yw_max: code |= self.TOP
        return code

    def cohen_sutherland_clip(self, x1, y1, x2, y2):
        outcode1, outcode2 = self._compute_outcode(x1, y1), self._compute_outcode(x2, y2)
        accept = False
        while True:
            if not (outcode1 | outcode2):
                accept = True; break
            elif outcode1 & outcode2: break
            else:
                x, y = 0, 0
                outcode_out = outcode1 if outcode1 else outcode2
                if outcode_out & self.TOP:
                    x = x1 + (x2 - x1) * (self.yw_max - y1) / (y2 - y1)
                    y = self.yw_max
                elif outcode_out & self.BOTTOM:
                    x = x1 + (x2 - x1) * (self.yw_min - y1) / (y2 - y1)
                    y = self.yw_min
                elif outcode_out & self.RIGHT:
                    y = y1 + (y2 - y1) * (self.xw_max - x1) / (x2 - x1)
                    x = self.xw_max
                elif outcode_out & self.LEFT:
                    y = y1 + (y2 - y1) * (self.xw_min - x1) / (x2 - x1)
                    x = self.xw_min
                if outcode_out == outcode1:
                    x1, y1 = x, y
                    outcode1 = self._compute_outcode(x1, y1)
                else:
                    x2, y2 = x, y
                    outcode2 = self._compute_outcode(x2, y2)
        if accept:
            self.canvas.create_line(x1, y1, x2, y2, fill='red', width=2, tags="clipped")

    def close_polygon_and_clip(self):
        if len(self.polygon_points) < 3: return
        p_start, p_end = self.polygon_points[0], self.polygon_points[-1]
        self.canvas.create_line(p_end, p_start, fill='gray', width=2, tags="original")
        clipped_polygon = self.sutherland_hodgman_clip(self.polygon_points)
        if clipped_polygon:
            self.canvas.create_polygon(clipped_polygon, fill='mediumorchid', outline='black', width=2, tags="clipped")
        self.polygon_closed = True
        self.close_poly_button.config(state=tk.DISABLED)

    def sutherland_hodgman_clip(self, subject_polygon):
        def _clip(poly, edge, is_inside):
            clipped_poly = []
            p1 = poly[-1]
            for p2 in poly:
                p1_inside, p2_inside = is_inside(p1, edge), is_inside(p2, edge)
                if p1_inside and p2_inside: clipped_poly.append(p2)
                elif p1_inside and not p2_inside: clipped_poly.append(self._get_intersection(p1, p2, edge))
                elif not p1_inside and p2_inside:
                    clipped_poly.append(self._get_intersection(p1, p2, edge))
                    clipped_poly.append(p2)
                p1 = p2
            return clipped_poly
        clipped = _clip(subject_polygon, 'left', lambda p, e: p[0] >= self.xw_min)
        clipped = _clip(clipped, 'right', lambda p, e: p[0] <= self.xw_max)
        clipped = _clip(clipped, 'top', lambda p, e: p[1] <= self.yw_max)
        clipped = _clip(clipped, 'bottom', lambda p, e: p[1] >= self.yw_min)
        return clipped

    def _get_intersection(self, p1, p2, edge):
        (x1, y1), (x2, y2) = p1, p2
        dx, dy = x2 - x1, y2 - y1
        if edge == 'left': x, y = self.xw_min, y1 + dy * (self.xw_min - x1) / dx if dx != 0 else y1
        elif edge == 'right': x, y = self.xw_max, y1 + dy * (self.xw_max - x1) / dx if dx != 0 else y1
        elif edge == 'top': y, x = self.yw_max, x1 + dx * (self.yw_max - y1) / dy if dy != 0 else x1
        elif edge == 'bottom': y, x = self.yw_min, x1 + dx * (self.yw_min - y1) / dy if dy != 0 else x1
        return (x, y)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClippingGUI(root)
    root.mainloop()