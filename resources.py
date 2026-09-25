"""Academic resource data for the Telegram bot.

This is the only module where club members should add or update URLs.
Keep the navigation logic in bot.py free of resource links.
"""

from __future__ import annotations

from typing import Final, TypedDict


class Resource(TypedDict):
    title: str
    url: str
    description: str


CategoryMap = dict[str, list[Resource]]


def resource(title: str, url: str, description: str) -> Resource:
    return {"title": title, "url": url, "description": description}


CATEGORY_LABELS: Final[dict[str, str]] = {
    "drives": "Internal Drives",
    "external": "External Drives",
    "apps": "Software & Tools",
    "youtube": "YouTube Playlists",
}

SPECIALTY_LABELS: Final[dict[str, str]] = {
    "IRIIA": "IRIIA — Intelligent Systems",
    "uE": "µE — Microelectronics",
    "ENER": "ENER — Renewable Energies (ENR)",
    "GH": "GH — Green Hydrogen",
    "GE": "GE — Electrical Engineering",
}


def _internal_drives() -> list[Resource]:
    return [
        resource(
            "Drive Promo 2024/2025",
            "",
            "Add the shared Google Drive folder for the 2024/2025 promotion.",
        ),
        resource(
            "Drive Promo 2023/2024",
            "",
            "Add the shared Google Drive folder for the 2023/2024 promotion.",
        ),
        resource(
            "Drive Promo 2022/2023",
            "",
            "Add the shared Google Drive folder for the 2022/2023 promotion.",
        ),
        resource(
            "Drive Promo 2021/2022",
            "",
            "Add the shared Google Drive folder for the 2021/2022 promotion.",
        ),
        resource(
            "Exam archives",
            "",
            "Add the shared Google Drive folder for archived exams.",
        ),
    ]


def _second_year_prepa_drives() -> list[Resource]:
    return [
        resource(
            "2025/2026",
            "https://drive.google.com/drive/folders/1ToQnuvoAWAfd_bEo1DLt3cROBIVCpByh",
            "Internal Drive for 2nd Year Prepa, 2025/2026.",
        ),
        resource(
            "2025/2024",
            "https://drive.google.com/drive/folders/1B8SLw57KT80xQ8C3QQqin2vXB1T0QUxR",
            "Internal Drive for 2nd Year Prepa, 2025/2024.",
        ),
        resource(
            "2024/2023",
            "https://drive.google.com/drive/folders/1-R-y0KMxJbLyflWd2-2f_TAOj7UPiVPK",
            "Internal Drive for 2nd Year Prepa, 2024/2023.",
        ),
        resource(
            "2022/2023",
            "https://drive.google.com/drive/folders/1DJueVupxrf52OrKIM8_ABnf_h4J3Qz4E",
            "Internal Drive for 2nd Year Prepa, 2022/2023.",
        ),
        resource(
            "Exam archives",
            "",
            "Add the shared Google Drive folder for archived 2nd Year Prepa exams.",
        ),
    ]


def _third_year_enr_drives() -> list[Resource]:
    return [
        resource(
            "2022/2021 — 3rd year ENR",
            "https://drive.google.com/drive/folders/1LQNtlCJ1Khw6Z4tDkfsxaeEQkLGW0WG9",
            "Internal Drive for 3rd Year Renewable Energies, 2022/2021.",
        ),
        resource(
            "2023/2024 — 3rd year ENR",
            "https://drive.google.com/drive/folders/1t9xszm0ORlveTo7jj0SOVQZMpoxo2wOA?usp=drive_link",
            "Internal Drive for 3rd Year Renewable Energies, 2023/2024.",
        ),
        resource(
            "2026/2025 — 3rd year ENR",
            "https://t.me/third_year_renewable_energies",
            "Telegram resource channel for 3rd Year Renewable Energies, 2026/2025.",
        ),
    ]


def _third_year_IRIIA_drives() -> list[Resource]:
    return [
        resource(
            "2025/2024 — 3rd year IRIIA",
            "https://drive.google.com/drive/folders/1gK46myB5nJSGeUuYXUszM5eU25JudwgI?usp=drive_link",
            "Internal Drive for 3rd Year IRIIA, 2025/2024.",
        ),
        resource(
            "2026/2025 — 3rd year IRIIA",
            "https://drive.google.com/drive/folders/1b2hM-zY42b64FBk1ubHxU8kbN_QO2O9A?usp=sharing",
            "Internal Drive for 3rd Year IRIIA, 2026/2025.",
        ),
    ]


