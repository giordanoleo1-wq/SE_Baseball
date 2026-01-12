import flet as ft
from UI.alert import AlertManager


class View:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "SE_Baseball"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        self.alert = AlertManager(page)
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def update(self):
        self.page.update()

    def load_interface(self):
        # Titolo
        self.txt_titolo = ft.Text(
            value="Gestione Squadre di Baseball",
            size=30,
            weight=ft.FontWeight.BOLD
        )

        # Dropdown anno (VUOTA)
        self.dd_anno = ft.Dropdown(
            label="Anno",
            width=200,
            options= self.controller.handle_dd_anno(),
            on_change=self.controller.handle_squadre_anno
        )


        # Riga 1
        row1 = ft.Row(
            [
                ft.Container(self.txt_titolo, width=500),
                ft.Container(self.dd_anno, width=250),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # ListView squadre
        self.txt_out_squadre = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=False
        )

        cont = ft.Container(
            self.txt_out_squadre,
            width=300,
            height=200,
            bgcolor=ft.Colors.SURFACE
        )

        self.pulsante_crea_grafo = ft.ElevatedButton(
            text="Crea Grafo",
            on_click=self.controller.handle_crea_grafo
        )

        row2 = ft.Row(
            [cont, self.pulsante_crea_grafo],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.END
        )

        # Dropdown squadra + bottoni
        self.dd_squadra = ft.Dropdown(label="Squadra", width=200)

        self.pulsante_dettagli = ft.ElevatedButton(
            text="Dettagli",
            on_click=self.controller.handle_dettagli
        )

        self.pulsante_percorso = ft.ElevatedButton(
            text="Percorso",
            on_click=self.controller.handle_percorso
        )

        row3 = ft.Row(
            [
                ft.Container(self.dd_squadra, width=250),
                ft.Container(self.pulsante_dettagli, width=250),
                ft.Container(self.pulsante_percorso, width=250),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Risultati
        self.txt_risultato = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True
        )

        # Layout finale
        self.page.add(
            row1,
            ft.Divider(),
            row2,
            ft.Divider(),
            row3,
            self.txt_risultato
        )

        self.dd_anno.options = self.controller.handle_dd_anno()
        self.page.update()
