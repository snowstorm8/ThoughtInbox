import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import utils.drafts as draft_module


class TestDraftManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()

        self.original_path = draft_module.DRAFT_FILE

        draft_module.DRAFT_FILE = (
            Path(self.temp_dir.name) / "drafts.txt"
        )

    def tearDown(self):
        draft_module.DRAFT_FILE = self.original_path
        self.temp_dir.cleanup()

    def test_save_and_load(self):

        text = "This is my unsaved thought."

        draft_module.DraftManager.save(text)

        loaded = draft_module.DraftManager.load()

        self.assertEqual(
            loaded,
            text
        )

    def test_load_missing_draft(self):

        loaded = draft_module.DraftManager.load()

        self.assertEqual(
            loaded,
            ""
        )

    def test_clear_draft(self):

        draft_module.DraftManager.save(
            "Temporary draft"
        )

        draft_module.DraftManager.clear()

        self.assertFalse(
            draft_module.DRAFT_FILE.exists()
        )

        self.assertEqual(
            draft_module.DraftManager.load(),
            ""
        )

    def test_overwrite_draft(self):

        draft_module.DraftManager.save(
            "First draft"
        )

        draft_module.DraftManager.save(
            "Second draft"
        )

        self.assertEqual(
            draft_module.DraftManager.load(),
            "Second draft"
        )
        
    def test_multiline_draft(self):
        text = """This is a thought
    with multiple lines.

    And another paragraph."""

        draft_module.DraftManager.save(text)

        loaded = draft_module.DraftManager.load()

        self.assertEqual(
            loaded,
            text
        )


    def test_empty_draft(self):

        draft_module.DraftManager.save("")

        loaded = draft_module.DraftManager.load()

        self.assertEqual(
            loaded,
            "" 
        )


    def test_unicode_draft(self):

        text = "Café ☕ — माँ — 数学"

        draft_module.DraftManager.save(text)

        loaded = draft_module.DraftManager.load()

        self.assertEqual(
            loaded,
            text
        )


    def test_clear_is_idempotent(self):

        # Clearing when there is no draft should not fail.
        draft_module.DraftManager.clear()

        draft_module.DraftManager.clear()

        self.assertEqual(
            draft_module.DraftManager.load(),
            ""
    )
        
    def test_draft_survives_new_session(self):

        text = "This draft should survive."

        draft_module.DraftManager.save(text)

        # Simulate closing and reopening the application
        loaded = draft_module.DraftManager.load()

        self.assertEqual(
            loaded,
            text
        )
        
    def test_latest_autosave_replaces_previous_draft(self):
        draft_module.DraftManager.save(
            "First version"
        )

        draft_module.DraftManager.save(
            "Second version"
        )

        loaded = draft_module.DraftManager.load()

        self.assertEqual(
            loaded,
            "Second version"
        )
        
    def test_clearing_draft_removes_persisted_text(self):
        draft_module.DraftManager.save(
            "Draft that should disappear"
        )

        draft_module.DraftManager.clear()

        self.assertEqual(
            draft_module.DraftManager.load(),
            ""
        )
        
    def test_large_draft(self):
        text = "ThoughtInbox " * 10000

        draft_module.DraftManager.save(
            text
        )

        loaded = draft_module.DraftManager.load()

        self.assertEqual(
            loaded,
            text
        )
        
    


if __name__ == "__main__":
    unittest.main()