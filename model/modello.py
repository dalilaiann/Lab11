import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapProduct={}
        self._lista=[]
        self._percorsoOpt=[]
        nodes=DAO.getAllProducts()
        for n in nodes:
            self._idMapProduct[n.Product_number]=n

    def getAllColors(self):
        return DAO.getAllColors()

    def buildGraph(self, color, year):
        self._lista=[]
        self._graph=nx.Graph()
        self.addNodes(color)
        self.addEdges(year,color)

    def addNodes(self, color):
        nodes=DAO.getAllNodes(color)
        self._graph.add_nodes_from(nodes)

    def addEdges(self, year, color):
        edges=DAO.getAllEdgesByYearColor(year, color, self._idMapProduct)
        for e in edges:
            self._lista.append((e[0], e[1], e[2]))
            self._graph.add_edge(e[0], e[1], weight=e[2])

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getEdgesPesoMaggiore(self):
        self._lista.sort(key=lambda x: x[2], reverse=True)
        lista_output=self._lista[:3]
        nodi_ripetuti=[]

        if (lista_output[0][0]==lista_output[1][0] or lista_output[0][0]==lista_output[0][1]):
            nodi_ripetuti.append(str(lista_output[0][0]))
        if (lista_output[0][0]==lista_output[2][0] or lista_output[0][0]==lista_output[2][1]):
            nodi_ripetuti.append(str(lista_output[0][0]))
        if (lista_output[0][1]==lista_output[1][0] or lista_output[0][1]==lista_output[1][1]):
            nodi_ripetuti.append(str(lista_output[0][1]))
        if (lista_output[0][1] == lista_output[2][0] or lista_output[0][1] == lista_output[2][1]):
            nodi_ripetuti.append(str(lista_output[0][1]))
        if (lista_output[1][0]==lista_output[2][0] or lista_output[1][0]==lista_output[2][1]):
            nodi_ripetuti.append(str(lista_output[1][0]))
        if (lista_output[1][1] == lista_output[2][0] or lista_output[1][1] == lista_output[2][1]):
            nodi_ripetuti.append(str(lista_output[1][1]))


        return self._lista[:3], nodi_ripetuti

    def getPercorsoOpt(self, source):
        self._percorsoOpt=[]
        parziale=[self._idMapProduct[source]]
        rimanenti=[(n, self._graph[self._idMapProduct[source]][n]['weight']) for n in self._graph.neighbors(self._idMapProduct[source])]
        self._ricorsione(parziale, rimanenti)

        return self._percorsoOpt

    def _ricorsione(self, parziale, rimanenti):
        if len(rimanenti)==0:
            if len(parziale)>len(self._percorsoOpt):
                self._percorsoOpt=copy.deepcopy(parziale)
        else:
            for n in rimanenti:
                if self.is_admisible(parziale, n):
                    parziale.append(n)
                    self._ricorsione(parziale, self._graph.neighbors(n))
                    parziale.pop()


    def is_admisible(self, parziale, nodo):
        flag=True
        for n in parziale:
            if nodo[1]<n[1]:
                flag=False
        return flag



if __name__=="__main__":
    myModel=Model()
    myModel.buildGraph('White', 2018)
    myModel.getPercorsoOpt(94110)
