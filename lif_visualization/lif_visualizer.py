# Imports

import networkx as nx
import json

import matplotlib.pyplot as plt

# Class definition


class LIF_Visualizer:

    def __init__(self) -> None:
        """This class allows to load in multiple LIF files and visualize them using networkx."""
        self.current_file = ""
        self.lif_data = {}
        self.layouts = {}
        return

    def load_from_file(self, filepath: str) -> None:
        """Loads in the LIF msg (JSON) as a networkx graph for later visualization

        Args:
            filepath (str): Path to the LIF file
        """
        with open(filepath) as f:
            lif_data = json.load(f)
        for layout in lif_data["layouts"]:
            self.layouts[layout["layoutId"]] = layout

        return

    def visualize_layout(self, layout_id: str) -> None:
        """Visualizes a single layout selected by its layout id

        Args:
            layout_id (string): Unique layout id within the loaded in LIF msg
        """
        # Get layout from dict by id
        layout = self.layouts[layout_id]

        # Create a graph
        G = nx.DiGraph()

        # Extract the list of nodes from the layout
        nodes = layout["nodes"]

        # Loop over all nodes within the layout
        for node in nodes:
            # Add the pair nodeId / nodePosition to the dict
            x = node["nodePosition"]["x"]
            y = node["nodePosition"]["y"]
            G.add_node(node["nodeId"], pos=(x, y))

        # Extract the list of edges from the layout
        edges = layout["edges"]

        # Loop over all edges and add them to the graph
        for edge in edges:
            # Check if the edge needs to be traversed backwards
            # TODO: Add functionality when multiply vehicles are present in a layout
            properties = edge["vehicleTypeEdgeProperties"][0]
            if properties["vehicleOrientation"] == 3.14:
                color = "red"
            else:
                color = "black"
            G.add_edge(edge["startNodeId"], edge["endNodeId"], color=color, weight=2)
            print(edge)

        pos = nx.get_node_attributes(G, "pos")
        colors = nx.get_edge_attributes(G, "color").values()
        weights = nx.get_edge_attributes(G, "weight").values()

        nx.draw(
            G,
            pos,
            edge_color=colors,
            width=list(weights),
            with_labels=True,
            connectionstyle="Arc3, rad=0.02",
        )
        plt.show()
