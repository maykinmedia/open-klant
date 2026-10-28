import threading

from django.db import connection, transaction
from django.test import TransactionTestCase

from openklant.components.klantinteracties.models import Klantcontact

THREADS = 10


class NummerConcurrencyTests(TransactionTestCase):
    def test_concurrent_creates_get_unique_nummers(self):
        barrier = threading.Barrier(THREADS)
        nummers, errors = [], []
        lock = threading.Lock()

        def create():
            try:
                with transaction.atomic():
                    klantcontact = Klantcontact.objects.create(
                        vertrouwelijk=False, nummer=""
                    )
                    barrier.wait(timeout=10)
                with lock:
                    nummers.append(klantcontact.nummer)
            except Exception as exc:  # noqa: BLE001
                barrier.abort()
                with lock:
                    errors.append(exc)
            finally:
                connection.close()

        threads = [threading.Thread(target=create) for _ in range(THREADS)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(errors, [])

        self.assertEqual(len(nummers), THREADS)
        for nummer in nummers:
            self.assertRegex(nummer, r"^[0-9]{12}$")

        self.assertEqual(len(set(nummers)), THREADS)
        self.assertEqual(
            Klantcontact.objects.values("nummer").distinct().count(), THREADS
        )

    def test_rolled_back_nummer_is_not_reused(self):
        with self.assertRaises(RuntimeError):
            with transaction.atomic():
                rolled_back = Klantcontact.objects.create(
                    vertrouwelijk=False, nummer=""
                )
                raise RuntimeError("rollback")

        klantcontact = Klantcontact.objects.create(vertrouwelijk=False, nummer="")

        self.assertGreater(int(klantcontact.nummer), int(rolled_back.nummer))
