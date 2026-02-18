"""
Unit tests for Arprax Visualization utilities.
Reaches 100% coverage by forcing edge drawing and node color branching.
"""

from unittest.mock import MagicMock, patch
from arprax.algos.utils.visuals import animate_sort, animate_list_search
from arprax.algos.structures.linear import SinglyLinkedList


@patch("matplotlib.pyplot.show")
@patch("matplotlib.pyplot.subplots")
@patch("matplotlib.animation.FuncAnimation")
def test_animate_sort_coverage(mock_func_anim, mock_subplots, mock_show):
    """Covers update logic and animation initialization."""
    mock_fig, mock_ax = MagicMock(), MagicMock()
    mock_subplots.return_value = (mock_fig, mock_ax)
    mock_ax.bar.return_value = [MagicMock(), MagicMock()]

    animate_sort([2, 1], lambda x: [[1, 2], 1])

    # Trigger internal update function
    update_func = mock_func_anim.call_args[1]["func"]
    update_func([1, 2])  # Hits bar update
    update_func(0)  # Hits isinstance check
    assert mock_show.called


@patch("matplotlib.pyplot.show")
@patch("networkx.draw")
def test_animate_list_search_branches(mock_draw, mock_show):
    """
    Targets Lines 79 and 99-102.
    Using a 2-node list where target is at index 1 forces:
    - Line 79: Adding an edge between nodes.
    - Line 100: Coloring a non-target node Red (current).
    - Line 102: Coloring other nodes Blue.
    """
    ll = SinglyLinkedList()
    ll.append(10)  # Node 0
    ll.append(20)  # Node 1 (Target)

    with patch("matplotlib.pyplot.pause"):
        # Searching for 20 means when idx=0, node is Red/Blue. When idx=1, it's Green.
        animate_list_search(ll, target=20)

    assert mock_draw.called
    # Line 79 is hit because len(nodes) > 1 and i < len(nodes) - 1.
    # Lines 99-102 are hit as the loop iterates through node colors.


def test_visuals_empty_and_error():
    """Covers empty list check and ImportError handling."""
    # Empty list branch
    with patch("builtins.print") as mock_print:
        animate_list_search(SinglyLinkedList(), 10)
        mock_print.assert_called_with("List is empty, nothing to visualize.")

    # ImportError branch
    with patch("builtins.__import__", side_effect=ImportError):
        animate_sort([1], lambda x: [x])
        animate_list_search(SinglyLinkedList(), 10)
