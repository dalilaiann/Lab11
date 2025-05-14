import flet as ft

from model import modello


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        colors=self._model.getAllColors()
        print(colors)
        for c in colors:
            self._view._ddcolor.options.append(ft.dropdown.Option(c))
        self._view.update_page()


    def handle_graph(self, e):
        year=self._view._ddyear.value
        if year is None:
            self._view.create_alert("Seleziona un anno!")
            return

        color=self._view._ddcolor.value
        if color is None:
            self._view.create_alert("Seleziona un colore!")
            return
        self._view.txtOut.controls.clear()
        self._model.buildGraph(color,year)
        numNodi=self._model.getNumNodes()
        numArchi=self._model.getNumEdges()
        if numNodi!=0 and numArchi!=0:
            self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {numNodi} Numero di archi: {numArchi}"))
            archiMaggiori, nodiRipetuti =self._model.getEdgesPesoMaggiore()
            for a in archiMaggiori:
                self._view.txtOut.controls.append(ft.Text(f"Arco da {a[0]} a {a[1]}, peso={a[2]}"))
            if len(nodiRipetuti)!=0:
                self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {nodiRipetuti}"))
        else:
            self._view.txtOut.controls.append(ft.Text(f"Non esiste un grafo con il colore e gli anni specificati. "))

        self.fillDDProduct(self._model._graph.nodes)
        self._view.btn_search.disabled=False
        self._view.update_page()

    def fillDDProduct(self, nodi):
        self._view._ddnode.options.clear()
        for n in nodi:
            self._view._ddnode.options.append(ft.dropdown.Option(str(n)))


    def handle_search(self, e):
        product=self._view._ddnode.value
        self._view.txtOut2.controls.clear()
        if product is None:
            self._view.create_alert("Seleziona un prodotto! ")
            return
        else:
            nodi=self._model.getPercorsoOpt(int(product))
            if len(nodi)>1:
                self._view.txtOut2.controls.append(ft.Text(f"Numero di archi percorso più lungo: {len(nodi)-1}"))
            else:
                self._view.txtOut2.controls.append(ft.Text(f"Non esistono nodi connessi al nodo {product}"))
        self._view.update_page()

