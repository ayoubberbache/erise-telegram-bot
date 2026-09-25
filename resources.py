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

YEAR_3_SPECIALTY_LABELS: Final[dict[str, str]] = {
    "IRIIA": "IRIIA — Intelligent Systems",
    "uE": "µE — Microelectronics",
    "ENER_GH": "ENER & GH — Renewable Energies & Green Hydrogen",
    "GE": "GE — Electrical Engineering",
}


class Year3Specialties(dict):
    """Specialties mapping for Year 3 ST where ENER and GH study together."""

    def __getitem__(self, key: str) -> dict[str, object]:
        if key in ("ENER", "GH") and not super().__contains__(key):
            return super().__getitem__("ENER_GH")
        return super().__getitem__(key)

    def __contains__(self, key: object) -> bool:
        if key in ("ENER", "GH"):
            return super().__contains__("ENER_GH")
        return super().__contains__(key)

    def get(self, key: str, default: object = None) -> object:
        if key in ("ENER", "GH") and not super().__contains__(key):
            return super().get("ENER_GH", default)
        return super().get(key, default)


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


def _first_year_st_drives() -> list[Resource]:
    return [
        resource(
            "Group Promo 2026/2027",
            "https://t.me/+9nAvFiCXiR9lMTg0",
            "Telegram group for 1st Year ST students, 2026/2027.",
        ),
        resource(
            "Group Promo 2025/2026",
            "https://t.me/+RJmZC1MMmiNhMzJk",
            "Telegram topic with academic resources for 1st Year ST, 2025/2026.",
        ),
        resource(
            "Group Promo 2024/2025",
            "https://t.me/hns1year",
            "Telegram main resource channel for 1st Year ST, Promo 2024/2025.",
        ),
    ]


def _second_year_prepa_drives() -> list[Resource]:
    return [
        resource(
            "Drive Promo 2025/2026",
            "https://drive.google.com/drive/folders/1ToQnuvoAWAfd_bEo1DLt3cROBIVCpByh",
            "Internal Drive for 2nd Year Prepa, 2025/2026.",
        ),
        resource(
            "Drive Promo 2024/2025",
            "https://drive.google.com/drive/folders/1B8SLw57KT80xQ8C3QQqin2vXB1T0QUxR",
            "Internal Drive for 2nd Year Prepa, 2024/2025.",
        ),
        resource(
            "Group Promo 2024/2025",
            "https://t.me/c/2210715774/13149",
            "Telegram main resource channel for 2nd Year Prepa, Promo 2024/2025.",
        ),
        resource(
            "Drive Promo 2023/2024 ver 1",
            "https://drive.google.com/drive/folders/1-R-y0KMxJbLyflWd2-2f_TAOj7UPiVPK",
            "Internal Drive (Version 1) for 2nd Year Prepa, 2023/2024.",
        ),
        resource(
            "Drive Promo 2023/2024 ver 2",
            "https://drive.google.com/drive/folders/1Q22KdlSS6B9TzIi0RrozBeAQtobBpvFx?usp=drive_link",
            "Internal Drive (Version 2) for 2nd Year Prepa, 2023/2024.",
        ),
        resource(
            "Group Promo 2023/2024",
            "https://t.me/doesntworkanyway/11",
            "Telegram group discussion for 2nd Year Prepa, Promo 2023/2024.",
        ),
        resource(
            "Drive Promo 2022/2023",
            "https://drive.google.com/drive/folders/1DJueVupxrf52OrKIM8_ABnf_h4J3Qz4E",
            "Internal Drive for 2nd Year Prepa, 2022/2023.",
        ),
        resource(
            "Group Summaries — 2nd Prepa",
            "https://t.me/summeries_2nd_prepa",
            "Curated course summaries and revision materials for 2nd Year Prepa.",
        ),
    ]


def _gh_channel_resource() -> Resource:
    return resource(
        "Channel RE2SD — Green Hydrogen",
        "https://t.me/RE2SD",
        "Telegram academic resource channel for Green Hydrogen students.",
    )


def _third_year_enr_drives() -> list[Resource]:
    return [
        resource(
            "Drive Promo 2021/2022 — 3rd Year ENR",
            "https://drive.google.com/drive/folders/1LQNtlCJ1Khw6Z4tDkfsxaeEQkLGW0WG9",
            "Internal Drive for 3rd Year Renewable Energies, 2021/2022.",
        ),
        resource(
            "Drive Promo 2023/2024 — 3rd Year ENR",
            "https://drive.google.com/drive/folders/1t9xszm0ORlveTo7jj0SOVQZMpoxo2wOA?usp=drive_link",
            "Internal Drive for 3rd Year Renewable Energies, 2023/2024.",
        ),
        resource(
            "Group Promo 2025/2026 — 3rd Year ENR & GH",
            "https://t.me/third_year_renewable_energies",
            "Telegram resource channel for 3rd Year Renewable Energies & Green Hydrogen, 2025/2026.",
        ),
        _gh_channel_resource(),
    ]


