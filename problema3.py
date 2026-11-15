"""Problema 3: atención hospitalaria con una cola de prioridad estable.

Autor: Jeremy Arévalo
Ejecución: python problema3.py
"""

from dataclasses import dataclass
import heapq


@dataclass(frozen=True)
class Patient:
    """Paciente con nivel de urgencia de 1 (máxima) a 5 (mínima)."""

    name: str
    urgency: int

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("El paciente debe tener un nombre.")
        if (
            isinstance(self.urgency, bool)
            or not isinstance(self.urgency, int)
            or not 1 <= self.urgency <= 5
        ):
            raise ValueError("La urgencia debe ser un número entero entre 1 y 5.")


class ColaEmergencias:
    """Prioriza urgencias bajas y respeta el orden de llegada en empates."""

    def __init__(self) -> None:
        # Tupla: (urgencia, orden de llegada, paciente).
        self._heap: list[tuple[int, int, Patient]] = []
        self._arrival_order = 0

    def add_patient(self, name: str, urgency: int) -> None:
        """Agrega un paciente con inserción eficiente O(log n)."""
        patient = Patient(name, urgency)
        heapq.heappush(self._heap, (urgency, self._arrival_order, patient))
        self._arrival_order += 1

    def attend_next(self) -> Patient:
        """Atiende al más urgente; en empate, al que llegó primero."""
        if self.is_empty():
            raise IndexError("No existen pacientes en espera.")
        return heapq.heappop(self._heap)[2]

    def front(self) -> Patient:
        """Consulta al siguiente paciente sin eliminarlo: O(1)."""
        if self.is_empty():
            raise IndexError("No existen pacientes en espera.")
        return self._heap[0][2]

    def is_empty(self) -> bool:
        return not self._heap

    def size(self) -> int:
        return len(self._heap)

    def show_waiting(self) -> list[str]:
        """Devuelve la lista ordenada sin cambiar la prioridad interna."""
        return [
            f"{patient.name} (urgencia {urgency})"
            for urgency, _, patient in sorted(self._heap)
        ]


def run_demo() -> None:
    """Demuestra ocho pacientes y empates de prioridad."""
    queue = ColaEmergencias()
    patients = [
        ("Ana", 4), ("Luis", 2), ("Marta", 1), ("Pedro", 3),
        ("Sofía", 2), ("Diego", 5), ("Elena", 1), ("Carlos", 3),
    ]

    print("PROBLEMA 3 - COLA DE EMERGENCIAS")
    for name, urgency in patients:
        queue.add_patient(name, urgency)
        print(f"Llegó {name} con urgencia {urgency}.")

    print("Pacientes registrados:", queue.size())
    print("Siguiente paciente:", queue.front().name)
    print("Lista de espera:")
    for patient in queue.show_waiting():
        print("-", patient)

    print("Orden de atención:")
    while not queue.is_empty():
        patient = queue.attend_next()
        print(f"Atendido: {patient.name} (urgencia {patient.urgency})")

    try:
        queue.attend_next()
    except IndexError as error:
        print("Error controlado:", error)

    try:
        queue.add_patient("Paciente inválido", 6)
    except ValueError as error:
        print("Validación de urgencia:", error)


# Los ejemplos se ejecutan al abrir este archivo con Python.
run_demo()
