from unittest.mock import MagicMock, patch
from examples.visuals import animate_sort, animate_list_search
from alnoms.structures.linear import SinglyLinkedList


@patch("matplotlib.pyplot.show")
@patch("matplotlib.pyplot.subplots")
@patch("matplotlib.animation.FuncAnimation")
def test_animate_sort_coverage(mock_func_anim, mock_subplots, mock_show):
    mock_fig, mock_ax = MagicMock(), MagicMock()
    mock_subplots.return_value = (mock_fig, mock_ax)
    mock_ax.bar.return_value = [MagicMock(), MagicMock()]

    animate_sort([2, 1], lambda x: [[1, 2], 1])

    update_func = mock_func_anim.call_args[1]["func"]
    update_func([1, 2])
    update_func(0)

    assert mock_show.called


@patch("matplotlib.pyplot.show")
@patch("networkx.draw")
def test_animate_list_search_branches(mock_draw, mock_show):
    ll = SinglyLinkedList()
    ll.append(10)
    ll.append(20)

    with patch("matplotlib.pyplot.pause"):
        animate_list_search(ll, target=20)

    assert mock_draw.called


def test_visuals_empty_and_error():
    # Empty list branch
    with patch("builtins.print") as mock_print:
        animate_list_search(SinglyLinkedList(), 10)
        mock_print.assert_called_with("List is empty, nothing to visualize.")

    # Empty array branch
    with patch("builtins.print") as mock_print:
        animate_sort([], lambda x: x)
        mock_print.assert_called_with("Array is empty, nothing to visualize.")

    # ImportError branch for animate_sort
    with patch.dict("sys.modules", {"matplotlib": None}):
        animate_sort([1], lambda x: [x])

    # ImportError branch for animate_list_search
    ll = SinglyLinkedList()
    ll.append(1)
    with patch.dict("sys.modules", {"networkx": None}):
        animate_list_search(ll, 1)
