"""Problema 1: cola FIFO implementada con una lista enlazada.

Autor: Jeremy Arévalo
Ejecución: python problema1.py
"""

from dataclasses import dataclass


@dataclass
class Node:
    """Nodo de la lista enlazada: guarda un dato y el siguiente nodo."""

    value: object
    next_node: "Node | None" = None


class Cola:
    """Cola FIFO con referencias al primer y al último nodo."""

    def __init__(self) -> None:
        self._first: Node | None = None
        self._last: Node | None = None
        self._count = 0

    def enqueue(self, element: object) -> None:
        """Inserta un dato al final sin recorrer la lista: O(1)."""
        new_node = Node(element)

        if self._last is None:
            # Si está vacía, el nuevo nodo es el primero y el último.
            self._first = new_node
        else:
            self._last.next_node = new_node

        self._last = new_node
        self._count += 1

    def dequeue(self) -> object:
        """Retira y devuelve el primer dato de la cola: O(1)."""
        if self.is_empty():
            raise IndexError("No se puede retirar: la cola está vacía.")

        first_node = self._first
        self._first = first_node.next_node
        self._count -= 1

        if self._first is None:
            # Se libera también el final para poder reutilizar la cola.
            self._last = None

        return first_node.value

    def front(self) -> object:
        """Consulta el primer dato sin quitarlo: O(1)."""
        if self.is_empty():
            raise IndexError("No se puede consultar: la cola está vacía.")
        return self._first.value

    def is_empty(self) -> bool:
        """Indica si quedan elementos pendientes."""
        return self._count == 0

    def size(self) -> int:
        """Devuelve el número de elementos guardados: O(1)."""
        return self._count

    def show_queue(self) -> list[object]:
        """Recorre los nodos para mostrar la cola sin modificarla."""
        elements = []
        current = self._first
        while current is not None:
            elements.append(current.value)
            current = current.next_node
        return elements


def run_demo() -> None:
    """Demuestra los cinco métodos solicitados y casos de cola vacía."""
    queue = Cola()
    print("PROBLEMA 1 - COLA BÁSICA CON LISTA ENLAZADA")
    print("¿Está vacía al inicio?:", queue.is_empty())

    for customer in ("Ana", "Luis", "Marta"):
        queue.enqueue(customer)
        print(f"enqueue({customer}) -> {queue.show_queue()}")

    print("front():", queue.front())
    print("size():", queue.size())
    print("dequeue():", queue.dequeue())
    print("front() después de retirar:", queue.front())

    while not queue.is_empty():
        print("dequeue():", queue.dequeue())

    print("¿Está vacía al terminar?:", queue.is_empty())

    # Se controla el error cuando alguien intenta retirar de una cola vacía.
    try:
        queue.dequeue()
    except IndexError as error:
        print("Error controlado:", error)

    queue.enqueue("Sofía")
    print("Reutilización de la cola:", queue.show_queue())


# Inicia el ejemplo práctico de la cola enlazada.
run_demo()
