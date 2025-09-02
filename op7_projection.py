import tkinter as tk
import math

class ProjectionGUI:
    def __init__(self, master, main_menu_callback=None): # Modificado
        self.master = master
        self.master.title("Visualizador de Projeções 3D")
        self.main_menu_callback = main_menu_callback # Modificado

        self.vertices = [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
        self.edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
        self.angle_x = tk.DoubleVar(value=0)
        self.angle_y = tk.DoubleVar(value=0)
        self.angle_z = tk.DoubleVar(value=0)
        self.projection_type = tk.StringVar(value="perspective")
        self.camera_distance = tk.DoubleVar(value=5)

        main_frame = tk.Frame(master)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(main_frame, width=500, height=500, bg='black')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        controls_frame = tk.Frame(main_frame, padx=10)
        controls_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botão para voltar ao menu principal (Modificado)
        if self.main_menu_callback:
            self.back_button = tk.Button(controls_frame, text="Voltar ao Menu", command=self._go_back)
            self.back_button.pack(pady=(0, 10))

        self._create_slider(controls_frame, "Rotação X", self.angle_x, -180, 180)
        self._create_slider(controls_frame, "Rotação Y", self.angle_y, -180, 180)
        self._create_slider(controls_frame, "Rotação Z", self.angle_z, -180, 180)
        proj_frame = tk.LabelFrame(controls_frame, text="Projeção", padx=5, pady=5)
        proj_frame.pack(pady=10, fill=tk.X)
        tk.Radiobutton(proj_frame, text="Ortogonal", variable=self.projection_type, value="orthographic", command=self._update_display).pack(anchor=tk.W)
        tk.Radiobutton(proj_frame, text="Perspectiva", variable=self.projection_type, value="perspective", command=self._update_display).pack(anchor=tk.W)
        self.dist_slider = self._create_slider(proj_frame, "Distância Câmera", self.camera_distance, 1, 20)
        self._update_display()

    def _go_back(self): # Modificado
        self.master.destroy()
        self.main_menu_callback()

    def _create_slider(self, parent, label, var, from_, to):
        frame = tk.Frame(parent)
        frame.pack(pady=2, fill=tk.X)
        tk.Label(frame, text=label).pack()
        slider = tk.Scale(frame, variable=var, from_=from_, to=to, orient=tk.HORIZONTAL, resolution=0.1)
        slider.bind("<Motion>", self._update_display)
        slider.pack(fill=tk.X)
        return slider

    def _update_display(self, event=None):
        self.canvas.delete("all")
        rad_x, rad_y, rad_z = math.radians(self.angle_x.get()), math.radians(self.angle_y.get()), math.radians(self.angle_z.get())
        rot_x, rot_y, rot_z = self._create_rotation_x(rad_x), self._create_rotation_y(rad_y), self._create_rotation_z(rad_z)
        rot_matrix = self._multiply_matrices(self._multiply_matrices(rot_z, rot_y), rot_x)
        projected_points = []
        for vertex in self.vertices:
            rotated = self._multiply_matrix_vector(rot_matrix, vertex + (1,))
            rotated = (rotated[0], rotated[1], rotated[2] + 5) # z_offset
            if self.projection_type.get() == "orthographic":
                px, py = rotated[0], rotated[1]
                self.dist_slider.config(state=tk.DISABLED)
            else:
                self.dist_slider.config(state=tk.NORMAL)
                dist = self.camera_distance.get()
                factor = dist / rotated[2] if rotated[2] != 0 else 1
                px, py = rotated[0] * factor, rotated[1] * factor
            screen_x = self.canvas.winfo_width() / 2 + px * 50
            screen_y = self.canvas.winfo_height() / 2 - py * 50
            projected_points.append((screen_x, screen_y))
        for edge in self.edges:
            p1, p2 = projected_points[edge[0]], projected_points[edge[1]]
            self.canvas.create_line(p1, p2, fill='cyan', width=2)

    def _create_rotation_x(self,r): c,s=math.cos(r),math.sin(r); return[[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]]
    def _create_rotation_y(self,r): c,s=math.cos(r),math.sin(r); return[[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]]
    def _create_rotation_z(self,r): c,s=math.cos(r),math.sin(r); return[[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]]
    def _multiply_matrix_vector(self, m, v):
        res = [0]*4
        for i in range(4):
            for j in range(4): res[i]+=m[i][j]*v[j]
        return tuple(res)
    def _multiply_matrices(self, m1, m2):
        res = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4): res[i][j]+=m1[i][k]*m2[k][j]
        return res

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectionGUI(root)
    root.mainloop()