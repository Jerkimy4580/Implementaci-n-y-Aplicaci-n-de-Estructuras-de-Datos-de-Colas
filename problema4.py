"""Problema 4, opción C: atención bancaria con dos tipos de colas.

Autor: Jeremy Arévalo
Ejecución: python problema4.py
"""

from collections import deque
from dataclasses import dataclass
import heapq


VALID_SERVICES = ("Caja", "Préstamos", "Consultas")
VALID_CATEGORIES = ("Normal", "Premium", "Adulto mayor")
PRIORITIES = {"Adulto mayor": 1, "Premium": 2}


@dataclass(frozen=True)
class Customer:
    """Cliente con servicio solicitado y categoría de atención."""

    name: str
    service: str
    category: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        if self.service not in VALID_SERVICES:
            raise ValueError("Servicio inválido. Use Caja, Préstamos o Consultas.")
        if self.category not in VALID_CATEGORIES:
            raise ValueError("Categoría inválida. Use Normal, Premium o Adulto mayor.")


class SimpleQueue:
    """Cola FIFO para clientes de atención normal."""

    def __init__(self) -> None:
        self._items: deque[Customer] = deque()

    def enqueue(self, customer: Customer) -> None:
        self._items.append(customer)

    def dequeue(self) -> Customer:
        if not self._items:
            raise IndexError("No hay clientes normales en espera.")
        return self._items.popleft()

    def is_empty(self) -> bool:
        return not self._items

    def show_waiting(self) -> list[str]:
        return [customer.name for customer in self._items]


class PriorityQueue:
    """Cola de prioridad para adultos mayores y clientes premium."""

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, Customer]] = []
        self._arrival_order = 0

    def enqueue(self, customer: Customer) -> None:
        if not isinstance(customer, Customer) or customer.category not in PRIORITIES:
            raise ValueError("La cola prioritaria admite adultos mayores o premium.")
        priority = PRIORITIES[customer.category]
        # El orden de llegada resuelve empates de una misma categoría.
        heapq.heappush(self._heap, (priority, self._arrival_order, customer))
        self._arrival_order += 1

    def dequeue(self) -> Customer:
        if not self._heap:
            raise IndexError("No hay clientes prioritarios en espera.")
        return heapq.heappop(self._heap)[2]

    def is_empty(self) -> bool:
        return not self._heap

    def show_waiting(self) -> list[str]:
        return [
            f"{customer.name} ({customer.category})"
            for _, _, customer in sorted(self._heap)
        ]


class ServiceQueue:
    """Mantiene una cola simple y otra prioritaria por servicio."""

    def __init__(self) -> None:
        self.normal_queue = SimpleQueue()
        self.priority_queue = PriorityQueue()

    def add_customer(self, customer: Customer) -> None:
        if customer.category == "Normal":
            self.normal_queue.enqueue(customer)
        else:
            self.priority_queue.enqueue(customer)

    def attend_next(self) -> Customer:
        """Atiende primero prioridades y luego clientes normales por llegada."""
        if not self.priority_queue.is_empty():
            return self.priority_queue.dequeue()
        return self.normal_queue.dequeue()

    def has_customers(self) -> bool:
        return not self.normal_queue.is_empty() or not self.priority_queue.is_empty()


class BankSystem:
    """Distribuye clientes entre Caja, Préstamos y Consultas."""

    def __init__(self) -> None:
        self._services = {service: ServiceQueue() for service in VALID_SERVICES}

    def add_customer(self, name: str, service: str, category: str) -> None:
        customer = Customer(name, service, category)
        self._services[service].add_customer(customer)

    def attend_next(self, service: str) -> Customer:
        if service not in self._services:
            raise ValueError("El servicio indicado no existe.")
        if not self._services[service].has_customers():
            raise IndexError(f"No hay clientes esperando en {service}.")
        return self._services[service].attend_next()

    def has_waiting(self, service: str) -> bool:
        if service not in self._services:
            raise ValueError("El servicio indicado no existe.")
        return self._services[service].has_customers()

    def waiting_list(self, service: str) -> tuple[list[str], list[str]]:
        """Devuelve (prioritarios, normales) sin retirar clientes."""
        if service not in self._services:
            raise ValueError("El servicio indicado no existe.")
        line = self._services[service]
        return line.priority_queue.show_waiting(), line.normal_queue.show_waiting()


def run_demo() -> None:
    """Simula distintos servicios y categorías de atención bancaria."""
    bank = BankSystem()
    customers = [
        ("Ana", "Caja", "Normal"),
        ("Luis", "Préstamos", "Premium"),
        ("Marta", "Caja", "Adulto mayor"),
        ("Pedro", "Consultas", "Normal"),
        ("Sofía", "Caja", "Premium"),
        ("Diego", "Préstamos", "Normal"),
        ("Elena", "Caja", "Normal"),
        ("Carlos", "Consultas", "Adulto mayor"),
        ("Valeria", "Préstamos", "Adulto mayor"),
        ("Julia", "Caja", "Premium"),
    ]

    print("PROBLEMA 4 - SISTEMA DE ATENCIÓN BANCARIA")
    print("Prioridad: Adulto mayor > Premium > Normal")
    for name, service, category in customers:
        bank.add_customer(name, service, category)
        print(f"Registro: {name} | {service} | {category}")

    for service in VALID_SERVICES:
        priority, normal = bank.waiting_list(service)
        print(f"\nServicio: {service}")
        print("Espera prioritaria:", priority)
        print("Espera normal:", normal)
        print("Orden de atención:")
        while bank.has_waiting(service):
            customer = bank.attend_next(service)
            print(f"- {customer.name} ({customer.category})")

    try:
        bank.attend_next("Caja")
    except IndexError as error:
        print("\nError controlado:", error)

    try:
        bank.add_customer("Cliente", "Seguros", "Normal")
    except ValueError as error:
        print("Validación de servicio:", error)


# La demostración se ejecuta directamente al correr problema4.py.
run_demo()
