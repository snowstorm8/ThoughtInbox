import unittest

from database import Database


class TestSearchIntegration(unittest.TestCase):

    def setUp(self):
        self.db = Database(":memory:")

    def tearDown(self):
        self.db.close()

    def test_normal_text_search(self):

        birthday = self.db.add_thought(
            "Plan Mom's birthday"
        )

        self.db.add_thought(
            "Study for calculus"
        )

        results = self.db.search(
            "birthday"
        )

        ids = [
            row[0]
            for row in results
        ]

        self.assertEqual(
            ids,
            [birthday]
        )

    def test_tag_search(self):

        birthday = self.db.add_thought(
            "Plan Mom's birthday"
        )

        other = self.db.add_thought(
            "Study for calculus"
        )

        self.db.assign_tag(
            birthday,
            "birthday"
        )

        self.db.assign_tag(
            other,
            "school"
        )

        results = self.db.search_tag(
            "birthday"
        )

        ids = [
            row[0]
            for row in results
        ]

        self.assertIn(
            birthday,
            ids
        )

        self.assertNotIn(
            other,
            ids
        )

    def test_tag_search_with_multiple_matching_tags(self):

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

        ids = [
            row[0]
            for row in results
        ]

        self.assertEqual(
            ids.count(thought_id),
            1
        )

    def test_tag_search_does_not_return_untagged_thoughts(self):

        tagged = self.db.add_thought(
            "Birthday planning"
        )

        untagged = self.db.add_thought(
            "Birthday cake"
        )

        self.db.assign_tag(
            tagged,
            "birthday"
        )

        results = self.db.search_tag(
            "birthday"
        )

        ids = [
            row[0]
            for row in results
        ]

        self.assertIn(
            tagged,
            ids
        )

        self.assertNotIn(
            untagged,
            ids
        )

    def test_favorite_search(self):

        favorite = self.db.add_thought(
            "Important thought"
        )

        normal = self.db.add_thought(
            "Normal thought"
        )

        self.db.toggle_favorite(
            favorite
        )

        results = self.db.search(
            "",
            favorites_only=True
        )

        ids = [
            row[0]
            for row in results
        ]

        self.assertIn(
            favorite,
            ids
        )

        self.assertNotIn(
            normal,
            ids
        )

    def test_combined_text_and_favorite_search(self):

        matching_favorite = self.db.add_thought(
            "Important birthday"
        )

        matching_normal = self.db.add_thought(
            "Important birthday"
        )

        unrelated_favorite = self.db.add_thought(
            "Important school event"
        )

        self.db.toggle_favorite(
            matching_favorite
        )

        self.db.toggle_favorite(
            unrelated_favorite
        )

        results = self.db.search(
            "birthday",
            favorites_only=True
        )

        ids = [
            row[0]
            for row in results
        ]

        self.assertEqual(
            ids,
            [matching_favorite]
        )


if __name__ == "__main__":
    unittest.main()