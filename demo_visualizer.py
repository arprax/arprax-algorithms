from arprax.algos.algorithms import bubble_sort
from arprax.algos.utils import random_array, animate_sort, animate_list_search
from arprax.algos.structures import SinglyLinkedList


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
