import copy

import networkx as nx

from database.DAO import DAO
class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._bestDiff = 0
        self._bestPilota = None
        self._tassiSconfitta = {}
        self._tassoTot = 0
        self._team = []
        self._bestPath = []
        self._bestScore = 1000

    def getDreamTeam(self, k):
        self._bestPath = []
        self._bestScore = 1000

        parziale = []
        self._ricorsione(parziale, k)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, k):

        #terminale
        if len(parziale) == k:
            if self.getScore(parziale) <  self._bestScore:
                self._bestScore = self.getScore(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return
        for n in self._grafo.nodes():
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, k)
                parziale.pop()

    def getScore(self, team):
        score = 0
        for e in self._grafo.edges(data=True):
            if e[0] not in team and e[1] in team:
                score += e[2]['weight']
        return score


    def dreamTeam(self, num):
        # Ordinamento corretto per tasso di sconfitta
        sorted_piloti = sorted(self._tassiSconfitta, key=lambda x: x[1])

        # Selezione primi 'num' piloti con minor sconfitte
        for pilota, tasso in sorted_piloti:
            if len(self._team) == num:
                return
            else:
                self._tassoTot += tasso
                self._team.append(str(pilota.driverId) + " - "+ pilota.__str__() + " - " + str(tasso))


    def builtGraph(self, anno):
        self._nodes = DAO.getVertici(anno)

        self._grafo.add_nodes_from(self._nodes)
        self._idMap = {}
        for nodo in self._nodes:
            self._idMap[nodo.driverId] = nodo

        for nodo1 in self._nodes:
            for nodo2 in self._nodes:
                if nodo1 != nodo2:
                    arco = DAO.getArchi(nodo1, nodo2, anno)
                    if arco.weight > 0:
                        if self._grafo.has_edge(nodo1, nodo2):
                            self._grafo[nodo1][nodo2]['weight'] += arco.weight
                        else:
                            self._grafo.add_edge(nodo1, nodo2, weight=arco.weight)

    def trovaMigliorPilota(self):
        for nodo in self._grafo.nodes:
            # Somma dei pesi degli archi uscenti (vittorie)
            uscenti = sum(self._grafo.edges[nodo, succ]['weight'] for succ in self._grafo.successors(nodo))

            # Somma dei pesi degli archi entranti (sconfitte)
            entranti = sum(self._grafo.edges[pred, nodo]['weight'] for pred in self._grafo.predecessors(nodo))
            self._tassiSconfitta[nodo] = entranti
            diff = uscenti - entranti

            if diff> self._bestDiff:
                self._bestDiff = diff
                self._bestPilota = nodo.__str__()

        self._tassiSconfitta = sorted(self._tassiSconfitta.items(), key=lambda x: x[1])


    def numArchi(self):
        return self._grafo.number_of_edges()

    def numNodi(self):
        print(self._grafo)
        return self._grafo.number_of_nodes()

    def getAnni(self):
        return DAO.getAnni()