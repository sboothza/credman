import os.path
import unittest

from mockito import mock, when

from src.passman import Passman
from src.storage import Storage


class TestPassman(unittest.TestCase):
    def setUp(self):
        self.salt = b'ed\xd9\xf1+\x07\xa7K|\n)6YgUy'

    def test_storage_read_write_virtual(self):
        self.mock_storage = mock(spec=Storage)
        when(Storage).read().thenReturn("data")
        when(Storage).write(...)
        storage = Storage("test")
        storage.write("data")
        self.assertEqual("data", storage.read())

    def test_storage_read_write_actual(self):
        if os.path.exists("test"):
            os.remove("test")

        storage = Storage("test")
        storage.write("my name is bob")
        storage.write("my name is still bob")
        data = storage.read()
        self.assertEqual("my name is still bob", data)
        os.remove("test")
        if os.path.exists("test.bak"):
            os.remove("test.bak")

    def test_storage_actual_backup(self):
        if os.path.exists("test"):
            os.remove("test")
        if os.path.exists("test.bak"):
            os.remove("test.bak")

        storage = Storage("test")
        storage.write("my name is bob")
        storage.write("my name is still bob")
        # break the file
        with (open("test", "at")) as f:
            f.write("\n")
        data = storage.read()
        self.assertEqual("my name is bob", data)

        if os.path.exists("test"):
            os.remove("test")
        if os.path.exists("test.bak"):
            os.remove("test.bak")

    def test_storage_memory(self):
        storage = Storage("memory")
        storage.write("my name is bob")
        storage.write("my name is still bob")
        data = storage.read()
        self.assertEqual("my name is still bob", data)

    def test_passman_basic(self):
        storage = Storage("memory")
        passman = Passman(storage, self.salt, "masterpass")
        passman.set_password("app1", "pass1")
        passman.set_password("app2", "pass2")
        self.assertEqual(passman.get_password("app1"), "pass1")
        self.assertEqual(passman.get_password("app2"), "pass2")
        self.assertEqual(passman.get_password("app3"), "")

    def test_passman_virtual(self):
        storage = Storage("memory")
        passman = Passman(storage, self.salt, "masterpass")
        passman.set_password("app1", "pass1")
        passman.set_password("app2", "pass2")
        passman.save()

        passman2 = Passman(storage, self.salt, "masterpass")
        self.assertEqual(passman2.get_password("app1"), "pass1")
        self.assertEqual(passman2.get_password("app2"), "pass2")
        self.assertEqual(passman2.get_password("app3"), "")

    def test_passman_file(self):
        storage = Storage("test")
        passman = Passman(storage, self.salt, "masterpass")
        passman.set_password("app1", "pass1")
        passman.set_password("app2", "pass2")
        passman.save()

        storage2 = Storage("test")
        passman2 = Passman(storage2, self.salt, "masterpass")
        self.assertEqual(passman2.get_password("app1"), "pass1")
        self.assertEqual(passman2.get_password("app2"), "pass2")
        self.assertEqual(passman2.get_password("app3"), "")


if __name__ == "__main__":
    unittest.main()
