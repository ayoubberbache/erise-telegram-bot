"""Fast standard-library checks for the academic data and callback contract."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

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
        self.assertEqual(
            [item["title"] for item in drives[:4]],
            ["2025/2026", "2025/2024", "2024/2023", "2022/2023"],
        )
        self.assertTrue(all(item["url"] for item in drives[:4]))

    def test_third_year_enr_uses_the_supplied_resources(self) -> None:
        specialty = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["ENER"]
        self.assertEqual(specialty["label"], "ENER — Renewable Energies (ENR)")
        drives = specialty["categories"]["drives"]
        self.assertEqual(len(drives), 3)
        self.assertTrue(all(item["url"] for item in drives))


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
        ]
        for callback in examples:
            self.assertLess(len(callback.encode("utf-8")), 64)


if __name__ == "__main__":
    unittest.main()