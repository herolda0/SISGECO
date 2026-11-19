
import customtkinter as ctk
from view.navigation import Navigation

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GestaoComercialApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SISGECO | Gestão Comercial")
        self.geometry("1440x900")
        self.minsize(1100, 700)

        self.after(100, lambda: self.state("zoomed"))

        self.configure(fg_color= "#141820")

        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        self.navigation = Navigation(self.container)
        self.navigation.mostrar_tela("dashboard")


if __name__ == "__main__":
    app = GestaoComercialApp()
    app.mainloop()
