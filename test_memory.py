import json
import tempfile
import unittest
from pathlib import Path

from memory_store import clear_memory, load_memory, save_memory


class MemoryStoreTests(unittest.TestCase):
    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "memory.json"
            self.assertEqual(load_memory(str(path)), [])

    def test_save_and_load_round_trip(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"},
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "memory.json"
            save_memory(messages, str(path))
            self.assertEqual(load_memory(str(path)), messages)

    def test_invalid_items_are_ignored(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "memory.json"
            path.write_text(
                json.dumps([
                    {"role": "user", "content": "Hello"},
                    {"role": "system", "content": "unexpected"},
                    "not a message",
                ]),
                encoding="utf-8",
            )
            self.assertEqual(
                load_memory(str(path)),
                [{"role": "user", "content": "Hello"}],
            )

    def test_clear_memory(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "memory.json"
            save_memory([{"role": "user", "content": "Hello"}], str(path))
            clear_memory(str(path))
            self.assertEqual(load_memory(str(path)), [])


if __name__ == "__main__":
    unittest.main()
