import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._view.dd_squadra.options.clear()



        try:
            anno = int(self._view.dd_anno.value)
        except Exception as exc:
            self._view.txt_out_squadre.controls.clear()
            print(exc)
            return


        self._model.crea_grafo(anno)

        for n in self._model.G.nodes():
            self._view.dd_squadra.options.append(ft.dropdown.Option(key= n.id, text= f"{n.team_code} ({str(n.name)}"))


        self._view.update()




    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO
        self._view.txt_risultato.controls.clear()
        try:
            id_nodo= int(self._view.dd_squadra.value)
        except Exception as exc:
            self._view.show_alert("Inserire una squadra valida")
            print(exc)
            return
        team= self._model.dic_team_id[id_nodo]
        lista_squadre_peso= self._model.get_dettagli(team)
        for s, p in lista_squadre_peso:
            self._view.txt_risultato.controls.append(ft.Text(f"{s.team_code} ({s.name}) - {p}"))

        self._view.update()







    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO
        self._view.txt_risultato.controls.clear()
        try:
            id_nodo= int(self._view.dd_squadra.value)
        except Exception as exc:
            self._view.show_alert("Inserire una squadra valida")
            print(exc)
            return
        team= self._model.dic_team_id[id_nodo]

        sequenza_ottima, costo_ottimo= self._model.get_percorso_ottimo(team, 3)

        for i in range(len(sequenza_ottima)-1):
            s1= sequenza_ottima[i]
            s2= sequenza_ottima[i+1]

            peso= self._model.G[s1][s2]['weight']

            self._view.txt_risultato.controls.append(ft.Text(f"{s1.team_code} ({s1.name}) --> {s2.team_code} ({s2.name}) (peso)"))

        self._view.txt_risultato.controls.append(ft.Text(f"Peso totale {costo_ottimo}"))

        self._view.update()







    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO

    def handle_dd_anno(self):
        lista_anni= self._model.get_years()

        result=[]
        for year in lista_anni:
            result.append(ft.dropdown.Option(year))

        return result

    def handle_squadre_anno(self, e):
        self._view.txt_out_squadre.controls.clear()
        try:
            anno = int(self._view.dd_anno.value)
        except Exception as exc:
            self._view.txt_out_squadre.controls.clear()
            print(exc)
            return

        lista_squadre = self._model.get_teams(anno)
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(lista_squadre)}"))

        for t in lista_squadre:
            self._view.txt_out_squadre.controls.append(ft.Text(f"{t.team_code} ({t.name})"))

        self._view.update()






