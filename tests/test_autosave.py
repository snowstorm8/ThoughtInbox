import unittest
from unittest.mock import Mock, patch

from app import ThoughtInbox


class TestAutosave(unittest.TestCase):

    def setUp(self):
        self.app = ThoughtInbox.__new__(
            ThoughtInbox
        )

        self.app.autosave_job = None

        self.app.settings = Mock()
        self.app.input_panel = Mock()

    def test_autosave_saves_text(self):

        self.app.input_panel.textbox.get.return_value = (
            "This should be autosaved."
        )

        with patch(
            "app.DraftManager.save"
        ) as mock_save:

            self.app.autosave()

            mock_save.assert_called_once_with(
                "This should be autosaved."
            )

    def test_autosave_saves_multiline_text(self):

        text = (
            "First line\n"
            "Second line\n"
            "Third line"
        )

        self.app.input_panel.textbox.get.return_value = text

        with patch(
            "app.DraftManager.save"
        ) as mock_save:

            self.app.autosave()

            mock_save.assert_called_once_with(
                text
            )

    def test_autosave_does_not_modify_text(self):

        text = "Original draft"

        self.app.input_panel.textbox.get.return_value = text

        with patch(
            "app.DraftManager.save"
        ) as mock_save:

            self.app.autosave()

            self.assertEqual(
                self.app.input_panel.textbox.get(
                    "1.0",
                    "end-1c"
                ),
                text
            )

            mock_save.assert_called_once_with(
                text
            )
            
    def test_autosave_not_scheduled_when_disabled(self):

        self.app.settings.get.return_value = False

        with patch.object(
            self.app,
            "after"
        ) as mock_after:

            self.app.schedule_autosave()

            mock_after.assert_not_called()

    def test_autosave_is_scheduled(self):

        self.app.settings.get.side_effect = [
            True,
            1000
        ]

        self.app.after = Mock(
            return_value="autosave_job_1"
        )

        self.app.schedule_autosave()

        self.app.after.assert_called_once_with(
            1000,
            self.app.autosave
        )

        self.assertEqual(
            self.app.autosave_job,
            "autosave_job_1"
        )

    def test_existing_autosave_is_cancelled(self):

        self.app.autosave_job = "old_job"

        self.app.settings.get.side_effect = [
            True,
            1000
        ]

        self.app.after_cancel = Mock()

        self.app.after = Mock(
            return_value="new_job"
        )

        self.app.schedule_autosave()

        self.app.after_cancel.assert_called_once_with(
            "old_job"
        )

        self.app.after.assert_called_once_with(
            1000,
            self.app.autosave
        )

        self.assertEqual(
            self.app.autosave_job,
            "new_job"
        )


if __name__ == "__main__":
    unittest.main()