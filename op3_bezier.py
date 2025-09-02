import tkinter as tk
import math

class BezierCurveGUI:
    def __init__(self, master, main_menu_callback=None): # Modificado
        self.master = master
        self.master.title("Visualizador de Curva de Bézier (Polinômios de Bernstein)")
        self.main_menu_callback = main_menu_callback # Modificado

        self.PIXEL_SIZE = 5
        self.GRID_WIDTH = 120
        self.GRID_HEIGHT = 100
        self.control_points = []
        
        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)
        self.draw_button = tk.Button(button_frame, text="Desenhar Curva", command=self.draw_curve)
        self.draw_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = tk.Button(button_frame, text="Limpar", command=self.clear_canvas)
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
        pass

    def clear_canvas(self):
        self.canvas.delete("all")
        self.control_points = []
        self.draw_grid()

    def combinations(self, n, i):
        return math.factorial(n) / (math.factorial(i) * math.factorial(n - i))

    def bernstein_poly(self, i, n, t):
        return self.combinations(n, i) * (t**i) * ((1 - t)**(n - i))

    def draw_curve(self):
        if len(self.control_points) < 2:
            return
        self.canvas.delete("curve")
        n = len(self.control_points) - 1
        curve_points = []
        num_steps = 200
        for t_step in range(num_steps + 1):
            t = t_step / num_steps
            x_on_curve, y_on_curve = 0.0, 0.0
            for i, point in enumerate(self.control_points):
                bernstein_val = self.bernstein_poly(i, n, t)
                x_on_curve += point[0] * bernstein_val
                y_on_curve += point[1] * bernstein_val
            curve_points.append((x_on_curve, y_on_curve))
        canvas_curve_points = []
        for p in curve_points:
            canvas_curve_points.append(p[0] * self.PIXEL_SIZE)
            canvas_curve_points.append(p[1] * self.PIXEL_SIZE)
        self.canvas.create_line(canvas_curve_points, fill='blue', width=2, tags="curve")

    def on_canvas_click(self, event):
        grid_x = event.x / self.PIXEL_SIZE
        grid_y = event.y / self.PIXEL_SIZE
        self.control_points.append((grid_x, grid_y))
        radius = 4
        self.canvas.create_oval(
            event.x - radius, event.y - radius,
            event.x + radius, event.y + radius,
            fill='red', outline='black', tags="point"
        )
        if len(self.control_points) > 1:
            p1 = self.control_points[-2]
            p2 = self.control_points[-1]
            self.canvas.create_line(
                p1[0] * self.PIXEL_SIZE, p1[1] * self.PIXEL_SIZE,
                p2[0] * self.PIXEL_SIZE, p2[1] * self.PIXEL_SIZE,
                fill='gray', dash=(2, 2), tags="point_line"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = BezierCurveGUI(root)
    root.mainloop()