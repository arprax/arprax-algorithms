from typing import List, Callable, Any


def animate_sort(
    arr: List[int], sort_func: Callable, title: str = "Arprax Lab Visualization"
):
    """
    Renders a real-time animation of sorting logic using Matplotlib.

    This function sets up a bar chart and updates the height of each bar
    based on snapshots yielded by the provided sorting generator.

    Args:
        arr (List[int]): The unsorted list of integers to visualize.
        sort_func (Callable): A generator function that yields List[int] states.
        title (str): The title displayed at the top of the animation window.
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
    except ImportError:
        print(
            "\n[!] Visuals Not Installed. Run: pip install arprax-algorithms[visuals]\n"
        )
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(title)

    bar_rects = ax.bar(range(len(arr)), arr, align="edge", color="#007acc")
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, int(max(arr) * 1.1))

    iteration = [0]
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontweight="bold")

    def update(data):
        if isinstance(data, int):
            return bar_rects
        for rect, val in zip(bar_rects, data):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text(f"Operations: {iteration[0]}")
        return bar_rects

    anim = animation.FuncAnimation(
        fig, func=update, frames=sort_func(arr), interval=50, repeat=False, blit=False
    )
    plt.show()
    return anim


def animate_list_search(sll, target: Any, title: str = "Singly Linked List Search"):
    """
    Visualizes a linear search through a Singly Linked List using a Graph.

    Args:
        sll (SinglyLinkedList): The list instance to visualize.
        target (Any): The value being searched for.
        title (str): The title for the plot window.
    """
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        print(
            "\n[!] Visuals Not Installed. Run: pip install arprax-algorithms[visuals]\n"
        )
        return

    # Convert the list to a list of values for easy graph mapping
    nodes = list(sll)
    if not nodes:
        print("List is empty, nothing to visualize.")
        return

    # 1. Create Graph structure
    G = nx.DiGraph()
    for i in range(len(nodes)):
        G.add_node(i, label=str(nodes[i]))
        if i < len(nodes) - 1:
            G.add_edge(i, i + 1)

    # 2. Define Layout (Linear)
    pos = {i: (i, 0) for i in range(len(nodes))}
    labels = {i: G.nodes[i]["label"] for i in range(len(nodes))}

    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots(figsize=(12, 3))

    # 3. Step through traversal
    # We use the 'traverse' method from your updated linear.py
    for idx, node in enumerate(sll.traverse()):
        ax.clear()
        ax.set_title(f"{title} | Searching for: {target}")

        # Color nodes: Red = Current, Green = Found, Blue = Neutral
        node_colors = []
        for i in range(len(nodes)):
            if i == idx and nodes[i] == target:
                node_colors.append("#28a745")  # Green
            elif i == idx:
                node_colors.append("#dc3545")  # Red
            else:
                node_colors.append("#007acc")  # Blue

        nx.draw(
            G,
            pos,
            labels=labels,
            with_labels=True,
            node_color=node_colors,
            node_size=1200,
            edge_color="#666666",
            arrows=True,
            ax=ax,
            font_color="white",
            font_weight="bold",
        )

        plt.pause(0.8)
        if nodes[idx] == target:
            ax.set_title(f"Target {target} FOUND at Index {idx}!")
            plt.pause(2.0)
            break

    plt.ioff()
    plt.show()
