import os.path
import shutil
from hashlib import md5
from pathlib import Path


def expand_path(path: str) -> str:
    p = Path(path)
    p.resolve()
    return str(p.expanduser())


class Storage:

    def __init__(self, filename: str):
        self.filename = filename
        if filename == "memory":
            self.data = ""
        else:
            self.filename = expand_path(self.filename)

    def read(self):
        if self.filename == "memory":
            return self.data
        else:
            if os.path.exists(self.filename):
                return self._read_internal()
            return ""

    def _read_internal(self):
        data, data_hash = self._read_raw(self.filename)
        calculated_hash = md5(str.encode(data)).digest()
        if data_hash == calculated_hash:
            return data

        # failed hash
        backup_filename = self.filename + ".bak"
        data, data_hash = self._read_raw(backup_filename)
        calculated_hash = md5(str.encode(data)).digest()
        if data_hash == calculated_hash:
            return data

        raise Exception("Invalid hash in both live and backup file")

    def _read_raw(self, filename: str):
        if os.path.exists(filename):
            with (open(filename, "rt")) as f:
                data_hash = bytes.fromhex(f.readline()[:-1])
                data = f.read()

            return data, data_hash,
        return "", "",

    def write(self, data: str):
        if self.filename == "memory":
            self.data = data
        else:
            self._write_internal(data)

    def _write_internal(self, data: str):
        if os.path.exists(self.filename):
            backup_filename = self.filename + ".bak"
            if os.path.exists(backup_filename):
                os.remove(backup_filename)
            shutil.copyfile(self.filename, backup_filename)
        calculated_hash = md5(str.encode(data)).digest()
        with (open(self.filename, "wt")) as f:
            f.write(calculated_hash.hex())
            f.write("\n")
            f.write(data)
