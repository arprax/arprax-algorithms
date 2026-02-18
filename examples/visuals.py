from typing import List, Callable, Any
from arprax.algos.algorithms import bubble_sort
from arprax.algos.utils import random_array
from arprax.algos.structures import SinglyLinkedList


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

    if not arr:
        print("Array is empty, nothing to visualize.")
        return

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
        fig,
        func=update,
        frames=sort_func(arr),
        interval=50,
        repeat=False,
        blit=False,
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

    nodes = list(sll)

    if not nodes:
        print("List is empty, nothing to visualize.")
        return

    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        print(
            "\n[!] Visuals Not Installed. Run: pip install arprax-algorithms[visuals]\n"
        )
        return

    G = nx.DiGraph()
    for i in range(len(nodes)):
        G.add_node(i, label=str(nodes[i]))
        if i < len(nodes) - 1:
            G.add_edge(i, i + 1)

    pos = {i: (i, 0) for i in range(len(nodes))}
    labels = {i: G.nodes[i]["label"] for i in range(len(nodes))}

    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 3))

    for idx, _ in enumerate(sll.traverse()):
        ax.clear()
        ax.set_title(f"{title} | Searching for: {target}")

        node_colors = []
        for i in range(len(nodes)):
            if i == idx and nodes[i] == target:
                node_colors.append("#28a745")
            elif i == idx:
                node_colors.append("#dc3545")
            else:
                node_colors.append("#007acc")

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


def run_demo():
    print("Choose a demo:\n1) Bubble Sort\n2) Linked List Search")
    choice = input("Enter choice (1/2): ")
    if choice == "1":
        test_data = random_array(20, 1, 100)
        animate_sort(
            test_data, lambda d: bubble_sort(d, visualize=True), "Bubble Sort Demo"
        )
    elif choice == "2":
        ll = SinglyLinkedList()
        for x in [10, 25, 40, 55, 70, 85]:
            ll.append(x)
        animate_list_search(ll, 55)


if __name__ == "__main__":
    run_demo()
