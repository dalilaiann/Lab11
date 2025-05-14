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
        for u in self._idMapProduct.values():
            for v in self._idMapProduct.values():
                if u.Product_number<v.Product_number and u.Product_color==color and v.Product_color==color:
                    peso=DAO.getAllEdgesByYearColor(u, v, year)
                    if peso!=0:
                        self._graph.add_edge(u,v, weight=peso)
                        self._lista.append((u,v,peso))

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getEdgesPesoMaggiore(self):
        self._lista.sort(key=lambda x: x[2], reverse=True)
        lista_output=self._lista[:3]
        nodi_ripetuti={}
        res=[]
        for l in lista_output:
            if l[0].Product_number not in nodi_ripetuti:
                nodi_ripetuti[l[0].Product_number]=1
            else:
                nodi_ripetuti[l[0].Product_number]+=1
            if l[1].Product_number  not in nodi_ripetuti:
                nodi_ripetuti[l[1].Product_number]=1
            else:
                nodi_ripetuti[l[1].Product_number]+=1

        for n in nodi_ripetuti:
            if nodi_ripetuti[n]>1:
                res.append(n)

        return self._lista[:3], res

    def getPercorsoOpt(self, source):
        self._percorsoOpt=[]
        parziale=[self._idMapProduct[source]]
        rimanenti=list(self._graph.neighbors(self._idMapProduct[source]))
        self._ricorsione(parziale, rimanenti)
        return self._percorsoOpt

    def _ricorsione(self, parziale, rimanenti):

        for n in rimanenti:
            if self.is_admisible(parziale,n):
                parziale.append(n)
                nuovi_rimanenti=list(self._graph.neighbors(n))
                self._ricorsione(parziale, nuovi_rimanenti)
                parziale.pop()
            else:
                if len(parziale) > len(self._percorsoOpt):
                    self._percorsoOpt = copy.deepcopy(parziale)


    def is_admisible(self, parziale, nodo):

        if len(parziale)>0:
            last = parziale[-1]
            # controllo che non ci siano cicli
            for i in range(len(parziale)-1):
                if (parziale[i]==last and parziale[i+1]==nodo) or (parziale[i]==nodo and parziale[i+1]==last) :
                    return False

            #controllo il peso
            for i in range(len(parziale)-1):
                if self._graph[last][nodo]['weight']<self._graph[parziale[i]][parziale[i+1]]['weight']:
                    return False

        return True




if __name__=="__main__":
    myModel=Model()
    myModel.buildGraph('White', 2018)
    nodi=myModel.getPercorsoOpt(94110)
    for i in range(len(nodi)-1):
        print(f"{str(nodi[i])}-{str(nodi[i+1])}-{myModel._graph[nodi[i]][nodi[i+1]]['weight']}")

