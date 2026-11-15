"""Pruebas de las cuatro soluciones con la biblioteca estándar unittest.

Ejecución desde la carpeta del proyecto:
python -m unittest discover -s tests -v
"""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
import unittest


# Cada archivo ejecuta su demostración al importarse. Se oculta esa salida
# únicamente durante las pruebas; los ejemplos siguen siendo independientes.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
with redirect_stdout(StringIO()):
    import problema1
    import problema2
    import problema3
    import problema4


class BasicQueueTests(unittest.TestCase):
    """Comprueba FIFO, tamaños y errores en una lista enlazada."""

    def test_all_basic_operations(self) -> None:
        queue = problema1.Cola()
        self.assertTrue(queue.is_empty())
        for value in ("A", "B", "C"):
            queue.enqueue(value)
        self.assertEqual(queue.size(), 3)
        self.assertEqual(queue.front(), "A")
        self.assertEqual([queue.dequeue() for _ in range(3)], ["A", "B", "C"])
        self.assertTrue(queue.is_empty())

    def test_empty_queue_and_reuse(self) -> None:
        queue = problema1.Cola()
        with self.assertRaises(IndexError):
            queue.dequeue()
        with self.assertRaises(IndexError):
            queue.front()
        queue.enqueue("Nuevo")
        self.assertEqual(queue.dequeue(), "Nuevo")


class CircularQueueTests(unittest.TestCase):
    """Comprueba rotación de índices, capacidad y Round Robin."""

    def test_circular_reuse(self) -> None:
        queue = problema2.ColaCircular(3)
        for name in ("A", "B", "C"):
            queue.add_process(name, 3)
        self.assertEqual(queue.dequeue().name, "A")
        self.assertEqual(queue.dequeue().name, "B")
        queue.add_process("D", 4)
        queue.add_process("E", 5)
        self.assertEqual([queue.dequeue().name for _ in range(3)], ["C", "D", "E"])
        self.assertTrue(queue.is_empty())

    def test_full_empty_and_invalid_time(self) -> None:
        queue = problema2.ColaCircular(1)
        with self.assertRaises(IndexError):
            queue.front()
        with self.assertRaises(ValueError):
            queue.add_process("Mal", 0)
        queue.add_process("Bien", 1)
        with self.assertRaises(OverflowError):
            queue.add_process("Lleno", 1)

    def test_round_robin_quantum_three(self) -> None:
        queue = problema2.ColaCircular(5)
        for name, time in (("P1", 7), ("P2", 4), ("P3", 9), ("P4", 2), ("P5", 5)):
            queue.add_process(name, time)
        with redirect_stdout(StringIO()):
            turns, total_time = queue.run_round_robin(3)
        self.assertEqual((turns, total_time), (11, 27))
        self.assertTrue(queue.is_empty())


class EmergencyQueueTests(unittest.TestCase):
    """Comprueba prioridad por urgencia y orden de llegada."""

    def test_stable_priorities(self) -> None:
        queue = problema3.ColaEmergencias()
        for name, urgency in (("A", 3), ("B", 1), ("C", 3), ("D", 1), ("E", 5)):
            queue.add_patient(name, urgency)
        self.assertEqual(queue.front().name, "B")
        self.assertEqual(queue.size(), 5)
        self.assertEqual(
            [queue.attend_next().name for _ in range(5)],
            ["B", "D", "A", "C", "E"],
        )

    def test_invalid_urgencies_and_empty_queue(self) -> None:
        queue = problema3.ColaEmergencias()
        for urgency in (0, 6, 1.5, True):
            with self.assertRaises(ValueError):
                queue.add_patient("Prueba", urgency)
        with self.assertRaises(IndexError):
            queue.attend_next()


class BankQueueTests(unittest.TestCase):
    """Verifica la mezcla de colas por servicio y las prioridades."""

    def test_priority_and_fifo_in_each_service(self) -> None:
        bank = problema4.BankSystem()
        customers = [
            ("Normal1", "Caja", "Normal"),
            ("Premium1", "Caja", "Premium"),
            ("Senior", "Caja", "Adulto mayor"),
            ("Premium2", "Caja", "Premium"),
            ("Normal2", "Caja", "Normal"),
            ("Otro", "Consultas", "Normal"),
        ]
        for customer in customers:
            bank.add_customer(*customer)
        self.assertEqual(
            [bank.attend_next("Caja").name for _ in range(5)],
            ["Senior", "Premium1", "Premium2", "Normal1", "Normal2"],
        )
        self.assertEqual(bank.attend_next("Consultas").name, "Otro")

    def test_empty_invalid_service_and_category(self) -> None:
        bank = problema4.BankSystem()
        with self.assertRaises(IndexError):
            bank.attend_next("Caja")
        with self.assertRaises(ValueError):
            bank.add_customer("X", "Otro servicio", "Normal")
        with self.assertRaises(ValueError):
            bank.add_customer("X", "Caja", "Desconocida")