def _third_year_IRIIA_drives() -> list[Resource]:
    return [
        resource(
            "Drive Promo 2025/2026 — 3rd Year IRIIA",
            "https://drive.google.com/drive/folders/1b2hM-zY42b64FBk1ubHxU8kbN_QO2O9A?usp=sharing",
            "Internal Drive for 3rd Year IRIIA, Promo 2025/2026.",
        ),
        resource(
            "Drive Promo 2024/2025 — 3rd Year IRIIA",
            "https://drive.google.com/drive/folders/1gK46myB5nJSGeUuYXUszM5eU25JudwgI?usp=drive_link",
            "Internal Drive for 3rd Year IRIIA, Promo 2024/2025.",
        ),
        resource(
            "Drive Promo 2022/2023 — 3rd Year IRIIA",
            "https://drive.google.com/drive/folders/1JICAObH9oNE2fkOq0_n5rPTkf_pIm6HO",
            "Internal Drive for 3rd Year IRIIA, Promo 2022/2023.",
        ),
    ]


def _fourth_year_IRIIA_drives() -> list[Resource]:
    return [
        resource(
            "Drive Promo 2025/2026 — 4th Year IRIIA",
            "https://drive.google.com/drive/folders/1CFjLVg5w1NV8mrUP6n_983rL8vuYPTjj?usp=sharing",
            "Internal Drive for 4th Year IRIIA, Promo 2025/2026.",
        ),
        resource(
            "Drive Promo 2023/2024 — 4th Year IRIIA",
            "https://drive.google.com/drive/folders/1_tPjRFBIkS7cPBVcsYt-dbW8dsJyQ0-F?usp=sharing",
            "Internal Drive for 4th Year IRIIA, Promo 2023/2024.",
        ),
    ]


def _third_year_GE_drives() -> list[Resource]:
    return [
        resource(
            "Drive 1st Promo — 3rd & 4th Year GE",
            "https://drive.google.com/drive/folders/1eWj9VE5y1uv9-t-sKmKzVvJwBjfS4woE",
            "Shared Google Drive folder for 1st Promo (3rd & 4th Year Electrical Engineering).",
        ),
        resource(
            "Group 3rd Promo — 3rd Year GE",
            "https://t.me/electricalenghns",
            "Telegram resource channel/group for 3rd Promo (3rd Year Electrical Engineering).",
        ),
    ]


def _fourth_year_GE_drives() -> list[Resource]:
    return [
        resource(
            "Drive 2nd Promo — 4th Year GE",
            "https://drive.google.com/drive/folders/1CjyzxvOEp5K-EDDEe6Rh-MpPz5TcCPrJ",
            "Internal Drive for 2nd Promo (4th Year Electrical Engineering).",
        ),
        resource(
            "Drive 1st Promo — 3rd & 4th Year GE",
            "https://drive.google.com/drive/folders/1eWj9VE5y1uv9-t-sKmKzVvJwBjfS4woE",
            "Shared Google Drive folder for 1st Promo (3rd & 4th Year Electrical Engineering).",
        ),
    ]


def _second_year_prepa_external() -> list[Resource]:
    return [
        resource(
            "National Contest Preparation (Concours ST)",
            "https://t.me/concour_st",
            "Telegram channel for national engineering concours preparation.",
        ),
        resource(
            "External Resources — 2nd Prepa",
            "https://t.me/hns2year/21932",
            "Curated external resources and modules for 2nd Year Prepa.",
        ),
        resource("Polytech resources", "", "Add the Polytech resource folder."),
        resource("USTHB resources", "", "Add the USTHB resource folder."),
        resource("ESI resources", "", "Add the ESI resource folder."),
    ]


def _overleaf_resource() -> Resource:
    return resource(
        "Overleaf (LaTeX)",
        "https://www.overleaf.com/",
        "Collaborative cloud LaTeX editor for scientific papers, thesis, and reports.",
    )


def _matlab_resource() -> Resource:
    return resource(
        "MATLAB",
        "https://getintopc.com/softwares/development/matlab-r2018b-free-download-6021288/",
        "MATLAB software package download and installation entry point.",
    )


