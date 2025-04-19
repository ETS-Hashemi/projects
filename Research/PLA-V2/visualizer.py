import networkx as nx
import matplotlib.pyplot as plt

def visualize_reasoning(facts, rules, explanations, output_file="reasoning_graph.png"):
    """Visualize the reasoning process as a directed graph."""
    graph = nx.DiGraph()

    # Add facts as nodes
    for fact in facts:
        graph.add_node(fact, color="lightgreen", label=f"Fact: {fact}")

    # Add rules and explanations as edges
    for explanation in explanations.split("\n"):
        if "triggered" in explanation:
            parts = explanation.split(" triggered ")
            if len(parts) == 2:
                conditions, result = parts
                for condition in conditions.split(" and "):
                    graph.add_edge(condition.strip(), result.split(" with")[0].strip(), label="Rule")

    # Use a hierarchical layout for better readability
    try:
        pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")  # Requires pygraphviz or pydot
    except ImportError:
        pos = nx.spring_layout(graph, seed=42)  # Fallback to spring layout if graphviz is unavailable

    # Node colors: green for facts, blue for inferred results, red for final results
    node_colors = []
    for node in graph.nodes:
        if node in facts:
            node_colors.append("lightgreen")  # Facts in green
        elif any(node in edge for edge in graph.edges):
            node_colors.append("lightblue")  # Intermediate results in blue
        else:
            node_colors.append("lightcoral")  # Final results in red

    # Create the figure with constrained layout
    fig, ax = plt.subplots(figsize=(14, 10), constrained_layout=True)

    # Draw the graph
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=3000,
        font_size=10,
        font_color="black",
        edge_color="gray",
        arrowsize=20,
        linewidths=1.5,
        ax=ax,
    )

    # Add edge labels for better understanding
    edge_labels = nx.get_edge_attributes(graph, "label")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8, ax=ax)

    # Add a legend
    legend_elements = [
        plt.Line2D([0], [0], marker="o", color="w", label="Fact", markersize=10, markerfacecolor="lightgreen"),
        plt.Line2D([0], [0], marker="o", color="w", label="Intermediate Result", markersize=10, markerfacecolor="lightblue"),
        plt.Line2D([0], [0], marker="o", color="w", label="Final Result", markersize=10, markerfacecolor="lightcoral"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=10)

    # Add a title to the graph
    ax.set_title("Reasoning Process Visualization", fontsize=16, fontweight="bold")

    # Save the graph
    plt.savefig(output_file, bbox_inches="tight")
    plt.show()
