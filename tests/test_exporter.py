import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from database import Database
from utils.exporter import Exporter


class TestExporter(unittest.TestCase):

    def setUp(self):

        self.temp_dir = TemporaryDirectory()

        self.db = Database(":memory:")

        self.thought_id = self.db.add_thought(
            "Buy flowers for Mom"
        )

        self.db.assign_tag(
            self.thought_id,
            "birthday"
        )

        self.db.assign_tag(
            self.thought_id,
            "family"
        )

        self.db.toggle_favorite(
            self.thought_id
        )

        self.thoughts = self.db.get_thoughts()

    def tearDown(self):

        self.db.close()
        self.temp_dir.cleanup()

    def test_export_txt(self):

        path = (
            Path(self.temp_dir.name)
            / "export.txt"
        )

        with patch(
            "utils.exporter.Database",
            return_value=self.db
        ):

            Exporter.export_txt(
                path,
                self.thoughts
            )

        content = path.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Buy flowers for Mom",
            content
        )

        self.assertIn(
            "#birthday",
            content
        )

        self.assertIn(
            "#family",
            content
        )

        self.assertIn(
            "*Favorite Thought*",
            content
        )

    def test_export_markdown(self):

        path = (
            Path(self.temp_dir.name)
            / "export.md"
        )

        with patch(
            "utils.exporter.Database",
            return_value=self.db
        ):

            Exporter.export_markdown(
                path,
                self.thoughts
            )

        content = path.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "# ThoughtInbox Export",
            content
        )

        self.assertIn(
            "Buy flowers for Mom",
            content
        )

        self.assertIn(
            "#birthday",
            content
        )

        self.assertIn(
            "**Favorite Thought**",
            content
        )

    def test_export_json(self):

        path = (
            Path(self.temp_dir.name)
            / "export.json"
        )

        with patch(
            "utils.exporter.Database",
            return_value=self.db
        ):

            Exporter.export_json(
                path,
                self.thoughts
            )

        with open(
            path,
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        self.assertEqual(
            len(data),
            1
        )

        thought = data[0]

        self.assertEqual(
            thought["thought"],
            "Buy flowers for Mom"
        )

        self.assertTrue(
            thought["favorite"]
        )

        self.assertEqual(
            set(thought["tags"]),
            {"birthday", "family"}
        )

    def test_json_export_is_valid_json(self):

        path = (
            Path(self.temp_dir.name)
            / "export.json"
        )

        with patch(
            "utils.exporter.Database",
            return_value=self.db
        ):

            Exporter.export_json(
                path,
                self.thoughts
            )

        content = path.read_text(
            encoding="utf-8"
        )

        data = json.loads(content)

        self.assertIsInstance(
            data,
            list
        )


if __name__ == "__main__":
    unittest.main()