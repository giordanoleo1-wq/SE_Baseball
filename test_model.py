from model.model import Model
model = Model()

#print(model.get_years())
#print(model.get_teams(1915))
#model.get_salari(2015)
#print(model.dic_team_salary)

model.crea_grafo(2015)

lista_valide= model.lista_squadre_valide
#print(lista_valide)
#print(model.G.number_of_nodes())
#print(model.G)
atl= model.dic_team_id[2777]
#print(model.get_dettagli(atl))

model.get_percorso_ottimo(atl, 3)
#print(model.sequenza_ottimo)
#print(model.costo_ottimo)
print(model.get_dizionario())



