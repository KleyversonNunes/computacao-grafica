import tkinter as tk
from tkinter import messagebox
import math

class AdvancedTransformationsGUI:
    def __init__(self, master, main_menu_callback=None): # Modificado
        self.master = master
        self.master.title("Editor de Transformações 2D")
        self.main_menu_callback = main_menu_callback # Modificado

        self.user_drawn_points = []
        self.original_polygon = []
        self.transformed_polygon = []
        self.polygon_closed = False

        main_frame = tk.Frame(master)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_width, self.canvas_height = 500, 500
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, bg='white', relief=tk.SUNKEN, borderwidth=1)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        controls_frame = tk.Frame(main_frame, padx=10)
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)
        draw_frame = tk.LabelFrame(controls_frame, text="1. Desenho", padx=10, pady=10)
        draw_frame.pack(fill=tk.X)
        self.close_poly_button = tk.Button(draw_frame, text="Fechar Polígono", command=self._close_polygon)
        self.close_poly_button.pack()
        self.clear_button = tk.Button(draw_frame, text="Limpar Tudo", command=self._clear_all)
        self.clear_button.pack(pady=5)
        
        # Botão para voltar ao menu principal (Modificado)
        if self.main_menu_callback:
            self.back_button = tk.Button(draw_frame, text="Voltar ao Menu", command=self._go_back)
            self.back_button.pack(pady=5)

        self.transform_frame = tk.LabelFrame(controls_frame, text="2. Transformações", padx=10, pady=10)
        self.transform_frame.pack(fill=tk.X, pady=10)
        self.entries = {}
        self._create_entry("Translação X:", "tx", "0.0")
        self._create_entry("Translação Y:", "ty", "0.0")
        self._create_entry("Escala X:", "sx", "1.0")
        self._create_entry("Escala Y:", "sy", "1.0")
        self._create_entry("Rotação (graus):", "angle", "0.0")
        self.pivot_choice = tk.StringVar(value="center")
        tk.Radiobutton(self.transform_frame, text="Pivô: Centro do Objeto", variable=self.pivot_choice, value="center").grid(row=5, columnspan=2, sticky='w')
        tk.Radiobutton(self.transform_frame, text="Pivô: Origem (0,0)", variable=self.pivot_choice, value="origin").grid(row=6, columnspan=2, sticky='w')
        self.apply_button = tk.Button(self.transform_frame, text="Aplicar Transformações", command=self._apply_transformations)
        self.apply_button.grid(row=7, columnspan=2, pady=10)

        coords_frame = tk.LabelFrame(controls_frame, text="3. Coordenadas", padx=10, pady=10)
        coords_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(coords_frame, text="Original:").pack(anchor='w')
        self.original_coords_text = tk.Text(coords_frame, height=8, width=30, state=tk.DISABLED, bg='#f0f0f0')
        self.original_coords_text.pack(fill=tk.X, pady=(0, 5))
        tk.Label(coords_frame, text="Transformado:").pack(anchor='w')
        self.transformed_coords_text = tk.Text(coords_frame, height=8, width=30, state=tk.DISABLED, bg='#f0f0f0')
        self.transformed_coords_text.pack(fill=tk.X)

        self._draw_axes()
        self._set_controls_state(tk.DISABLED)

    def _go_back(self): # Modificado
        self.master.destroy()
        self.main_menu_callback()

    def _create_entry(self, label, key, default_value):
        tk.Label(self.transform_frame, text=label).grid(row=len(self.entries), column=0, sticky='w', pady=2)
        var = tk.StringVar(value=default_value)
        entry = tk.Entry(self.transform_frame, textvariable=var, width=10)
        entry.grid(row=len(self.entries), column=1, sticky='e', pady=2)
        self.entries[key] = (var, entry)

    def on_canvas_click(self, event):
        if self.polygon_closed: return
        self.user_drawn_points.append((event.x, event.y))
        radius = 3
        self.canvas.create_oval(event.x-radius, event.y-radius, event.x+radius, event.y+radius, fill='blue')
        if len(self.user_drawn_points) > 1:
            self.canvas.create_line(self.user_drawn_points[-2], self.user_drawn_points[-1], fill='blue')

    def _close_polygon(self):
        if len(self.user_drawn_points) < 3:
            messagebox.showwarning("Aviso", "Desenhe um polígono com pelo menos 3 vértices.")
            return
        self.polygon_closed = True
        self.close_poly_button.config(state=tk.DISABLED)
        cx, cy = self.canvas_width/2, self.canvas_height/2
        self.original_polygon = [(p[0]-cx, cy-p[1]) for p in self.user_drawn_points]
        self.transformed_polygon = self.original_polygon[:]
        self._draw_polygons()
        self._update_coordinate_display()
        self._set_controls_state(tk.NORMAL)

    def _clear_all(self):
        self.canvas.delete("all")
        self._draw_axes()
        self.user_drawn_points, self.original_polygon, self.transformed_polygon = [], [], []
        self.polygon_closed = False
        self.close_poly_button.config(state=tk.NORMAL)
        self._set_controls_state(tk.DISABLED)
        self._update_coordinate_display()
        self.entries['tx'][0].set("0.0"); self.entries['ty'][0].set("0.0")
        self.entries['sx'][0].set("1.0"); self.entries['sy'][0].set("1.0")
        self.entries['angle'][0].set("0.0")

    def _set_controls_state(self, state):
        for child in self.transform_frame.winfo_children():
            if isinstance(child, (tk.Entry, tk.Radiobutton, tk.Button)):
                child.config(state=state)

    def _draw_axes(self):
        cx, cy = self.canvas_width/2, self.canvas_height/2
        self.canvas.create_line(0, cy, self.canvas_width, cy, fill='gray', dash=(4,2))
        self.canvas.create_line(cx, 0, cx, self.canvas_height, fill='gray', dash=(4,2))
        self.canvas.create_text(cx+5, 10, text="Y", fill="gray")
        self.canvas.create_text(self.canvas_width-10, cy-10, text="X", fill="gray")

    def _draw_polygons(self):
        self.canvas.delete("polygon")
        cx, cy = self.canvas_width/2, self.canvas_height/2
        if self.original_polygon:
            canvas_original = [(p[0]+cx, cy-p[1]) for p in self.original_polygon]
            self.canvas.create_polygon(canvas_original, fill='', outline='gray', width=2, dash=(4,4), tags="polygon")
        canvas_transformed = [(p[0]+cx, cy-p[1]) for p in self.transformed_polygon]
        self.canvas.create_polygon(canvas_transformed, fill='royalblue', outline='black', width=2, tags="polygon")

    def _update_coordinate_display(self):
        def format_coords(poly): return "".join([f"P{i}: ({p[0]:.2f}, {p[1]:.2f})\n" for i, p in enumerate(poly)])
        for txt_widget, poly in [(self.original_coords_text, self.original_polygon), (self.transformed_coords_text, self.transformed_polygon)]:
            txt_widget.config(state=tk.NORMAL)
            txt_widget.delete('1.0', tk.END)
            txt_widget.insert('1.0', format_coords(poly))
            txt_widget.config(state=tk.DISABLED)

    def _apply_transformations(self):
        try:
            params = {k: float(v[0].get()) for k, v in self.entries.items()}
            for _, entry in self.entries.values(): entry.config(bg='white')
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira apenas números válidos.")
            return
        pivot_x, pivot_y = (0, 0)
        if self.pivot_choice.get() == "center":
            pivot_x, pivot_y = self._calculate_center(self.original_polygon)
        to_origin = self._create_translation_matrix(-pivot_x, -pivot_y)
        scale = self._create_scale_matrix(params['sx'], params['sy'])
        rotation = self._create_rotation_matrix(math.radians(params['angle']))
        from_origin = self._create_translation_matrix(pivot_x, pivot_y)
        translation = self._create_translation_matrix(params['tx'], params['ty'])
        tm = self._multiply_matrices(rotation, scale)
        tm = self._multiply_matrices(from_origin, tm)
        tm = self._multiply_matrices(tm, to_origin)
        tm = self._multiply_matrices(translation, tm)
        self.transformed_polygon = [self._transform_point(p, tm) for p in self.original_polygon]
        self._draw_polygons()
        self._update_coordinate_display()

    def _calculate_center(self, polygon):
        if not polygon: return 0, 0
        x_c, y_c = [p[0] for p in polygon], [p[1] for p in polygon]
        return sum(x_c)/len(polygon), sum(y_c)/len(polygon)
    def _create_translation_matrix(self, tx, ty): return [[1,0,tx],[0,1,ty],[0,0,1]]
    def _create_scale_matrix(self, sx, sy): return [[sx,0,0],[0,sy,0],[0,0,1]]
    def _create_rotation_matrix(self, rad): c,s=math.cos(rad),math.sin(rad);return[[c,-s,0],[s,c,0],[0,0,1]]
    def _multiply_matrices(self, m1, m2):
        res=[[0,0,0] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(3): res[i][j]+=m1[i][k]*m2[k][j]
        return res
    def _transform_point(self, point, matrix):
        px, py = point
        return (matrix[0][0]*px+matrix[0][1]*py+matrix[0][2], matrix[1][0]*px+matrix[1][1]*py+matrix[1][2])

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedTransformationsGUI(root)
    root.mainloop()