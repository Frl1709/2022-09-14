import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []
        self.idMap = {}

        self.connessa = []

        self.bestSet = []

    def getBestSet(self, v0, dTot):
        self.bestSet = set()

        parziale = [v0]
        rimanenti = self.connessa
        rimanenti.remove(v0)

        self._ricorsione(parziale, rimanenti, dTot)

        return self.bestSet

    def _ricorsione(self, parziale, rimanenti, dTot):
        if self.getDurataCammino(parziale) > dTot:
            return

        if len(parziale) > len(self.bestSet):
            self.bestSet = copy.deepcopy(parziale)

        for node in rimanenti:
            if node not in parziale:
                parziale.append(node)
                self._ricorsione(parziale, rimanenti, dTot)
                parziale.pop()

    def buildGraph(self, durata):
        self.graph.clear()
        self.nodes = DAO.getNodes(durata)
        self.graph.add_nodes_from(self.nodes)
        for n in self.nodes:
            self.idMap[n.AlbumId] = n

        self.edges = DAO.getEdge(self.idMap)
        self.graph.add_edges_from(self.edges)

    def getGraphSize(self):
        return len(self.nodes), len(self.edges)

    def getConnessa(self, v0):
        self.connessa = nx.node_connected_component(self.graph, v0)
        durata = self.getDurataCammino(list(self.connessa))

        return len(self.connessa), durata

    def getDurataCammino(self, lista):
        durata = 0
        for album in lista:
            durata += album.Durata

        return durata

