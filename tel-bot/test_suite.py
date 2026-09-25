"""Fast standard-library checks for the academic data and callback contract."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

try:
    from bot import (
        _branch_keyboard,
        _category_keyboard,
        _fast_panel_keyboard,
        _guide_text,
        _years_keyboard,
        get_empty_button_mode,
        set_empty_button_mode,
    )
    HAS_BOT_DEPENDENCIES = True
except ImportError:
    HAS_BOT_DEPENDENCIES = False

from resources_data import (
    ACADEMIC_DATA,
    CATEGORY_LABELS,
    SPECIALTY_LABELS,
    YEAR_3_SPECIALTY_LABELS,
)


class ResourceDataTests(unittest.TestCase):
    def test_mi_only_exposes_year_one(self) -> None:
        self.assertEqual(ACADEMIC_DATA["MI"]["active_years"], [1])
        self.assertEqual(list(ACADEMIC_DATA["MI"]["years"]), [1])

    def test_st_prepa_and_engineering_cycle_are_present(self) -> None:
        self.assertEqual(ACADEMIC_DATA["ST"]["active_years"], [1, 2, 3, 4, 5])
        for year in (1, 2):
            self.assertIn("categories", ACADEMIC_DATA["ST"]["years"][year])
        self.assertEqual(
            set(ACADEMIC_DATA["ST"]["years"][3]["specialties"]),
            set(YEAR_3_SPECIALTY_LABELS),
        )
        for year in (4, 5):
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

    def test_third_year_ener_gh_uses_the_supplied_resources(self) -> None:
        specialty = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["ENER_GH"]
        self.assertEqual(specialty["label"], "ENER & GH — Renewable Energies & Green Hydrogen")
        drives = specialty["categories"]["drives"]
        self.assertEqual(len(drives), 4)
        self.assertTrue(all(item["url"] for item in drives))
        # ENER and GH aliases in year 3 resolve to ENER_GH
        self.assertEqual(ACADEMIC_DATA["ST"]["years"][3]["specialties"]["ENER"], specialty)
        self.assertEqual(ACADEMIC_DATA["ST"]["years"][3]["specialties"]["GH"], specialty)

        # Software tools for 3rd year ENER & GH
        apps = specialty["categories"]["apps"]
        titles = [item["title"] for item in apps]
        for expected in (
            "SolidWorks",
            "PVsyst",
            "Meteonorm",
            "Global Wind Atlas",
            "RETScreen Expert",
            "Overleaf (LaTeX)",
            "MATLAB",
            "VS Code",
        ):
            self.assertIn(expected, titles)
        # Advanced hydrogen apps are assigned to 5th year GH
        for moved in (
            "Modelica (OpenModelica)",
            "ANSYS Products",
            "HOMER Pro",
            "COMSOL Multiphysics",
        ):
            self.assertNotIn(moved, titles)
        self.assertTrue(all(item["url"] for item in apps))

        # Check Get Into PC links for apps available there, and official site for Wind Atlas
        by_title = {item["title"]: item["url"] for item in apps}
        self.assertIn("getintopc.com", by_title["SolidWorks"])
        self.assertIn("getintopc.com", by_title["Meteonorm"])
        self.assertIn("getintopc.com", by_title["RETScreen Expert"])
        self.assertIn("globalwindatlas.info", by_title["Global Wind Atlas"])

    def test_fifth_year_gh_apps_contain_advanced_hydrogen_tools(self) -> None:
        y5_gh_apps = ACADEMIC_DATA["ST"]["years"][5]["specialties"]["GH"]["categories"]["apps"]
        titles = [item["title"] for item in y5_gh_apps]
        expected = [
            "Modelica (OpenModelica)",
            "ANSYS Products",
            "HOMER Pro",
            "COMSOL Multiphysics",
            "SolidWorks",
            "RETScreen Expert",
            "Overleaf (LaTeX)",
            "MATLAB",
            "VS Code",
        ]
        for name in expected:
            self.assertIn(name, titles)
        self.assertTrue(all(item["url"] for item in y5_gh_apps))

    def test_first_year_st_uses_the_supplied_resources(self) -> None:
        drives = ACADEMIC_DATA["ST"]["years"][1]["categories"]["drives"]
        self.assertEqual(len(drives), 3)
        self.assertTrue(all(item["url"] for item in drives))

    def test_third_year_iriia_uses_the_supplied_resources(self) -> None:
        specialty = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["IRIIA"]
        self.assertEqual(specialty["label"], "IRIIA — Intelligent Systems")
        drives = specialty["categories"]["drives"]
        self.assertEqual(len(drives), 3)
        self.assertTrue(all(item["url"] for item in drives))
        titles = [item["title"] for item in drives]
        self.assertIn("Drive Promo 2022/2023 — 3rd Year IRIIA", titles)

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
            "Oracle Database Free",
            "Oracle SQL Developer",
            "Cisco Packet Tracer",
            "Huawei eNSP (Network Simulator)",
        ]
        for name in expected:
            self.assertIn(name, titles)
        self.assertTrue(all(item["url"] for item in apps))

    def test_overleaf_in_every_engineering_specialty_years_3_4_5(self) -> None:
        for year in (3, 4, 5):
            for specialty_key in ACADEMIC_DATA["ST"]["years"][year]["specialties"]:
                apps = ACADEMIC_DATA["ST"]["years"][year]["specialties"][specialty_key]["categories"]["apps"]
                titles = [item["title"] for item in apps]
                self.assertIn("Overleaf (LaTeX)", titles)
                overleaf = next(item for item in apps if item["title"] == "Overleaf (LaTeX)")
                self.assertEqual(overleaf["url"], "https://www.overleaf.com/")

    def test_external_drives_only_available_for_assigned_year_and_specialty(self) -> None:
        # Year 2 Prepa has external drives assigned
        st_y2_external = ACADEMIC_DATA["ST"]["years"][2]["categories"]["external"]
        self.assertGreater(len(st_y2_external), 0)
        self.assertTrue(any(bool(item["url"]) for item in st_y2_external))

        # Year 1 ST does not have external drives assigned
        st_y1_external = ACADEMIC_DATA["ST"]["years"][1]["categories"]["external"]
        self.assertEqual(len(st_y1_external), 0)

        # Year 3 IRIIA does not have external drives assigned
        iriia_external = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["IRIIA"]["categories"]["external"]
        self.assertEqual(len(iriia_external), 0)

    def test_intel_quartus_prime_removed_everywhere(self) -> None:
        for branch_name, branch_data in ACADEMIC_DATA.items():
            for year, year_data in branch_data["years"].items():
                if "categories" in year_data:
                    apps = year_data["categories"].get("apps", [])
                    titles = [item["title"] for item in apps]
                    self.assertNotIn("Intel Quartus Prime", titles)
                elif "specialties" in year_data:
                    for spec_name, spec_data in year_data["specialties"].items():
                        apps = spec_data["categories"].get("apps", [])
                        titles = [item["title"] for item in apps]
                        self.assertNotIn("Intel Quartus Prime", titles)

    def test_first_year_software_tools_include_codeblocks_and_solidworks(self) -> None:
        for branch in ("ST", "MI"):
            apps = ACADEMIC_DATA[branch]["years"][1]["categories"]["apps"]
            titles = [item["title"] for item in apps]
            self.assertIn("Code::Blocks", titles)
            self.assertIn("SolidWorks", titles)
            solidworks = next(item for item in apps if item["title"] == "SolidWorks")
            self.assertIn("getintopc.com", solidworks["url"])
            codeblocks = next(item for item in apps if item["title"] == "Code::Blocks")
            self.assertIn("codeblocks.org", codeblocks["url"])

    def test_get_into_pc_links_applied(self) -> None:
        iriia_apps = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["IRIIA"]["categories"]["apps"]
        by_title = {item["title"]: item["url"] for item in iriia_apps}
        self.assertIn("getintopc.com", by_title["PyCharm"])
        self.assertIn("getintopc.com", by_title["VirtualBox"])
        self.assertIn("getintopc.com", by_title["Apache NetBeans"])
        self.assertIn("getintopc.com", by_title["Cisco Packet Tracer"])
        self.assertIn("getintopc.com", by_title["MATLAB"])

    def test_re2sd_channel_in_all_three_years_of_gh(self) -> None:
        # Year 3 (ENER_GH / GH)
        y3_gh = ACADEMIC_DATA["ST"]["years"][3]["specialties"]["GH"]
        y3_drives = y3_gh["categories"]["drives"]
        self.assertTrue(any(item["url"] == "https://t.me/RE2SD" for item in y3_drives))

        # Year 4 GH
        y4_gh = ACADEMIC_DATA["ST"]["years"][4]["specialties"]["GH"]
        y4_drives = y4_gh["categories"]["drives"]
        self.assertTrue(any(item["url"] == "https://t.me/RE2SD" for item in y4_drives))

        # Year 5 GH
        y5_gh = ACADEMIC_DATA["ST"]["years"][5]["specialties"]["GH"]
        y5_drives = y5_gh["categories"]["drives"]
        self.assertTrue(any(item["url"] == "https://t.me/RE2SD" for item in y5_drives))


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

    @unittest.skipUnless(HAS_BOT_DEPENDENCIES, "Requires bot dependencies (python-telegram-bot, dotenv)")
    def test_mi_branch_hides_inactive_years_in_keyboard(self) -> None:
        kb = _years_keyboard("MI")
        button_texts = [b.text for row in kb.inline_keyboard for b in row]
        self.assertEqual(button_texts, ["Year 1", "Back"])

    @unittest.skipUnless(HAS_BOT_DEPENDENCIES, "Requires bot dependencies (python-telegram-bot, dotenv)")
    def test_fast_panel_and_guide_keyboard_and_text(self) -> None:
        guide = _guide_text()
        self.assertIn("ERISE", guide)
        self.assertIn("MI", guide)
        self.assertIn("ST", guide)
        self.assertIn("ENER & GH", guide)
        self.assertIn("Internal Drives", guide)
        self.assertIn("Software & Tools", guide)

        panel = _fast_panel_keyboard()
        button_texts = [b.text for row in panel.inline_keyboard for b in row]
        self.assertIn("⚡ 1st Year ST", button_texts)
        self.assertIn("⚡ 1st Year MI", button_texts)
        self.assertIn("⚡ 2nd Year Prepa", button_texts)
        self.assertIn("⚡ 3rd Year ENER & GH", button_texts)
        self.assertIn("⚡ 3rd Year IRIIA", button_texts)
        self.assertIn("⚡ 3rd Year GE", button_texts)
        self.assertIn("🚀 Main Menu (All Branches)", button_texts)

        branch_kb = _branch_keyboard()
        branch_texts = [b.text for row in branch_kb.inline_keyboard for b in row]
        self.assertIn("⚡ Fast Panel & Guide", branch_texts)


if __name__ == "__main__":
    unittest.main()