"""Fast standard-library checks for the academic data and callback contract."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

try:
    from bot import (
        _category_keyboard,
        get_empty_button_mode,
        set_empty_button_mode,
    )
    HAS_BOT_DEPENDENCIES = True
except ImportError:
    HAS_BOT_DEPENDENCIES = False

from resources_data import ACADEMIC_DATA, CATEGORY_LABELS, SPECIALTY_LABELS


class ResourceDataTests(unittest.TestCase):
    def test_mi_only_exposes_year_one(self) -> None:
        self.assertEqual(ACADEMIC_DATA["MI"]["active_years"], [1])
        self.assertEqual(list(ACADEMIC_DATA["MI"]["years"]), [1])

    def test_st_prepa_and_engineering_cycle_are_present(self) -> None:
        self.assertEqual(ACADEMIC_DATA["ST"]["active_years"], [1, 2, 3, 4, 5])
        for year in (1, 2):
            self.assertIn("categories", ACADEMIC_DATA["ST"]["years"][year])
        for year in (3, 4, 5):
            self.assertEqual(
                set(ACADEMIC_DATA["ST"]["years"][year]["specialties"]),
                set(SPECIALTY_LABELS),
            )

    def test_every_active_level_has_four_categories(self) -> None:
        for branch_data in ACADEMIC_DATA.values():
            for year_data in branch_data["years"].values():
                if "categories" in year_data:
                    self.assertEqual(set(year_data["categories"]), set(CATEGORY_LABELS))
                else:
                    for specialty in year_data["specialties"].values():
                        self.assertEqual(set(specialty["categories"]), set(CATEGORY_LABELS))

    def test_second_year_prepa_uses_the_supplied_drive_folders(self) -> None:
        drives = ACADEMIC_DATA["ST"]["years"][2]["categories"]["drives"]
        self.assertGreaterEqual(len(drives), 7)
        self.assertTrue(all(item["url"] for item in drives))
        titles = [item["title"] for item in drives]
        self.assertIn("Drive Promo 2025/2026", titles)
        self.assertIn("Drive Promo 2024/2025", titles)
        self.assertIn("Drive Promo 2023/2024 ver 1", titles)
        self.assertIn("Drive Promo 2023/2024 ver 2", titles)
        self.assertIn("Drive Promo 2022/2023", titles)

    def test_third_year_enr_uses_the_supplied_resources(self) -> None:
        specialty = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["ENER"]
        self.assertEqual(specialty["label"], "ENER — Renewable Energies (ENR)")
        drives = specialty["categories"]["drives"]
        self.assertEqual(len(drives), 3)
        self.assertTrue(all(item["url"] for item in drives))

    def test_first_year_st_uses_the_supplied_resources(self) -> None:
        drives = ACADEMIC_DATA["ST"]["years"][1]["categories"]["drives"]
        self.assertEqual(len(drives), 3)
        self.assertTrue(all(item["url"] for item in drives))

    def test_third_year_iriia_uses_the_supplied_resources(self) -> None:
        specialty = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["IRIIA"]
        self.assertEqual(specialty["label"], "IRIIA — Intelligent Systems")
        drives = specialty["categories"]["drives"]
        self.assertEqual(len(drives), 2)
        self.assertTrue(all(item["url"] for item in drives))

    def test_fourth_year_iriia_uses_the_supplied_resources(self) -> None:
        specialty = ACADEMIC_DATA["ST"]["years"][4]["specialties"]["IRIIA"]
        drives = specialty["categories"]["drives"]
        self.assertEqual(len(drives), 2)
        self.assertTrue(all(item["url"] for item in drives))

    def test_ge_specialty_uses_the_supplied_resources(self) -> None:
        drives_y3 = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["GE"]["categories"]["drives"]
        self.assertEqual(len(drives_y3), 2)
        self.assertTrue(all(item["url"] for item in drives_y3))

        drives_y4 = ACADEMIC_DATA["ST"]["years"][4]["specialties"]["GE"]["categories"]["drives"]
        self.assertEqual(len(drives_y4), 2)
        self.assertTrue(all(item["url"] for item in drives_y4))

    def test_third_year_iriia_apps_contain_all_requested_tools(self) -> None:
        apps = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["IRIIA"]["categories"]["apps"]
        titles = [item["title"] for item in apps]
        expected = [
            "VS Code",
            "VirtualBox",
            "Ubuntu Desktop",
            "WSL Linux",
            "PyCharm",
            "Apache NetBeans",
            "VUE (Mind Mapping)",
            "Overleaf (LaTeX)",
            "MATLAB",
        ]
        for name in expected:
            self.assertIn(name, titles)
        self.assertTrue(all(item["url"] for item in apps))

    def test_overleaf_in_every_engineering_specialty_years_3_4_5(self) -> None:
        for year in (3, 4, 5):
            for specialty_key in SPECIALTY_LABELS:
                apps = ACADEMIC_DATA["ST"]["years"][year]["specialties"][specialty_key]["categories"]["apps"]
                titles = [item["title"] for item in apps]
                self.assertIn("Overleaf (LaTeX)", titles)
                overleaf = next(item for item in apps if item["title"] == "Overleaf (LaTeX)")
                self.assertEqual(overleaf["url"], "https://www.overleaf.com/")


class NavigationContractTests(unittest.TestCase):
    def test_bot_does_not_contain_hardcoded_http_links(self) -> None:
        source = Path(__file__).with_name("bot.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        self.assertNotIn("http://", source)
        self.assertNotIn("https://", source)
        self.assertIsNotNone(tree)

    def test_callback_examples_stay_under_telegram_limit(self) -> None:
        examples = [
            "d:MI",
            "y:ST:5",
            "s:ST:3:IRIIA",
            "c:ST:3:IRIIA:apps",
            "n:ST:3:IRIIA:youtube:99",
            "e:youtube",
        ]
        for callback in examples:
            self.assertLess(len(callback.encode("utf-8")), 64)

    @unittest.skipUnless(HAS_BOT_DEPENDENCIES, "Requires bot dependencies (python-telegram-bot, dotenv)")
    def test_button_toggle_modes(self) -> None:
        orig = get_empty_button_mode()
        try:
            # In disappear mode, empty categories are omitted
            set_empty_button_mode("disappear")
            self.assertEqual(get_empty_button_mode(), "disappear")
            kb = _category_keyboard("ST", 3, "IRIIA")
            buttons = [b.text for row in kb.inline_keyboard for b in row]
            # YouTube is empty in IRIIA, so in disappear mode it should disappear
            self.assertNotIn("YouTube Playlists", buttons)
            self.assertNotIn("▫️ YouTube Playlists (Empty)", buttons)

            # In grey mode, empty categories appear with ▫️ indicator
            set_empty_button_mode("grey")
            self.assertEqual(get_empty_button_mode(), "grey")
            kb_grey = _category_keyboard("ST", 3, "IRIIA")
            buttons_grey = [b.text for row in kb_grey.inline_keyboard for b in row]
            self.assertIn("▫️ YouTube Playlists (Empty)", buttons_grey)
        finally:
            set_empty_button_mode(orig)


if __name__ == "__main__":
    unittest.main()