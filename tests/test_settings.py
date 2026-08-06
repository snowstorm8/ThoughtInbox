import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import settings as settings_module


class TestSettings(unittest.TestCase):

    def setUp(self):

        self.temp_dir = TemporaryDirectory()

        self.original_path = settings_module.SETTINGS_FILE

        settings_module.SETTINGS_FILE = (
            Path(self.temp_dir.name)
            / "settings.json"
        )

    def tearDown(self):

        settings_module.SETTINGS_FILE = (
            self.original_path
        )

        self.temp_dir.cleanup()

    def test_defaults_are_loaded(self):

        settings = settings_module.Settings()

        self.assertEqual(
            settings.get("theme"),
            "System"
        )

        self.assertEqual(
            settings.get("window_width"),
            900
        )

        self.assertEqual(
            settings.get("window_height"),
            700
        )

        self.assertTrue(
            settings.get("autosave")
        )

    def test_set_and_get(self):

        settings = settings_module.Settings()

        settings.set(
            "theme",
            "Dark"
        )

        self.assertEqual(
            settings.get("theme"),
            "Dark"
        )

    def test_settings_persist(self):

        settings = settings_module.Settings()

        settings.set(
            "autosave_delay",
            2500
        )

        new_settings = settings_module.Settings()

        self.assertEqual(
            new_settings.get("autosave_delay"),
            2500
        )

    def test_missing_key_uses_default(self):

        settings = settings_module.Settings()

        self.assertEqual(
            settings.get("theme"),
            "System"
        )

    def test_settings_file_is_created(self):

        Settings = settings_module.Settings

        Settings()

        self.assertTrue(
            settings_module.SETTINGS_FILE.exists()
        )
        
    def test_window_geometry_persists(self):
        settings = settings_module.Settings()

        settings.set(
            "window_width",
            1200
        )

        settings.set(
            "window_height",
            800
        )

        settings.set(
            "window_x",
            100
        )

        settings.set(
            "window_y",
            200
        )

        new_settings = settings_module.Settings()

        self.assertEqual(
            new_settings.get("window_width"),
            1200
        )

        self.assertEqual(
            new_settings.get("window_height"),
            800
        )

        self.assertEqual(
            new_settings.get("window_x"),
            100
        )

        self.assertEqual(
            new_settings.get("window_y"),
            200
        )


    def test_autosave_settings_persist(self):

        settings = settings_module.Settings()

        settings.set(
            "autosave",
            False
        )

        settings.set(
            "autosave_delay",
            2500
        )

        new_settings = settings_module.Settings()

        self.assertFalse(
            new_settings.get("autosave")
        )

        self.assertEqual(
            new_settings.get("autosave_delay"),
            2500
        )


    def test_theme_persists(self):

        settings = settings_module.Settings()

        settings.set(
            "theme",
            "Dark"
        )

        new_settings = settings_module.Settings()

        self.assertEqual(
            new_settings.get("theme"),
            "Dark"
        )


if __name__ == "__main__":
    unittest.main()