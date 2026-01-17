import networkx as nx
from database.dao import DAO
from model.team import Team


class Model:
    def __init__(self):
        self.G= nx.Graph()
        self.lista_teams= []
        self.lista_appearences= []
        self.lista_salaries= []

        self.lista_years= []
        self.lista_squadre_valide= []

        self.dic_team_id= {}
        self.dic_team_salary= {}


        self.costo_ottimo= 0
        self.sequenza_ottimo= 0

    def load_all_teams(self):
        self.lista_teams= DAO.read_all_teams()
    def load_all_appearences(self):
        self.lista_appearences= DAO.read_all_appearences()

    def load_all_salaries(self):
        self.lista_salaries= DAO.read_all_salaries()

    def get_years(self):
        self.load_all_teams()
        self.lista_years= []

        set_anni= set()
        for team in self.lista_teams:
            set_anni.add(team.year)

        return list(sorted(set_anni))

    def get_teams(self, anno):
        self.load_all_teams()

        set_squadre= set()
        for t in self.lista_teams:
            if t.year == anno:
                set_squadre.add(t)

        return list(set_squadre)

    def crea_grafo(self, anno):
        self.load_all_teams()
        self.load_all_salaries()
        self.get_years()
        self.get_salari(anno)

        self.G= nx.Graph()




        for t in self.lista_teams:
            if t.year == anno:
                self.dic_team_id[t.id] = t
                if t not in self.lista_squadre_valide:
                    self.lista_squadre_valide.append(t)

        for s in self.lista_squadre_valide:
            self.G.add_node(s)

        for i in range(len(self.lista_squadre_valide)):
            for j in range(i+1, len(self.lista_squadre_valide)):

                squadra1= self.lista_squadre_valide[i]
                squadra2= self.lista_squadre_valide[j]

                if not self.G.has_edge(squadra1, squadra2):
                    peso= self.dic_team_salary[squadra1.id]+ self.dic_team_salary[squadra2.id]
                    self.G.add_edge(squadra1, squadra2, weight=peso)


    def get_salari(self, anno):
        self.load_all_salaries()

        for s in self.lista_salaries:
            if s.year == anno:
                if s.team_id in self.dic_team_salary.keys():
                    self.dic_team_salary[s.team_id] += s.salary
                else:
                    self.dic_team_salary[s.team_id] = s.salary


    def get_dettagli(self, nodo):
        vicini= self.G.neighbors(nodo)
        result= []
        for v in vicini:
            peso= self.G[nodo][v]['weight']
            result.append((v, peso))

        result.sort(key=lambda x: x[1], reverse=True)

        return result





    def get_percorso_ottimo(self, start, k=3):
        self.costo_ottimo= 0
        self.sequenza_ottimo= []


        self.ricorsione(start, [start], 0, k)

        return self.sequenza_ottimo, self.costo_ottimo



    def ricorsione(self, start: Team, sequenza_parziale, costo_parziale, k):

        if costo_parziale > self.costo_ottimo:
            self.costo_ottimo= costo_parziale
            self.sequenza_ottimo= list(sequenza_parziale)


        lista_iniziale= []
        if len(sequenza_parziale)<2:
            for nodo in self.G.neighbors(start):
                if nodo not in sequenza_parziale:
                    peso= self.G[start][nodo]['weight']
                    lista_iniziale.append((nodo, peso))
                    lista_iniziale.sort(key=lambda x: x[1], reverse=True)
                    lista_ottima= lista_iniziale[:k]

        else:
            for nodo in self.G.neighbors(start):
                if nodo not in sequenza_parziale:
                    peso= self.G[nodo][start]['weight']
                    ultimo_peso= self.G[sequenza_parziale[-2]][start]['weight']
                    if peso< ultimo_peso:
                        lista_iniziale.append((nodo, peso))
            lista_iniziale.sort(key=lambda x: x[1], reverse=True)
            lista_ottima= lista_iniziale[:k]


        for nodo, peso in lista_ottima:
            sequenza_parziale.append(nodo)
            nuovo_costo= costo_parziale + peso
            self.ricorsione(nodo, sequenza_parziale, nuovo_costo, k)
            sequenza_parziale.pop()





#METODO ALTERNATIVO

'''''''''''
import networkx as nx
from database.dao import DAO
from model.team import Team

class Model:
    def _init_(self):
        self.G = nx.Graph()
        self.lista_teams = []
        self.lista_salaries = []
        self.lista_appearences= []
        self.set_anni= set()

        self.dic_team_id={}
        self.dic_team_players= {}
        self.dic_player_salary= {}

        self.dic_team_tot_salary={}

        self.lista_team_validi= []

        self.componente_connessa= set()

        self.stipendio_ottimo = 0
        self.sequenza_ottima= []
        self.pesi_ottimi= []


    def load_all_data(self):
        self.lista_teams = DAO.read_all_teams()
        self.lista_salaries = DAO.read_all_salaries()
        self.lista_appearences = DAO.read_all_appearences()


    def lista_anni(self):
        self.load_all_data()
        self.set_anni.clear()

        for t in self.lista_teams:
            self.set_anni.add(t.year)
        return sorted(self.set_anni)



    def crea_grafo(self, anno_soglia):
        self.load_all_data()
        self.G = nx.Graph()
        self.lista_team_validi= []

        self.dic_team_id.clear()
        self.dic_team_players.clear()
        self.dic_player_salary.clear()
        self.dic_team_tot_salary.clear()



        for t in self.lista_teams:
            if t.year == anno_soglia:
                self.dic_team_id[t.id] = t
                self.dic_team_players[t.id]= set()

                self.lista_team_validi.append(t)

        for s in self.lista_salaries:
            if s.year == anno_soglia:
                self.dic_player_salary[s.player_id] = s.salary

        for a in self.lista_appearences:
           if a.year == anno_soglia:
                if a.team_id in self.dic_team_players:
                    self.dic_team_players[a.team_id].add(a.player_id)

        for team_id, players in self.dic_team_players.items():
            total = 0
            for p in players:
                if p in self.dic_player_salary:
                    total += self.dic_player_salary[p]
                self.dic_team_tot_salary[team_id] = total


        for t in self.lista_team_validi:
            self.G.add_node(t)

        for i in range(len(self.lista_team_validi)):
            for j in range(i+1, len(self.lista_team_validi)):
                team1= self.lista_team_validi[i]
                team2= self.lista_team_validi[j]

                peso= self.dic_team_tot_salary[team1.id] + self.dic_team_tot_salary[team2.id]
                self.G.add_edge(team1, team2, weight=peso)



    def gestione_dettagli(self, squadra):
        squadre_adiacenti= self.G.neighbors(squadra)
        risultato= []
        for s in squadre_adiacenti:
            peso= self.G[squadra][s]['weight']
            risultato.append((s, peso))

        risultato= sorted(risultato, key=lambda x: x[1], reverse=True)
        return risultato

    def trova_componente_connessa(self, start):
        return nx.node_connected_component(self.G, start)
    
'''''''''


















