import tkinter as tk
import math

class MidpointCircleGUI:
    def __init__(self, master, main_menu_callback=None): # Modificado
        self.master = master
        self.master.title("Visualizador do Algoritmo de Círculo do Ponto Médio")
        self.main_menu_callback = main_menu_callback # Modificado

        self.PIXEL_SIZE = 15
        self.GRID_WIDTH = 40
        self.GRID_HEIGHT = 40
        self.center_point = None

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

    def _go_back(self): # Modificado
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
        self.center_point = None

    def draw_pixel(self, x, y, color="black"):
        if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
            x1 = x * self.PIXEL_SIZE
            y1 = y * self.PIXEL_SIZE
            x2 = x1 + self.PIXEL_SIZE
            y2 = y1 + self.PIXEL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    def plot_circle_points(self, xc, yc, x, y):
        self.draw_pixel(xc + x, yc + y)
        self.draw_pixel(xc - x, yc + y)
        self.draw_pixel(xc + x, yc - y)
        self.draw_pixel(xc - x, yc - y)
        self.draw_pixel(xc + y, yc + x)
        self.draw_pixel(xc - y, yc + x)
        self.draw_pixel(xc + y, yc - x)
        self.draw_pixel(xc - y, yc - x)

    def midpoint_circle(self, xc, yc, r):
        x = 0
        y = r
        p = 1 - r
        self.plot_circle_points(xc, yc, x, y)
        while x < y:
            x += 1
            if p < 0:
                p += 2 * x + 1
            else:
                y -= 1
                p += 2 * (x - y) + 1
            self.plot_circle_points(xc, yc, x, y)

    def on_canvas_click(self, event):
        grid_x = event.x // self.PIXEL_SIZE
        grid_y = event.y // self.PIXEL_SIZE
        if self.center_point is None:
            self.center_point = (grid_x, grid_y)
            self.draw_pixel(grid_x, grid_y, "blue")
        else:
            xc, yc = self.center_point
            dx = grid_x - xc
            dy = grid_y - yc
            radius = int(round(math.sqrt(dx**2 + dy**2)))
            if radius > 0:
                self.midpoint_circle(xc, yc, radius)
            self.center_point = None

if __name__ == "__main__":
    root = tk.Tk()
    app = MidpointCircleGUI(root)
    root.mainloop()