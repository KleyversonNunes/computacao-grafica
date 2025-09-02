import tkinter as tk
import sys

sys.setrecursionlimit(20000)

class FillAlgorithmGUI:
    def __init__(self, master, main_menu_callback=None): # Modificado
        self.master = master
        self.master.title("Visualizador de Algoritmos de Preenchimento")
        self.main_menu_callback = main_menu_callback # Modificado

        self.CANVAS_WIDTH = 600
        self.CANVAS_HEIGHT = 500
        self.polygon_points = []
        self.polygon_closed = False
        self.pixel_grid = [[0 for _ in range(self.CANVAS_WIDTH)] for _ in range(self.CANVAS_HEIGHT)]

        controls_frame = tk.Frame(master)
        controls_frame.pack(pady=5)
        self.close_poly_button = tk.Button(controls_frame, text="Fechar Polígono", command=self.close_polygon)
        self.close_poly_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = tk.Button(controls_frame, text="Limpar Tudo", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Botão para voltar ao menu principal (Modificado)
        if self.main_menu_callback:
            self.back_button = tk.Button(controls_frame, text="Voltar ao Menu", command=self._go_back)
            self.back_button.pack(side=tk.LEFT, padx=5)

        self.algo_choice = tk.StringVar(value="scanline")
        tk.Radiobutton(controls_frame, text="Recursivo (Flood Fill)", variable=self.algo_choice, value="floodfill").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(controls_frame, text="Scanline", variable=self.algo_choice, value="scanline").pack(side=tk.LEFT, padx=5)
        self.canvas = tk.Canvas(master, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg='white')
        self.canvas.pack(pady=10, padx=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def _go_back(self): # Modificado
        self.master.destroy()
        self.main_menu_callback()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        if not self.polygon_closed:
            self.polygon_points.append((x, y))
            if len(self.polygon_points) > 1:
                p1, p2 = self.polygon_points[-2], self.polygon_points[-1]
                self.canvas.create_line(p1, p2, fill='black', width=2)
        else:
            if self.pixel_grid[y][x] == 0:
                fill_color = "skyblue"
                if self.algo_choice.get() == "floodfill":
                    self.flood_fill(x, y, fill_color)
                else:
                    self.scanline_fill(x, y, fill_color)

    def close_polygon(self):
        if not self.polygon_points or len(self.polygon_points) < 3: return
        p_start, p_end = self.polygon_points[0], self.polygon_points[-1]
        self.canvas.create_line(p_end, p_start, fill='black', width=2)
        all_points = self.polygon_points + [self.polygon_points[0]]
        for i in range(len(all_points) - 1):
            self.rasterize_line_on_grid(all_points[i], all_points[i+1])
        self.polygon_closed = True
        self.close_poly_button.config(state=tk.DISABLED)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.polygon_points = []
        self.polygon_closed = False
        self.pixel_grid = [[0 for _ in range(self.CANVAS_WIDTH)] for _ in range(self.CANVAS_HEIGHT)]
        self.close_poly_button.config(state=tk.NORMAL)

    def rasterize_line_on_grid(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            if 0 <= y1 < self.CANVAS_HEIGHT and 0 <= x1 < self.CANVAS_WIDTH:
                self.pixel_grid[y1][x1] = 1
            if x1 == x2 and y1 == y2: break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def flood_fill(self, x, y, fill_color):
        if not (0 <= x < self.CANVAS_WIDTH and 0 <= y < self.CANVAS_HEIGHT) or self.pixel_grid[y][x] != 0:
            return
        self.pixel_grid[y][x] = 2
        self.canvas.create_rectangle(x, y, x, y, outline=fill_color, fill=fill_color)
        self.flood_fill(x + 1, y, fill_color)
        self.flood_fill(x - 1, y, fill_color)
        self.flood_fill(x, y + 1, fill_color)
        self.flood_fill(x, y - 1, fill_color)

    def scanline_fill(self, x, y, fill_color):
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            lx = x
            while lx > 0 and self.pixel_grid[y][lx - 1] == 0: lx -= 1
            rx = x
            while rx < self.CANVAS_WIDTH - 1 and self.pixel_grid[y][rx + 1] == 0: rx += 1
            self.canvas.create_line(lx, y, rx, y, fill=fill_color)
            for i in range(lx, rx + 1):
                self.pixel_grid[y][i] = 2
            for scan_y in [y - 1, y + 1]:
                if 0 <= scan_y < self.CANVAS_HEIGHT:
                    for scan_x in range(lx, rx + 1):
                        if self.pixel_grid[scan_y][scan_x] == 0:
                            stack.append((scan_x, scan_y))

if __name__ == "__main__":
    root = tk.Tk()
    app = FillAlgorithmGUI(root)
    root.mainloop()