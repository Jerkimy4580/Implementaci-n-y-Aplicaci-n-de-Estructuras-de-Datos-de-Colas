"""Problema 2: cola circular y planificación Round Robin (quantum = 3).

Autor: Jeremy Arévalo
Ejecución: python problema2.py
"""

from dataclasses import dataclass


TIME_QUANTUM = 3


@dataclass
class Process:
    """Proceso con nombre y tiempo de CPU pendiente."""

    name: str
    remaining_time: int

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("El proceso debe tener un nombre.")
        if (
            isinstance(self.remaining_time, bool)
            or not isinstance(self.remaining_time, int)
            or self.remaining_time <= 0
        ):
            raise ValueError("El tiempo de ejecución debe ser un entero positivo.")


class ColaCircular:
    """Cola FIFO con arreglo fijo e índices que vuelven al inicio."""

    def __init__(self, capacity: int) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            raise ValueError("La capacidad debe ser un entero positivo.")

        self._capacity = capacity
        self._items: list[Process | None] = [None] * capacity
        self._front_index = 0
        self._rear_index = 0
        self._count = 0

    def enqueue(self, process: Process) -> None:
        """Agrega un proceso en el siguiente espacio circular."""
        if not isinstance(process, Process):
            raise TypeError("Se esperaba un proceso válido.")
        if self._count == self._capacity:
            raise OverflowError("La cola circular está llena.")

        self._items[self._rear_index] = process
        self._rear_index = (self._rear_index + 1) % self._capacity
        self._count += 1

    def dequeue(self) -> Process:
        """Extrae el proceso del frente y avanza el índice circular."""
        if self.is_empty():
            raise IndexError("La cola circular está vacía.")

        process = self._items[self._front_index]
        self._items[self._front_index] = None
        self._front_index = (self._front_index + 1) % self._capacity
        self._count -= 1
        return process

    def front(self) -> Process:
        """Consulta el siguiente proceso sin retirarlo."""
        if self.is_empty():
            raise IndexError("La cola circular está vacía.")
        return self._items[self._front_index]

    def is_empty(self) -> bool:
        return self._count == 0

    def size(self) -> int:
        return self._count

    def add_process(self, name: str, execution_time: int) -> None:
        """Valida y añade un proceso nuevo."""
        self.enqueue(Process(name, execution_time))

    def show_pending(self) -> list[str]:
        """Muestra procesos en el orden que recibirán la CPU."""
        pending = []
        for offset in range(self._count):
            index = (self._front_index + offset) % self._capacity
            process = self._items[index]
            pending.append(f"{process.name}({process.remaining_time})")
        return pending

    def run_round_robin(self, quantum: int = TIME_QUANTUM) -> tuple[int, int]:
        """Ejecuta procesos por turnos y devuelve (turnos, tiempo total)."""
        if isinstance(quantum, bool) or not isinstance(quantum, int) or quantum < 1:
            raise ValueError("El quantum debe ser un entero positivo.")

        turns = 0
        total_time = 0

        while not self.is_empty():
            process = self.dequeue()
            executed_time = min(quantum, process.remaining_time)
            process.remaining_time -= executed_time
            turns += 1
            total_time += executed_time

            unit_label = "unidad" if executed_time == 1 else "unidades"
            print(f"Turno {turns}: {process.name} ejecutó {executed_time} {unit_label}.")
            if process.remaining_time > 0:
                # El proceso incompleto vuelve al final de la cola.
                self.enqueue(process)
            else:
                print(f"Proceso terminado: {process.name}")

            remaining = " -> ".join(self.show_pending()) or "Ninguno"
            print("Procesos restantes:", remaining)

        return turns, total_time


def run_demo() -> None:
    """Simula cinco procesos con quantum fijo de tres unidades."""
    queue = ColaCircular(capacity=5)
    initial_processes = [
        ("P1", 7), ("P2", 4), ("P3", 9), ("P4", 2), ("P5", 5)
    ]

    print("PROBLEMA 2 - COLA CIRCULAR ROUND ROBIN")
    for name, execution_time in initial_processes:
        queue.add_process(name, execution_time)

    print("Quantum:", TIME_QUANTUM)
    print("Cola inicial:", " -> ".join(queue.show_pending()))
    print("Procesos registrados:", queue.size())
    print("Primer proceso:", queue.front().name)

    # Se demuestra el error de capacidad sin interrumpir la simulación.
    try:
        queue.add_process("P6", 3)
    except OverflowError as error:
        print("Error controlado:", error)

    turns, total_time = queue.run_round_robin()
    print(f"Resumen: {turns} turnos y {total_time} unidades ejecutadas.")
    print("Cola vacía al finalizar:", queue.is_empty())

    # La misma memoria se puede reutilizar después de completar los procesos.
    queue.add_process("P6", 1)
    print("Nuevo proceso después de finalizar:", queue.front().name)


# La simulación comienza automáticamente al ejecutar este archivo.
run_demo()
