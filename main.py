import customtkinter as ctk
from view.dashboard_view import DashboardView


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class GestaoComercialApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SISGECO | Gestão Comercial")
        self.geometry("1440x900")
        self.minsize(1100, 700)

        self.configure(fg_color="#F5F7FA")

        dashboard = DashboardView(self)
        dashboard.pack(fill="both", expand=True)


if __name__ == "__main__":

    app = GestaoComercialApp()
    app.mainloop()