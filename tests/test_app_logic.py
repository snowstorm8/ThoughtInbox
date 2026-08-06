import unittest
from unittest.mock import Mock, patch

from app import ThoughtInbox


class TestAppLogic(unittest.TestCase):

    def setUp(self):
        self.app = ThoughtInbox.__new__(
            ThoughtInbox
        )

        self.app.db = Mock()
        self.app.input_panel = Mock()
        self.app.status_bar = Mock()
        self.app.editing_id = None
        self.app.undo_stack = []
        self.app.undo_timer = None

    def test_save_empty_thought_does_nothing(self):

        self.app.input_panel.textbox.get.return_value = "   "

        self.app.save_thought()

        self.app.db.add_thought.assert_not_called()
        self.app.db.update.assert_not_called()

    def test_save_thought_creates_new_thought(self):

        self.app.input_panel.textbox.get.return_value = (
            "This is a thought"
        )

        self.app.db.add_thought.return_value = 42

        with patch(
            "app.DraftManager.clear"
        ) as clear:

            self.app.refresh = Mock()

            self.app.save_thought()

        self.app.db.add_thought.assert_called_once_with(
            "This is a thought"
        )

        clear.assert_called_once()

        self.app.input_panel.textbox.delete.assert_called_once_with(
            "1.0",
            "end"
        )

    def test_save_thought_extracts_and_assigns_tags(self):

        self.app.input_panel.textbox.get.return_value = (
            "Study #math and #physics"
        )

        self.app.db.add_thought.return_value = 10
        self.app.refresh = Mock()

        with patch(
            "app.DraftManager.clear"
        ):

            self.app.save_thought()

        self.app.db.assign_tag.assert_any_call(
            10,
            "math"
        )

        self.app.db.assign_tag.assert_any_call(
            10,
            "physics"
        )

        self.assertEqual(
            self.app.db.assign_tag.call_count,
            2
        )

    def test_tags_are_normalized_to_lowercase(self):

        self.app.input_panel.textbox.get.return_value = (
            "Test #Math #PYTHON"
        )

        self.app.db.add_thought.return_value = 5
        self.app.refresh = Mock()

        with patch(
            "app.DraftManager.clear"
        ):

            self.app.save_thought()

        self.app.db.assign_tag.assert_any_call(
            5,
            "math"
        )

        self.app.db.assign_tag.assert_any_call(
            5,
            "python"
        )

    def test_edit_thought_sets_editing_id(self):

        self.app.edit_thought(
            25,
            "Updated thought"
        )

        self.assertEqual(
            self.app.editing_id,
            25
        )

        self.app.input_panel.textbox.delete.assert_called_once_with(
            "1.0",
            "end"
        )

        self.app.input_panel.textbox.insert.assert_called_once_with(
            "1.0",
            "Updated thought"
        )

        self.app.input_panel.save_button.configure.assert_called_once_with(
            text="Update Thought"
        )

    def test_cancel_edit_clears_editing_state(self):

        self.app.editing_id = 25
        self.app.refresh = Mock()

        self.app.cancel_edit()

        self.assertIsNone(
            self.app.editing_id
        )

        self.app.input_panel.textbox.delete.assert_called_once_with(
            "1.0",
            "end"
        )

        self.app.input_panel.save_button.configure.assert_called_once_with(
            text="Save Thought"
        )

        self.app.refresh.assert_called_once()

    def test_clear_search_clears_search_entry(self):

        self.app.refresh = Mock()

        self.app.clear_search()

        self.app.input_panel.search_entry.delete.assert_called_once_with(
            0,
            "end"
        )

        self.app.refresh.assert_called_once()

    def test_search_tag_sets_tag_query(self):

        self.app.refresh = Mock()

        self.app.search_tag(
            "python"
        )

        self.app.input_panel.search_entry.delete.assert_called_once_with(
            0,
            "end"
        )

        self.app.input_panel.search_entry.insert.assert_called_once_with(
            0,
            "#python"
        )

        self.app.refresh.assert_called_once()

    def test_show_reminder_marks_it_triggered(self):

        with patch(
            "app.messagebox.showinfo"
        ) as showinfo:

            self.app.show_reminders(
                7,
                "Call Mom"
            )

        self.app.db.mark_reminder_triggered.assert_called_once_with(
            7
        )

        showinfo.assert_called_once_with(
            "ThoughtInbox Reminder",
            "Call Mom"
        )

    def test_show_reminder_truncates_long_preview(self):

        text = "A" * 150

        with patch(
            "app.messagebox.showinfo"
        ) as showinfo:

            self.app.show_reminders(
                7,
                text
            )

        preview = showinfo.call_args.args[1]

        self.assertEqual(
            len(preview),
            103
        )

        self.assertTrue(
            preview.endswith("...")
        )


if __name__ == "__main__":
    unittest.main()