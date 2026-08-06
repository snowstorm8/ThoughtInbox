import unittest

from database import Database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database(":memory:")

    def tearDown(self):
        self.db.close()

    # --------------------------------------------------
    # THOUGHTS
    # --------------------------------------------------

    def test_add_thought(self):

        thought_id = self.db.add_thought(
            "Buy flowers for Mom"
        )

        thought = self.db.get_thought(
            thought_id
        )

        self.assertIsNotNone(thought)
        self.assertEqual(
            thought[1],
            "Buy flowers for Mom"
        )

    def test_update_thought(self):

        thought_id = self.db.add_thought(
            "Buy flowers"
        )

        self.db.update(
            thought_id,
            "Buy flowers for Mom"
        )

        thought = self.db.get_thought(
            thought_id
        )

        self.assertEqual(
            thought[1],
            "Buy flowers for Mom"
        )

    def test_delete_thought(self):

        thought_id = self.db.add_thought(
            "Temporary thought"
        )

        self.db.delete(thought_id)

        thought = self.db.get_thought(
            thought_id
        )

        self.assertIsNone(thought)

    def test_restore_thought(self):

        thought_id = self.db.add_thought(
            "Important thought"
        )

        original = self.db.get_thought(
            thought_id
        )

        self.db.delete(thought_id)

        self.db.restore_thought(
            original[0],
            original[1],
            original[2],
            original[3]
        )

        restored = self.db.get_thought(
            thought_id
        )

        self.assertIsNotNone(restored)
        self.assertEqual(
            restored[1],
            "Important thought"
        )

    # --------------------------------------------------
    # FAVORITES
    # --------------------------------------------------

    def test_toggle_favorite(self):

        thought_id = self.db.add_thought(
            "Favorite thought"
        )

        self.assertFalse(
            self.db.is_favorite(thought_id)
        )

        self.db.toggle_favorite(
            thought_id
        )

        self.assertTrue(
            self.db.is_favorite(thought_id)
        )

        self.db.toggle_favorite(
            thought_id
        )

        self.assertFalse(
            self.db.is_favorite(thought_id)
        )

    def test_get_only_favorites(self):

        favorite_id = self.db.add_thought(
            "Favorite"
        )

        normal_id = self.db.add_thought(
            "Normal"
        )

        self.db.toggle_favorite(
            favorite_id
        )

        favorites = self.db.get_only_favorite()

        ids = [
            thought[0]
            for thought in favorites
        ]

        self.assertIn(
            favorite_id,
            ids
        )

        self.assertNotIn(
            normal_id,
            ids
        )

    # --------------------------------------------------
    # TAGS
    # --------------------------------------------------

    def test_assign_tag(self):

        thought_id = self.db.add_thought(
            "Birthday planning"
        )

        self.db.assign_tag(
            thought_id,
            "birthday"
        )

        tags = self.db.get_tags(
            thought_id
        )

        self.assertIn(
            "birthday",
            tags
        )

    def test_multiple_tags(self):

        thought_id = self.db.add_thought(
            "Birthday planning"
        )

        self.db.assign_tag(
            thought_id,
            "birthday"
        )

        self.db.assign_tag(
            thought_id,
            "family"
        )

        tags = self.db.get_tags(
            thought_id
        )

        self.assertEqual(
            set(tags),
            {"birthday", "family"}
        )

    def test_duplicate_tag_assignment(self):

        thought_id = self.db.add_thought(
            "Birthday planning"
        )

        self.db.assign_tag(
            thought_id,
            "birthday"
        )

        self.db.assign_tag(
            thought_id,
            "birthday"
        )

        tags = self.db.get_tags(
            thought_id
        )

        self.assertEqual(
            tags.count("birthday"),
            1
        )

    def test_remove_tag(self):

        thought_id = self.db.add_thought(
            "Birthday planning"
        )

        self.db.assign_tag(
            thought_id,
            "birthday"
        )

        self.db.remove_tag(
            thought_id,
            "birthday"
        )

        tags = self.db.get_tags(
            thought_id
        )

        self.assertNotIn(
            "birthday",
            tags
        )

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def test_text_search(self):

        self.db.add_thought(
            "Buy flowers"
        )

        self.db.add_thought(
            "Finish homework"
        )

        results = self.db.search(
            "flowers"
        )

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0][1],
            "Buy flowers"
        )

    def test_search_is_case_insensitive(self):

        self.db.add_thought(
            "Buy Flowers"
        )

        results = self.db.search(
            "flowers"
        )

        self.assertEqual(
            len(results),
            1
        )

    def test_favorite_search(self):

        favorite_id = self.db.add_thought(
            "Important"
        )

        self.db.add_thought(
            "Not important"
        )

        self.db.toggle_favorite(
            favorite_id
        )

        results = self.db.search(
            "",
            favorites_only=True
        )

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0][0],
            favorite_id
        )

    def test_tag_search(self):

        birthday_id = self.db.add_thought(
            "Birthday planning"
        )

        other_id = self.db.add_thought(
            "Study for exam"
        )

        self.db.assign_tag(
            birthday_id,
            "birthday"
        )

        results = self.db.search_tag(
            "birthday"
        )

        ids = [
            thought[0]
            for thought in results
        ]

        self.assertIn(
            birthday_id,
            ids
        )

        self.assertNotIn(
            other_id,
            ids
        )

    def test_tag_search_has_no_duplicates(self):

        thought_id = self.db.add_thought(
            "Birthday planning"
        )

        self.db.assign_tag(
            thought_id,
            "birthday"
        )

        self.db.assign_tag(
            thought_id,
            "birthday-planning"
        )

        results = self.db.search_tag(
            "birthday"
        )

        ids = [
            thought[0]
            for thought in results
        ]

        self.assertEqual(
            ids.count(thought_id),
            1
        )

    # --------------------------------------------------
    # REMINDERS
    # --------------------------------------------------

    def test_add_reminder(self):

        thought_id = self.db.add_thought(
            "Call Mom"
        )

        reminder_id = self.db.add_reminder(
            thought_id,
            "2099-01-01T12:00:00+00:00"
        )

        reminder = self.db.get_pending_reminder(
            thought_id
        )

        self.assertIsNotNone(
            reminder
        )

        self.assertEqual(
            reminder[0],
            reminder_id
        )

    def test_update_reminder(self):

        thought_id = self.db.add_thought(
            "Call Mom"
        )

        reminder_id = self.db.add_reminder(
            thought_id,
            "2099-01-01T12:00:00+00:00"
        )

        new_time = (
            "2099-02-01T12:00:00+00:00"
        )

        self.db.update_reminder(
            reminder_id,
            new_time
        )

        reminder = self.db.get_pending_reminder(
            thought_id
        )

        self.assertEqual(
            reminder[1],
            new_time
        )

    def test_delete_reminder(self):

        thought_id = self.db.add_thought(
            "Call Mom"
        )

        reminder_id = self.db.add_reminder(
            thought_id,
            "2099-01-01T12:00:00+00:00"
        )

        self.db.delete_reminder(
            reminder_id
        )

        reminder = self.db.get_pending_reminder(
            thought_id
        )

        self.assertIsNone(
            reminder
        )

    def test_reminder_cascades_when_thought_deleted(self):

        thought_id = self.db.add_thought(
            "Call Mom"
        )

        self.db.add_reminder(
            thought_id,
            "2099-01-01T12:00:00+00:00"
        )

        self.db.delete(
            thought_id
        )

        reminders = self.db.get_reminder(
            thought_id
        )

        self.assertEqual(
            reminders,
            []
        )
        
    def test_due_reminder_is_returned(self):
        thought_id = self.db.add_thought(
            "Call Mom"
        )

        reminder_id = self.db.add_reminder(
            thought_id,
            "2000-01-01T12:00:00+00:00"
        )

        due = self.db.get_due_reminders()

        self.assertEqual(
            len(due),
            1
        )

        self.assertEqual(
            due[0][0],
            reminder_id
        )

        self.assertEqual(
            due[0][1],
            thought_id
        )

    def test_triggered_reminder_is_not_returned_as_due(self):
        thought_id = self.db.add_thought(
            "Call Mom"
        )

        reminder_id = self.db.add_reminder(
            thought_id,
            "2000-01-01T12:00:00+00:00"
        )

        self.db.mark_reminder_triggered(
            reminder_id
        )

        due = self.db.get_due_reminders()

        self.assertEqual(
            due,
            []
        )

    def test_tag_search_returns_one_result_per_thought(self):
        thought_id = self.db.add_thought(
            "Mom's birthday"
        )

        self.db.assign_tag(
            thought_id,
            "birthday"
        )

        self.db.assign_tag(
            thought_id,
            "birthday-planning"
        )

        results = self.db.search_tag(
            "birthday"
        )

        matching_ids = [
            row[0]
            for row in results
        ]

        self.assertEqual(
            matching_ids.count(thought_id),
            1
        )
        
    def test_delete_removes_thought_and_cascades_reminder(self):
        thought_id = self.db.add_thought(
            "Important thought"
        )

        self.db.add_reminder(
            thought_id,
            "2099-01-01T12:00:00+00:00"
        )

        self.db.delete(thought_id)

        self.assertIsNone(
            self.db.get_thought(thought_id)
        )

        self.assertEqual(
            self.db.get_reminder(thought_id),
            []
        )
        
    def test_thought_metadata_can_be_captured_before_delete(self):
        thought_id = self.db.add_thought(
            "Birthday planning"
        )

        self.db.toggle_favorite(
            thought_id
        )

        self.db.assign_tag(
            thought_id,
            "birthday"
        )

        self.db.assign_tag(
            thought_id,
            "family"
        )

        self.db.add_reminder(
            thought_id,
            "2099-01-01T12:00:00+00:00"
        )

        thought = self.db.get_thought(
            thought_id
        )

        tags = self.db.get_tags(
            thought_id
        )

        reminder = self.db.get_pending_reminder(
            thought_id
        )

        self.assertEqual(
            thought[1],
            "Birthday planning"
        )

        self.assertEqual(
            thought[3],
            1
        )

        self.assertEqual(
            set(tags),
            {"birthday", "family"}
        )

        self.assertIsNotNone(
            reminder
        )    
        
    def test_full_thought_restore(self):
        thought_id = self.db.add_thought(
            "Birthday planning"
        )

        self.db.toggle_favorite(
            thought_id
        )

        self.db.assign_tag(
            thought_id,
            "birthday"
        )

        self.db.assign_tag(
            thought_id,
            "family"
        )

        self.db.add_reminder(
            thought_id,
            "2099-01-01T12:00:00+00:00"
        )

        original = self.db.get_thought(
            thought_id
        )

        tags = self.db.get_tags(
            thought_id
        )

        reminder = self.db.get_pending_reminder(
            thought_id
        )

        # Delete
        self.db.delete(
            thought_id
        )

        self.assertIsNone(
            self.db.get_thought(thought_id)
        )

        # Restore
        self.db.restore_thought(
            original[0],
            original[1],
            original[2],
            original[3]
        )

        for tag in tags:
            self.db.assign_tag(
                thought_id,
                tag
            )

        if reminder is not None:
            self.db.add_reminder(
                thought_id,
                reminder[1]
            )

        # Verify restoration
        restored = self.db.get_thought(
            thought_id
        )

        self.assertIsNotNone(
            restored
        )

        self.assertEqual(
            restored[1],
            "Birthday planning"
        )

        self.assertEqual(
            restored[3],
            1
        )

        restored_tags = self.db.get_tags(
            thought_id
        )

        self.assertEqual(
            set(restored_tags),
            {"birthday", "family"}
        )

        restored_reminder = (
            self.db.get_pending_reminder(
                thought_id
            )
        )

        self.assertIsNotNone(
            restored_reminder
        )

        self.assertEqual(
            restored_reminder[1],
            "2099-01-01T12:00:00+00:00"
        )
    
    def test_thought_persists_after_database_reopen(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = str(
                Path(temp_dir) / "test.db"
            )

            db = Database(db_path)

            thought_id = db.add_thought(
                "Persistent thought"
            )

            db.close()

            db = Database(db_path)

            thought = db.get_thought(
                thought_id
            )

            self.assertIsNotNone(
                thought
            )

            self.assertEqual(
                thought[1],
                "Persistent thought"
            )

            db.close()
            
    def test_thought_metadata_persists_after_database_reopen(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = str(
                Path(temp_dir) / "test.db"
            )

            db = Database(db_path)

            thought_id = db.add_thought(
                "Mom's birthday"
            )

            db.toggle_favorite(
                thought_id
            )

            db.assign_tag(
                thought_id,
                "birthday"
            )

            db.assign_tag(
                thought_id,
                "family"
            )

            db.add_reminder(
                thought_id,
                "2099-01-01T12:00:00+00:00"
            )

            db.close()

            db = Database(db_path)

            thought = db.get_thought(
                thought_id
            )

            tags = db.get_tags(
                thought_id
            )

            reminder = db.get_pending_reminder(
                thought_id
            )

            self.assertEqual(
                thought[1],
                "Mom's birthday"
            )

            self.assertEqual(
                thought[3],
                1
            )

            self.assertEqual(
                set(tags),
                {"birthday", "family"}
            )

            self.assertIsNotNone(
                reminder
            )

            self.assertEqual(
                reminder[1],
                "2099-01-01T12:00:00+00:00"
            )

            db.close()
    
    def test_deleted_thought_stays_deleted_after_reopen(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = str(
                Path(temp_dir) / "test.db"
            )

            db = Database(db_path)

            thought_id = db.add_thought(
                "Delete me"
            )

            db.delete(
                thought_id
            )

            db.close()

            db = Database(db_path)

            thought = db.get_thought(
                thought_id
            )

            self.assertIsNone(
                thought
            )

            db.close()
            
    def test_triggered_reminder_stays_triggered_after_reopen(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = str(
                Path(temp_dir) / "test.db"
            )

            db = Database(db_path)

            thought_id = db.add_thought(
                "Call Mom"
            )

            reminder_id = db.add_reminder(
                thought_id,
                "2000-01-01T12:00:00+00:00"
            )

            db.mark_reminder_triggered(
                reminder_id
            )

            db.close()

            db = Database(db_path)

            due = db.get_due_reminders()

            self.assertEqual(
                due,
                []
            )

            db.close()
            
    def test_reminder_update_changes_due_time(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = str(Path(temp_dir) / "test.db")

            db = Database(db_path)

            thought_id = db.add_thought("Test reminder")

            reminder_id = db.add_reminder(
                thought_id,
                "2099-01-01T12:00:00+00:00"
            )

            db.update_reminder(
                reminder_id,
                "2000-01-01T12:00:00+00:00"
            )

            due = db.get_due_reminders()

            self.assertEqual(len(due), 1)
            self.assertEqual(due[0][0], reminder_id)
            
            db.close()
        
    def test_deleted_reminder_is_not_due(self):
        thought_id = self.db.add_thought(
            "Reminder to delete"
        )

        reminder_id = self.db.add_reminder(
            thought_id,
            "2000-01-01T12:00:00+00:00"
        )

        self.db.delete_reminder(
            reminder_id
        )

        due = self.db.get_due_reminders()

        self.assertEqual(
            due,
            []
        )
        
    def test_multiple_reminders_are_returned_in_time_order(self):
        thought_id = self.db.add_thought(
            "Multiple reminders"
        )

        first = self.db.add_reminder(
            thought_id,
            "2027-01-01T12:00:00+00:00"
        )

        second = self.db.add_reminder(
            thought_id,
            "2026-01-01T12:00:00+00:00"
        )

        third = self.db.add_reminder(
            thought_id,
            "2028-01-01T12:00:00+00:00"
        )

        reminders = self.db.get_reminder(
            thought_id
        )

        reminder_times = [
            reminder[1]
            for reminder in reminders
        ]

        self.assertEqual(
            set(reminder_times),
            {
                "2026-01-01T12:00:00+00:00",
                "2027-01-01T12:00:00+00:00",
                "2028-01-01T12:00:00+00:00"
            }
        )
        
    def test_deleting_thought_removes_its_reminders(self):
        thought_id = self.db.add_thought(
            "Thought with reminders"
        )

        self.db.add_reminder(
            thought_id,
            "2099-01-01T12:00:00+00:00"
        )

        self.db.add_reminder(
            thought_id,
            "2099-02-01T12:00:00+00:00"
        )

        self.db.delete(
            thought_id
        )

        self.assertEqual(
            self.db.get_reminder(thought_id),
            []
        )
        
    
            
if __name__ == "__main__":
    unittest.main()