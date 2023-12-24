import pydot
from pydot import Edge, Node
from pathlib import Path

graph = pydot.Dot('Example Factory', graph_type='digraph', nodesep=1.5)


graph.add_node(Node('1'))

graph.add_node(Node('2'))

graph.add_node(Node('3'))
graph.add_node(Node('4'))

graph.add_node(Node('5'))
graph.add_node(Node('6'))

graph.add_node(Node('7'))
graph.add_node(Node('8'))

graph.add_node(Node('9'))

#dummy nodes for edges
graph.add_node(Node('d1', style='invis'))
graph.add_node(Node('d2', style='invis'))
graph.add_node(Node('d3', style='invis'))
graph.add_node(Node('d4', style='invis'))


graph.add_edge(Edge('1', '2', dir='back', label='QQQWBVVLVLPQECCAYDWCC', fontsize=9))

graph.add_edge(Edge('2', '3', dir='back', label='QQWBVV', fontsize=9))
graph.add_edge(Edge('2', '4', dir='back', label='LVLPQECCAYDWCC', fontsize=9))

graph.add_edge(Edge('3', '5', dir='back', label='WQQWBV', fontsize=9))
graph.add_edge(Edge('3', '6', dir='back', label='VI', fontsize=9))

graph.add_edge(Edge('4', '7', dir='back', label='LVLPQE', fontsize=9))
graph.add_edge(Edge('4', '8', dir='back', label='CCAYDWCC', fontsize=9))

graph.add_edge(Edge('6', '9', dir='back', label='VICZ', fontsize=9))

graph.add_edge(Edge('5', 'd1', dir='back', label='VBWQQW', fontsize=9))
graph.add_edge(Edge('9', 'd2', dir='back', label='ZVICZA', fontsize=9))
graph.add_edge(Edge('7', 'd3', dir='back', label='EQPLVL', fontsize=9))
graph.add_edge(Edge('8', 'd4', dir='back', label='CAYDWC', fontsize=9))




path = Path.cwd() / 'graphs'
path.mkdir(parents=True, exist_ok=True)
output = graph.write_png(path / 'graph.png')
