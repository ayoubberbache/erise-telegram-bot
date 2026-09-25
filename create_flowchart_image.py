"""
create_flowchart_image.py
-------------------------
Generates an ultra-high-resolution (300 DPI), professional infographic flowchart
for the HNS RE2SD Resources Telegram Bot (ERISE Scientific Club).

Accurate Academic Structure (HNS RE2SD Batna):
- MI Branch: Only 1st Year (Active) -> Direct to Resources.
  Years 2, 3, 4, 5 are greyed out (Not open yet, no specialties). Zero connection to ST.
- ST Branch:
  * Years 1 & 2 (Prepa) -> Direct to Resources.
  * Years 3, 4, 5 (Cycle Ingenieur) -> 5 ST Specialties (IRIIA, uE, ENER, GH, GE) -> Resources.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Set system font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']

def create_diagram():
    # 4K / poster quality: 24 x 18 inches at 300 DPI (7200 x 5400 px)
    fig = plt.figure(figsize=(24, 18), dpi=300, facecolor="#0B0F19")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#0B0F19")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Helper function to draw stylish cards
    def draw_card(x, y, w, h, bg_color, border_color, title, subtitle="", items=None, badge=None, 
                  title_color="#FFFFFF", title_size=12.5, radius=1.2, border_width=1.8, border_style="-"):
        box = FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle=f"round,pad=0.2,rounding_size={radius}",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=border_width,
            linestyle=border_style,
            zorder=2
        )
        ax.add_patch(box)
        
        # Badge tag
        if badge:
            badge_w = len(badge) * 0.70 + 1.2
            badge_box = FancyBboxPatch(
                (x - w/2 + 0.8, y + h/2 - 1.35), badge_w, 1.15,
                boxstyle="round,pad=0.1,rounding_size=0.35",
                facecolor=border_color,
                edgecolor="none",
                zorder=4
            )
            ax.add_patch(badge_box)
            ax.text(x - w/2 + 0.8 + badge_w/2, y + h/2 - 0.78, badge, ha="center", va="center", 
                    color="#0B0F19", fontsize=8, weight="bold", zorder=5)

        # Title
        if subtitle or (items and len(items) > 0):
            ty = y + h/2 - 1.75
        else:
            ty = y
        ax.text(x, ty, title, ha="center", va="center", color=title_color, fontsize=title_size, weight="bold", zorder=3)
        
        # Subtitle
        if subtitle:
            ax.text(x, ty - 1.5, subtitle, ha="center", va="center", color="#94A3B8", fontsize=title_size*0.75, style="italic", zorder=3)
            
        # Items list
        if items:
            start_y = ty - 2.7
            for i, it in enumerate(items):
                ax.text(x - w/2 + 1.1, start_y - (i * 1.45), it, ha="left", va="center", color="#E2E8F0", fontsize=title_size*0.70, zorder=3)

    # Helper function to draw directional arrows
    def draw_arrow(start, end, color="#38BDF8", width=2.4, style="->", rad=0.0, linestyle="-"):
        arrow = FancyArrowPatch(
            start, end,
            arrowstyle=style,
            connectionstyle=f"arc3,rad={rad}",
            color=color,
            linewidth=width,
            linestyle=linestyle,
            mutation_scale=18,
            zorder=1
        )
        ax.add_patch(arrow)

    # =========================================================================
    # 1. HEADER & BRANDING
    # =========================================================================
    draw_card(50, 94.5, 92, 7.5, "#111827", "#10B981", 
              "ERISE SCIENTIFIC CLUB  •  HNS RE2SD BATNA",
              "Academic Resources Telegram Bot Architecture & Verified Student Navigation Flow",
              title_color="#10B981", title_size=18, border_width=2.5)

    ax.text(50, 91.8, "École Nationale Supérieure des Énergies Renouvelables, Environnement & Développement Durable (Batna, Algérie)",
            ha="center", va="center", color="#6EE7B7", fontsize=11, weight="bold")

    # =========================================================================
    # 2. START & WELCOME
    # =========================================================================
    draw_card(50, 83.5, 30, 5.2, "#1E293B", "#38BDF8", "1. Student Types /start", "Greeting from ERISE Club Team", title_size=13)
    draw_arrow((50, 80.8), (50, 76.5), color="#38BDF8")

    # =========================================================================
    # 3. DEPARTMENT SELECTION (BRANCHING)
    # =========================================================================
    draw_card(50, 73.8, 36, 5.2, "#1F2937", "#F59E0B", "2. Choose Department / Branch", "Select Field of Study", title_color="#FBBF24", title_size=13)
    
    # Left Branch: MI (Center = 24)
    draw_arrow((40, 71.2), (24, 66.0), color="#06B6D4", rad=-0.06)
    draw_card(24, 63.2, 34, 5.4, "#164E63", "#06B6D4", "Filiere MI", "Mathematiques & Informatique", badge="BRANCH A", title_color="#67E8F9", title_size=13)

    # Right Branch: ST (Center = 70)
    draw_arrow((60, 71.2), (70, 66.0), color="#F59E0B", rad=0.06)
    draw_card(70, 63.2, 42, 5.4, "#78350F", "#F59E0B", "Filiere ST", "Sciences & Technologies (Full Engineering)", badge="BRANCH B", title_color="#FDE68A", title_size=13)

    # =========================================================================
    # 4. BRANCH A: MI DETAILS (ONLY 1ST YEAR ACTIVE, NO SPECS, NO ST CONNECTION)
    # =========================================================================
    # Arrow down from MI Branch
    draw_arrow((24, 60.5), (24, 55.5), color="#06B6D4")

    # MI Sub-container explaining state
    draw_card(24, 53.0, 34, 4.4, "#0F172A", "#06B6D4", "MI Academic Status", "Newly opened branch at HNS RE2SD", title_color="#67E8F9", title_size=12)

    # Side-by-side MI cards:
    # 1st Year (ACTIVE) at x=14
    draw_card(14.5, 41.5, 15, 13.5, "#0E3A42", "#10B981", "1ere Annee MI", "Preparatoire",
              badge="ACTIVE",
              items=[
                  "* Active Program",
                  "* Maths, Algos & C",
                  "* Physics, Logic",
                  "* Direct access to",
                  "  drives & apps"
              ], title_color="#34D399", title_size=11, border_width=2.2)

    # Arrow from MI 1st Year straight down to Resource Categories
    draw_arrow((14.5, 34.6), (14.5, 25.5), color="#10B981", width=2.6)
    ax.text(14.5, 29.5, "Direct to Resources", ha="center", va="center", color="#34D399", fontsize=9.5, weight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#064E3B", edgecolor="#10B981", alpha=0.95))

    # Years 2, 3, 4, 5 (GREYED OUT) at x=31.5
    draw_card(31.5, 41.5, 16.5, 13.5, "#1E293B", "#475569", "Annees 2, 3, 4, 5", "Upcoming Promotions",
              badge="NOT OPEN",
              items=[
                  "- Currently inactive",
                  "- Opens in future years",
                  "- No engineering",
                  "  specialties yet",
                  "- (NOT connected to",
                  "  ST specialties)"
              ], title_color="#94A3B8", title_size=11, border_width=1.6, border_style="--")

    # Arrow from MI Status to cards
    draw_arrow((19, 50.7), (15.5, 48.4), color="#10B981")
    draw_arrow((29, 50.7), (31.5, 48.4), color="#475569", linestyle=":")

    # =========================================================================
    # 5. BRANCH B: ST DETAILS (PREPA & 5 SPECIALTIES)
    # =========================================================================
    draw_arrow((70, 60.5), (70, 56.5), color="#F59E0B")

    # ST Year Fork Card
    draw_card(70, 54.0, 42, 4.4, "#0F172A", "#F59E0B", "Select Year in ST (1 to 5)", "Prepa vs Cycle Ingenieur", title_size=12)

    # ST Prepa (Years 1 & 2) at x=52
    draw_card(51.5, 44.5, 17, 8.5, "#0E3A42", "#10B981", "ST Years 1 & 2", "Classes Preparatoires",
              badge="PREPA",
              items=[
                  "* S1 to S4 Prepa Modules",
                  "* Direct access to drives,",
                  "  courses and tools"
              ], title_color="#34D399", title_size=11)

    # Arrow ST Prepa to Resources
    draw_arrow((51.5, 40.1), (51.5, 25.5), color="#10B981", width=2.4)
    ax.text(51.5, 30.5, "Direct to Resources", ha="center", va="center", color="#34D399", fontsize=9.5, weight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#064E3B", edgecolor="#10B981", alpha=0.95))

    # ST Cycle Ingenieur (Years 3, 4, 5) at x=78
    draw_card(78.5, 44.5, 27, 8.5, "#3B0764", "#C084FC", "ST Years 3, 4, 5", "Cycle Ingenieur (Choose Specialty)",
              badge="INGENIEUR",
              items=[
                  "* Access to 5 ST Engineering",
                  "  Specialties at Batna",
                  "* Drives, simulation apps & PFE"
              ], title_color="#E9D5FF", title_size=11)

    draw_arrow((63, 51.7), (53, 48.9), color="#10B981")
    draw_arrow((76, 51.7), (78.5, 48.9), color="#A855F7")

    # 5 ST Specialties Row below ST Cycle Ingenieur
    st_specs = [
        ("IRIIA", "Smart Grids & AI", "#0284C7", 63.5),
        ("uE", "Microelectronics", "#6366F1", 71.0),
        ("ENER", "Energetics & Solar", "#D97706", 78.5),
        ("GH", "Hydrogen Eng.", "#0D9488", 86.0),
        ("GE", "Environment Eng.", "#16A34A", 93.5),
    ]

    for title, desc, col, px in st_specs:
        draw_card(px, 34.0, 7.2, 5.0, "#1E1B4B", col, title, desc, title_color=col, title_size=10, border_width=1.8)
        draw_arrow((78.5, 40.1), (px, 36.6), color=col, width=1.4)
        draw_arrow((px, 31.4), (px, 25.5), color=col, width=1.5)

    # =========================================================================
    # 6. RESOURCE CATEGORIES (FINAL DESTINATION)
    # =========================================================================
    container = FancyBboxPatch(
        (4, 3), 92, 22,
        boxstyle="round,pad=0.4,rounding_size=2",
        facecolor="#0B132B",
        edgecolor="#38BDF8",
        linewidth=2,
        linestyle="--",
        zorder=1
    )
    ax.add_patch(container)
    ax.text(50, 23.5, "ALL ACTIVE STUDENTS ACCESS 4 ESSENTIAL RESOURCE CATEGORIES", 
            ha="center", va="center", color="#38BDF8", fontsize=13, weight="bold")

    # 4 Category Cards
    # Cat 1: Internal Drive (Organized by Promotion Academic Years)
    draw_card(16, 13, 19, 15, "#1E293B", "#10B981", "1. Internal Drive", "Drives par Annee Promo",
              badge="OFFICIAL",
              items=[
                  "* Drive Promo 2024/2025",
                  "* Drive Promo 2023/2024",
                  "* Drive Promo 2022/2023",
                  "* Drive Promo 2021/2022",
                  "* Cours, TD, TP & Examens"
              ], title_color="#34D399", title_size=12)

    # Cat 2: External Drive
    draw_card(38.5, 13, 19, 15, "#1E293B", "#38BDF8", "2. External Drives", "Other Engineering Schools",
              badge="EXTERNAL",
              items=[
                  "* Polytech / ENP Archives",
                  "* USTHB / ESI Drives",
                  "* International Repositories",
                  "* National Concours Prep",
                  "* Engineering Books & PDFs"
              ], title_color="#38BDF8", title_size=12)

    # Cat 3: Applications & Tools
    draw_card(61.5, 13, 19, 15, "#1E293B", "#F59E0B", "3. Software & Tools", "Download & Setup Guides",
              badge="SOFTWARE",
              items=[
                  "* Python, VS Code, GCC",
                  "* MATLAB / GNU Octave",
                  "* Quartus Prime & ModelSim",
                  "* PVsyst & ANSYS Fluent",
                  "* QGIS, Aspen Plus & CAD"
              ], title_color="#FBBF24", title_size=12)

    # Cat 4: YouTube Playlists
    draw_card(84, 13, 19, 15, "#1E293B", "#EF4444", "4. YouTube Playlists", "Top Curated Courses",
              badge="VIDEO",
              items=[
                  "* Algorithmics & Coding in C",
                  "* Analysis & Linear Algebra",
                  "* Physics (Mechanics & Elecs)",
                  "* Machine Learning & IoT",
                  "* Renewable Energy Tuts"
              ], title_color="#F87171", title_size=12)

    # =========================================================================
    # 7. FOOTER
    # =========================================================================
    ax.text(50, 1.4, "HNS RE2SD Batna  •  ERISE Scientific Club  •  24/7 Web Cloud Deployment (Render.com)",
            ha="center", va="center", color="#64748B", fontsize=10, weight="bold")

    output_path = "e:/tel-bot/hns_re2sd_bot_flowchart.png"
    plt.savefig(output_path, dpi=300, facecolor="#0B0F19", edgecolor="none", bbox_inches="tight")
    plt.close()
    print(f"Successfully generated pristine 300 DPI flowchart: {output_path}")

if __name__ == "__main__":
    create_diagram()
