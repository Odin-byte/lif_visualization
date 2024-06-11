# Imports

import networkx as nx
import json

import matplotlib.pyplot as plt

# Class definition


class LIF_Visualizer:

    def __init__(self) -> None:
        """This class allows to load in multiple LIF files and visualize them using networkx."""
        self.current_filepath = ""
        self.lif_data = {}
        self.layouts = {}
        self.stationDict = {}
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

    def layout_selection(self) -> str:
        number_layout = -1
        # Get the names and ids of the available layouts
        for index, layoutId in enumerate(self.layouts):
            print(f"Layout {index}: {layoutId}")
        print("Enter a valid number of a layout to visualize it: ")
        # Check if the number is valid
        while number_layout < 0 or number_layout >= len(self.layouts):
            try:
                number_layout = int(input())
            except:
                print("Enter a integer value.")

        return list(self.layouts)[number_layout]

    def visualize_layout(self, layout_id: str) -> None:
        """Visualizes a single layout selected by its layout id

        Args:
            layout_id (string): Unique layout id within the loaded in LIF msg
        """
        # Get layout from dict by id
        layout = self.layouts[layout_id]

        # Create a graph
        G = nx.DiGraph()

        # Add nodes and edges to the graph
        self._add_nodes_to_graph(layout, G)
        self._add_edges_to_graph(layout, G)

        pos = nx.get_node_attributes(G, "pos")
        colors_edges = nx.get_edge_attributes(G, "color").values()
        colors_nodes = nx.get_node_attributes(G, "color").values()
        weights = nx.get_edge_attributes(G, "weight").values()

        fig, ax = plt.subplots(num=layout["layoutName"])

        nx.draw(
            G,
            pos,
            ax,
            edge_color=colors_edges,
            width=list(weights),
            node_color=colors_nodes,
            with_labels=True,
            connectionstyle="Arc3, rad=0.02",
        )
        # TODO: Hide overlapping needs to be set by the parser
        self._add_stationTexts_to_graph(pos, ax, hide_overlapping=False)
        plt.tight_layout()
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.show()

    def _add_nodes_to_graph(self, layout: dict, graph: nx.Graph) -> None:
        """Adds nodes based on a LIF layout JSON object to a networkx graph

        Args:
            layout (dict): Dictionary holding the information from one layout JSON structure
            graph (nx.Graph): nx.Graph object to add the nodes to
        """
        # Extract the list of nodes from the layout
        nodes = layout["nodes"]

        self._fill_stationDict(layout["stations"])

        # Loop over all nodes within the layout
        for node in nodes:
            # Add the pair nodeId / nodePosition to the dict
            x = node["nodePosition"]["x"]
            y = node["nodePosition"]["y"]

            # Check if the node has a station associated with it
            if node["nodeId"] in self.stationDict:
                nodeColor = "green"
            else:
                nodeColor = "grey"
            graph.add_node(node["nodeId"], pos=(x, y), color=nodeColor)

        return

    def _add_edges_to_graph(self, layout: dict, graph: nx.Graph) -> None:
        """Adds edges based on a LIF layout JSON object to a networkx graph

        Args:
            layout (dict): Dictionary holding the information from one layout JSON structure
            graph (nx.Graph): nx.Graph object to add the edges to
        """
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
            graph.add_edge(
                edge["startNodeId"], edge["endNodeId"], color=color, weight=2
            )

        return

    def _fill_stationDict(self, stations: dict) -> None:
        """Called to fill a dict object used to map the stations of the LIF file to their networkx nodes

        Args:
            stations (dict): JSON structure of stations within one LIF layout
        """
        # Create dict
        stationDict = {}

        # Loop over stations and add key-value pairs
        for station in stations:
            for node in station["interactionNodeIds"]:

                # Key: nodeId - Value: stationName
                stationDict[node] = station["stationName"]

        self.stationDict = stationDict

    def _add_stationTexts_to_graph(
        self, positions: dict, ax, hide_overlapping: bool = False
    ) -> None:
        """Used to annotate the networkx nodes with their corresponding stationNames if available

        Args:
            positions (dict): Positions of all nodes in the networkx graph
            ax (_type_): Axis object the graph is plotted with
            hide_overlapping (bool, optional): Whether or not to hide a station text if a close copy already exists. Defaults to False.
        """
        plotted_positions = []
        for station, description in self.stationDict.items():
            x, y = positions[station]

            # Check if position is above the threshold for plotting
            if (
                not self._is_overlapping(x, y, plotted_positions)
                and not hide_overlapping
            ):
                ax.annotate(
                    description,
                    xy=(x, y),
                    xytext=(5, 20),
                    textcoords="offset points",
                    bbox=dict(facecolor="green", alpha=0.4),
                    fontsize=8,
                    horizontalalignment="center",
                    verticalalignment="center",
                )
                plotted_positions.append((x, y))

        return

    def _is_overlapping(
        self, x: float, y: float, position_list: list, threshold: float = 0.5
    ) -> bool:
        """Checks if given position is too close too any other position given in the list

        Args:
            x (_type_): _description_
            y (_type_): _description_
            plotted_positions (_type_): _description_
            threshold (float, optional): _description_. Defaults to 0.5.

        Returns:
            bool: _description_
        """
        for px, py in position_list:
            distance = ((x - px) ** 2 + (y - py) ** 2) ** 0.5
            if distance < threshold:
                return True
        return False