def _third_year_IRIIA_apps() -> list[Resource]:
    return [
        resource(
            "VS Code",
            "https://code.visualstudio.com/download",
            "Official Visual Studio Code editor download.",
        ),
        resource(
            "VirtualBox",
            "https://getintopc.com/softwares/virtualization/virtualbox-free-download/",
            "Oracle VM VirtualBox installer from Get Into PC.",
        ),
        resource(
            "Ubuntu Desktop",
            "https://ubuntu.com/download/desktop",
            "Official Ubuntu Linux desktop ISO download for VMs and dual-boot.",
        ),
        resource(
            "WSL Linux",
            "https://learn.microsoft.com/en-us/windows/wsl/install",
            "Microsoft official setup and install guide for Windows Subsystem for Linux.",
        ),
        resource(
            "PyCharm",
            "https://getintopc.com/softwares/development/jetbrains-pycharm-pro-2023-free-download/",
            "JetBrains PyCharm Professional IDE installer from Get Into PC.",
        ),
        resource(
            "Apache NetBeans",
            "https://getintopc.com/softwares/development/netbeans-ide-free-download/",
            "Apache NetBeans IDE installer from Get Into PC.",
        ),
        resource(
            "VUE (Mind Mapping)",
            "https://vue.tufts.edu/",
            "Tufts Visual Understanding Environment for concept mapping and mind maps.",
        ),
        _overleaf_resource(),
        _matlab_resource(),
        resource(
            "Oracle Database Free",
            "https://www.oracle.com/database/free/",
            "Official free full-featured Oracle Database (23c/XE) for developers and students.",
        ),
        resource(
            "Oracle SQL Developer",
            "https://www.oracle.com/database/sqldeveloper/",
            "Free official graphical interface tool for Oracle database development and queries.",
        ),
        resource(
            "Cisco Packet Tracer",
            "https://getintopc.com/softwares/network/cisco-packet-tracer-2024-free-download/",
            "Cisco Packet Tracer network simulation software installer from Get Into PC.",
        ),
        resource(
            "Huawei eNSP (Network Simulator)",
            "https://github.com/horserosemilkshake/huawei-ensp",
            "Free Enterprise Network Simulation Platform for Huawei networking and routing labs.",
        ),
    ]


def _first_year_software_tools() -> list[Resource]:
    return [
        resource(
            "Code::Blocks",
            "https://www.codeblocks.org/downloads/binaries/",
            "Free open-source C/C++ IDE official binaries for 1st Year programming.",
        ),
        resource(
            "SolidWorks",
            "https://getintopc.com/softwares/3d-cad/solidworks-premium-2020-free-download/",
            "SolidWorks 3D CAD modeling software installer from Get Into PC.",
        ),
        resource(
            "VS Code",
            "https://code.visualstudio.com/download",
            "Official download page. Code editor for all programming modules.",
        ),
        _matlab_resource(),
    ]


def _software_tools() -> list[Resource]:
    return [
        resource(
            "VS Code",
            "https://code.visualstudio.com/download",
            "Official download page. Code editor for all programming modules.",
        ),
        _matlab_resource(),
        resource(
            "PVsyst",
            "https://getintopc.com/softwares/simulation/pvsyst-2024-free-download/",
            "Photovoltaic system design software installer from Get Into PC.",
        ),
        resource(
            "QGIS",
            "https://getintopc.com/softwares/development/qgis-free-download/",
            "GIS spatial data application installer from Get Into PC.",
        ),
    ]


def _third_year_ener_gh_apps() -> list[Resource]:
    return [
        _overleaf_resource(),
        _matlab_resource(),
        resource(
            "VS Code",
            "https://code.visualstudio.com/download",
            "Official code editor for development.",
        ),
        resource(
            "PVsyst",
            "https://getintopc.com/softwares/simulation/pvsyst-2024-free-download/",
            "Photovoltaic system design software installer from Get Into PC.",
        ),
        resource(
            "Modelica (OpenModelica)",
            "https://openmodelica.org/download/download-windows/",
            "Free open-source Modelica modeling and simulation environment for energy systems.",
        ),
        resource(
            "ANSYS Products",
            "https://getintopc.com/softwares/simulation/ansys-products-2024-free-download/",
            "Engineering simulation suite (CFD, FEA, thermal) installer from Get Into PC.",
        ),
        resource(
            "HOMER Pro",
            "https://getintopc.com/softwares/electrical-engineering/homer-pro-free-download/",
            "Microgrid and hybrid renewable/hydrogen systems optimization installer from Get Into PC.",
        ),
        resource(
            "COMSOL Multiphysics",
            "https://getintopc.com/softwares/simulation/comsol-multiphysics-2024-free-download/",
            "Multiphysics simulation software for fuel cells and electrolysis from Get Into PC.",
        ),
    ]