def _first_year_ST_drives() -> list[Resource]:
    return [
        resource(
            "2027/2026 — 1st year ST",
            "https://t.me/+9nAvFiCXiR9lMTg0",
            "Telegram Group for 1st year students, 2027/2026.",
        ),
        resource(
            "2026/2025 — 1st year ST",
            "https://t.me/doesntworkanyway",
            "Telegram Group for 1st year students, 2026/2025.",
        ),
    ]


def _external_drives() -> list[Resource]:
    return [
        resource("Polytech resources", "", "Add the Polytech resource folder."),
        resource("USTHB resources", "", "Add the USTHB resource folder."),
        resource("ESI resources", "", "Add the ESI resource folder."),
        resource(
            "National contest preparation",
            "",
            "Add the folder for national contest preparation.",
        ),
    ]


def _software_tools() -> list[Resource]:
    return [
        resource(
            "VS Code",
            "https://code.visualstudio.com/download",
            "Official download page. Add installation notes to the description if needed.",
        ),
        resource(
            "MATLAB",
            "https://getintopc.com/softwares/development/matlab-r2018b-free-download-6021288/",
            "Official MATLAB product page and download entry point.",
        ),
        resource(
            "Intel Quartus Prime",
            "https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/overview.html",
            "Official FPGA design software page.",
        ),
        resource(
            "PVsyst",
            "https://getintopc.com/softwares/simulation/pvsyst-2024-free-download/",
            "Official photovoltaic system design software page.",
        ),
        resource(
            "QGIS",
            "https://qgis.org/download/",
            "Official download page for the open-source GIS application.",
        ),
    ]


def _youtube_playlists() -> list[Resource]:
    return [
        resource(
            "Club-curated courses",
            "",
            "Add the club's curated playlist URL.",
        ),
        resource(
            "Tutorials and exam review",
            "",
            "Add the playlist URL for tutorials and exam review.",
        ),
    ]


def _categories(internal_drives: list[Resource] | None = None) -> CategoryMap:
    return {
        "drives": internal_drives if internal_drives is not None else _internal_drives(),
        "external": _external_drives(),
        "apps": _software_tools(),
        "youtube": _youtube_playlists(),
    }


def _specialty_categories(
    specialty: str, internal_drives: list[Resource] | None = None
) -> CategoryMap:
    categories = _categories(internal_drives)
    categories["youtube"] = [
        resource(
            f"{specialty} course playlist",
            "",
            f"Add the curated {specialty} playlist URL.",
        ),
        *categories["youtube"],
    ]
    return categories


# The structure mirrors the academic rules in the project brief:
# MI is newly opened, so only Year 1 is active.
# ST Years 1–2 go directly to resources; Years 3–5 go through specialties.
ACADEMIC_DATA: Final[dict[str, dict[str, object]]] = {
    "MI": {
        "label": "MI — Mathematics & Informatics",
        "active_years": [1],
        "years": {
            1: {"label": "Year 1", "categories": _categories()},
        },
    },
    "ST": {
        "label": "ST — Science & Technology",
        "active_years": [1, 2, 3, 4, 5],
        "years": {
            1: {"label": "Year 1", "categories": _categories(_first_year_ST_drives())},
            2: {
                "label": "Year 2 — Prepa",
                "categories": _categories(_second_year_prepa_drives()),
            },
            3: {
                "label": "Year 3 — Engineering Cycle",
                "specialties": {
                    key: {
                        "label": label,
                        "categories": _specialty_categories(
                            key,
                            {
                                "ENER": _third_year_enr_drives(),
                                "IRIIA": _third_year_IRIIA_drives(),
                            }.get(key),
                        ),
                    }
                    for key, label in SPECIALTY_LABELS.items()
                },
            },
            4: {
                "label": "Year 4 — Engineering Cycle",
                "specialties": {
                    key: {
                        "label": label,
                        "categories": _specialty_categories(key),
                    }
                    for key, label in SPECIALTY_LABELS.items()
                },
            },
            5: {
                "label": "Year 5 — Engineering Cycle",
                "specialties": {
                    key: {
                        "label": label,
                        "categories": _specialty_categories(key),
                    }
                    for key, label in SPECIALTY_LABELS.items()
                },
            },
        },
    },
}