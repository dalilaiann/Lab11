from model.modello import Model

myModel=Model()
myModel.buildGraph('White', 2018)
print(myModel.getNumNodes())
print(myModel.getNumEdges())

for n in myModel._graph.edges(data=True):
    print(n)