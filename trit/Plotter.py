import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from pyvis.network import Network
from pyvis import network as net


class Plotter:

    def __init__(self, cleaned_results):
        relations = cleaned_results.relations
        self.topics = cleaned_results.topics

        remove_quotation = [rel for rel in relations if rel['relation'] != 'Quotation']
        edges = [(relation['entity'], relation['relation']) for relation in remove_quotation]
        nodes = set([relation['entity'] for relation in remove_quotation]).union(
            set([relation['relation'] for relation in remove_quotation]))

        graph = self.graph(nodes, edges)
        self.diagram = self.plot_relation(graph)

    @staticmethod
    def graph(nodes, edges):
        g = nx.Graph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        return g

    @staticmethod
    def plot_relation(g):
        vis = net.Network(notebook=True)
        vis.from_nx(g)
        vis.show("test.html")
        return vis
    
    def plot_topics(self):
        df = pd.DataFrame(self.topics, columns=['topic', 'confidence'])
        fig, ax = plt.subplots(figsize=(3, 7))
        g = sns.swarmplot(x='confidence', y='topic', data=df, color='blue')
        plt.grid()
        plt.show()
        return plt