import tkinter as tk

class BresenhamGUI:
    def __init__(self, master, main_menu_callback=None): # Modificado
        self.master = master
        self.master.title("Visualizador do Algoritmo de Bresenham")
        self.main_menu_callback = main_menu_callback # Modificado

        self.PIXEL_SIZE = 20
        self.GRID_WIDTH = 30
        self.GRID_HEIGHT = 30
        self.start_point = None
        
        button_frame = tk.Frame(master) # Modificado
        button_frame.pack(pady=5)

        self.clear_button = tk.Button(button_frame, text="Limpar", command=self.clear_canvas) # Modificado
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Botão para voltar ao menu principal (Modificado)
        if self.main_menu_callback:
            self.back_button = tk.Button(button_frame, text="Voltar ao Menu", command=self._go_back)
            self.back_button.pack(side=tk.LEFT, padx=5)
        
        canvas_width = self.GRID_WIDTH * self.PIXEL_SIZE
        canvas_height = self.GRID_HEIGHT * self.PIXEL_SIZE
        self.canvas = tk.Canvas(master, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack(pady=10, padx=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.draw_grid()
    
    # Nova função para voltar ao menu (Modificado)
    def _go_back(self):
        self.master.destroy()
        self.main_menu_callback()

    def draw_grid(self):
        for i in range(0, self.GRID_WIDTH * self.PIXEL_SIZE, self.PIXEL_SIZE):
            self.canvas.create_line(i, 0, i, self.GRID_HEIGHT * self.PIXEL_SIZE, fill='#e0e0e0')
        for i in range(0, self.GRID_HEIGHT * self.PIXEL_SIZE, self.PIXEL_SIZE):
            self.canvas.create_line(0, i, self.GRID_WIDTH * self.PIXEL_SIZE, i, fill='#e0e0e0')

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.start_point = None

    def draw_pixel(self, x, y, color="black"):
        x1 = x * self.PIXEL_SIZE
        y1 = y * self.PIXEL_SIZE
        x2 = x1 + self.PIXEL_SIZE
        y2 = y1 + self.PIXEL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    def bresenham(self, x1, y1, x2, y2):
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        x, y = x1, y1
        if dx > dy:
            err = dx / 2.0
            while x != x2:
                points.append((x, y))
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y2:
                points.append((x, y))
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy
        points.append((x, y))
        return points

    def on_canvas_click(self, event):
        grid_x = event.x // self.PIXEL_SIZE
        grid_y = event.y // self.PIXEL_SIZE
        if self.start_point is None:
            self.start_point = (grid_x, grid_y)
            self.draw_pixel(grid_x, grid_y, "blue")
        else:
            end_point = (grid_x, grid_y)
            self.draw_pixel(grid_x, grid_y, "red")
            x1, y1 = self.start_point
            x2, y2 = end_point
            line_points = self.bresenham(x1, y1, x2, y2)
            for point in line_points[1:-1]:
                self.draw_pixel(point[0], point[1], "black")
            self.start_point = None

if __name__ == "__main__":
    root = tk.Tk()
    app = BresenhamGUI(root)
    root.mainloop()