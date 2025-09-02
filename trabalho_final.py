import tkinter as tk
from tkinter import font

# Importa as classes de cada um dos arquivos de algoritmos
from op1_breshnham import BresenhamGUI
from op2_midpoint_circle import MidpointCircleGUI
from op3_bezier import BezierCurveGUI
from op4_fill import FillAlgorithmGUI
from op5_clipping import ClippingGUI
from op6_transforms import AdvancedTransformationsGUI
from op7_projection import ProjectionGUI

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Trabalho Final - Computação Gráfica")
        self.master.geometry("400x450")

        # Frame principal para centralizar o conteúdo
        main_frame = tk.Frame(master, padx=20, pady=20)
        main_frame.pack(expand=True)

        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        button_font = font.Font(family="Helvetica", size=12)

        tk.Label(main_frame, text="Menu Principal", font=title_font).pack(pady=(0, 20))

        # Dicionário com o nome do botão e a classe do algoritmo correspondente
        self.menu_options = {
            "1 - Linha (Bresenham)": BresenhamGUI,
            "2 - Círculo (Ponto Médio)": MidpointCircleGUI,
            "3 - Curvas (Bézier)": BezierCurveGUI,
            "4 - Preenchimento": FillAlgorithmGUI,
            "5 - Recorte": ClippingGUI,
            "6 - Transformações 2D": AdvancedTransformationsGUI,
            "7 - Projeções 3D": ProjectionGUI
        }

        # Cria um botão para cada opção do menu
        for text, app_class in self.menu_options.items():
            button = tk.Button(
                main_frame,
                text=text,
                font=button_font,
                width=25,
                command=lambda ac=app_class: self.launch_app(ac)
            )
            button.pack(pady=5)

        # Botão de Sair
        exit_button = tk.Button(
            main_frame,
            text="8 - Sair",
            font=button_font,
            width=25,
            command=master.destroy
        )
        exit_button.pack(pady=5)

    def launch_app(self, app_class):
        """Esconde o menu principal e abre a janela do algoritmo selecionado."""
        self.master.withdraw()  # Esconde a janela principal
        app_window = tk.Toplevel(self.master)
        
        # Inicia a classe do algoritmo, passando a nova janela e a função de callback
        app_class(app_window, main_menu_callback=self.show_main_menu)

    def show_main_menu(self):
        """Mostra o menu principal novamente."""
        self.master.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()