def _software_tools_for_specialty(specialty: str, year: int) -> list[Resource]:
    if specialty == "IRIIA" and year == 3:
        return _third_year_IRIIA_apps()
    if (specialty in ("ENER", "ENER_GH", "GH") and year == 3) or specialty == "ENER_GH":
        return _third_year_ener_gh_apps()

    tools = [
        _overleaf_resource(),
        _matlab_resource(),
        resource(
            "VS Code",
            "https://code.visualstudio.com/download",
            "Official code editor for development.",
        ),
    ]
    if specialty == "ENER":
        tools.extend([
            resource(
                "PVsyst",
                "https://getintopc.com/softwares/simulation/pvsyst-2024-free-download/",
                "Photovoltaic system design software installer from Get Into PC.",
            ),
            resource(
                "HOMER Pro",
                "https://getintopc.com/softwares/electrical-engineering/homer-pro-free-download/",
                "Microgrid and hybrid renewable systems optimization installer from Get Into PC.",
            ),
        ])
    elif specialty == "GH":
        tools.extend([
            resource(
                "Modelica (OpenModelica)",
                "https://openmodelica.org/download/download-windows/",
                "Free open-source Modelica modeling and simulation environment for energy systems.",
            ),
            resource(
                "ANSYS Products",
                "https://getintopc.com/softwares/simulation/ansys-products-2024-free-download/",
                "Engineering simulation suite (CFD, FEA, thermal) installer from Get Into PC.",
            ),
            resource(
                "HOMER Pro",
                "https://getintopc.com/softwares/electrical-engineering/homer-pro-free-download/",
                "Microgrid and hybrid renewable/hydrogen systems optimization installer from Get Into PC.",
            ),
            resource(
                "COMSOL Multiphysics",
                "https://getintopc.com/softwares/simulation/comsol-multiphysics-2024-free-download/",
                "Multiphysics simulation software for fuel cells and electrolysis from Get Into PC.",
            ),
        ])
    return tools


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


def _categories(
    internal_drives: list[Resource] | None = None,
    software_tools: list[Resource] | None = None,
    external_drives: list[Resource] | None = None,
) -> CategoryMap:
    return {
        "drives": internal_drives if internal_drives is not None else _internal_drives(),
        "external": external_drives if external_drives is not None else [],
        "apps": software_tools if software_tools is not None else _software_tools(),
        "youtube": _youtube_playlists(),
    }


def _specialty_categories(
    specialty: str,
    year: int = 3,
    internal_drives: list[Resource] | None = None,
    external_drives: list[Resource] | None = None,
) -> CategoryMap:
    categories = _categories(
        internal_drives=internal_drives,
        software_tools=_software_tools_for_specialty(specialty, year),
        external_drives=external_drives,
    )
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
            1: {
                "label": "Year 1",
                "categories": _categories(software_tools=_first_year_software_tools()),
            },
        },
    },
    "ST": {
        "label": "ST — Science & Technology",
        "active_years": [1, 2, 3, 4, 5],
        "years": {
            1: {
                "label": "Year 1",
                "categories": _categories(
                    internal_drives=_first_year_st_drives(),
                    software_tools=_first_year_software_tools(),
                ),
            },
            2: {
                "label": "Year 2 — Prepa",
                "categories": _categories(
                    internal_drives=_second_year_prepa_drives(),
                    external_drives=_second_year_prepa_external(),
                ),
            },
            3: {
                "label": "Year 3 — Engineering Cycle",
                "specialties": Year3Specialties(
                    {
                        key: {
                            "label": label,
                            "categories": _specialty_categories(
                                key,
                                year=3,
                                internal_drives={
                                    "ENER_GH": _third_year_enr_drives(),
                                    "IRIIA": _third_year_IRIIA_drives(),
                                    "GE": _third_year_GE_drives(),
                                }.get(key),
                            ),
                        }
                        for key, label in YEAR_3_SPECIALTY_LABELS.items()
                    }
                ),
            },
            4: {
                "label": "Year 4 — Engineering Cycle",
                "specialties": {
                    key: {
                        "label": label,
                        "categories": _specialty_categories(
                            key,
                            year=4,
                            internal_drives={
                                "GH": [_gh_channel_resource(), *_internal_drives()],
                                "IRIIA": _fourth_year_IRIIA_drives(),
                                "GE": _fourth_year_GE_drives(),
                            }.get(key),
                        ),
                    }
                    for key, label in SPECIALTY_LABELS.items()
                },
            },
            5: {
                "label": "Year 5 — Engineering Cycle",
                "specialties": {
                    key: {
                        "label": label,
                        "categories": _specialty_categories(
                            key,
                            year=5,
                            internal_drives={
                                "GH": [_gh_channel_resource(), *_internal_drives()],
                            }.get(key),
                        ),
                    }
                    for key, label in SPECIALTY_LABELS.items()
                },
            },
        },
    },
}