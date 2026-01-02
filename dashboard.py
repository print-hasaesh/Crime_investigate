import os
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ============================
# 1. LOAD & CLEAN DATA
# ============================
FILE_NAME = "crime_data.csv"

if not os.path.exists(FILE_NAME):
    raise FileNotFoundError("crime_data.csv not found")

df = pd.read_csv(FILE_NAME)
loaded_records = len(df)

df["reported_date"] = pd.to_datetime(df["reported_date"], errors="coerce")
df_clean = df.dropna(subset=["outcome"])
cleaned_records = len(df_clean)

df_clean["solved"] = df_clean["outcome"].str.contains("Solved", case=False, na=False)

with_location = df_clean[df_clean["area"].notna()]
without_location = df_clean[df_clean["area"].isna()]

solve_rate_with = with_location["solved"].mean() * 100
solve_rate_without = (
    without_location["solved"].mean() * 100 if len(without_location) else 0
)

# ============================
# 2. CREATE FIGURES (FIXED SIZE)
# ============================
def make_figure():
    fig, ax = plt.subplots(figsize=(5.5, 4), dpi=100)
    fig.subplots_adjust(bottom=0.30)  # ← key fix
    return fig, ax

figures = []

# Chart 1: Outcomes
fig1, ax1 = make_figure()
df_clean["outcome"].value_counts().plot(kind="bar", ax=ax1)
ax1.set_title("Crime Outcomes")
figures.append(fig1)

# Chart 2: Crime Types
fig2, ax2 = make_figure()
df_clean["crime_type"].value_counts().plot(kind="bar", ax=ax2)
ax2.set_title("Crimes by Type")
figures.append(fig2)

# Chart 3: Severity
fig3, ax3 = make_figure()
df_clean["severity"].value_counts().plot(
    kind="pie", autopct="%1.1f%%", ax=ax3
)
ax3.set_ylabel("")
ax3.set_title("Crime Severity Distribution")
figures.append(fig3)

# Chart 4: Monthly Trend
fig4, ax4 = make_figure()
monthly = (
    df_clean.dropna(subset=["reported_date"])
    .set_index("reported_date")
    .resample("ME")
    .size()
)
monthly.plot(ax=ax4)
ax4.set_title("Monthly Crime Trend")
ax4.set_xlabel("Month")
ax4.set_ylabel("Cases")
figures.append(fig4)

# Chart 5: Solve Rate Comparison
fig5, ax5 = make_figure()
ax5.bar(
    ["With Location", "Without Location"],
    [solve_rate_with, solve_rate_without]
)
ax5.set_title("Solve Rate Comparison")
ax5.set_ylabel("Solve Rate (%)")
figures.append(fig5)

# ============================
# 3. GUI APPLICATION
# ============================
class CrimeDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Crime Data Dashboard")
        self.root.geometry("900x600")

        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True)

        # -------- SUMMARY TAB --------
        summary_tab = ttk.Frame(notebook)
        notebook.add(summary_tab, text="Summary")

        tree = ttk.Treeview(
            summary_tab, columns=("Metric", "Value"), show="headings", height=6
        )
        tree.heading("Metric", text="Metric")
        tree.heading("Value", text="Value")
        tree.column("Metric", width=300)
        tree.column("Value", width=200)

        summary_data = [
            ("Loaded Records", loaded_records),
            ("Records After Cleaning", cleaned_records),
            ("Solve Rate (With Location)", f"{solve_rate_with:.2f}%"),
            ("Solve Rate (Without Location)", f"{solve_rate_without:.2f}%"),
        ]

        for row in summary_data:
            tree.insert("", tk.END, values=row)

        tree.pack(padx=20, pady=20)

        # -------- CHARTS TAB --------
        self.charts_tab = ttk.Frame(notebook)
        notebook.add(self.charts_tab, text="Charts")

        self.index = 0
        self.canvas = None
        self.show_chart()

        btn_frame = ttk.Frame(self.charts_tab)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="◀ Previous", command=self.prev_chart).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Next ▶", command=self.next_chart).pack(
            side=tk.LEFT, padx=5
        )

    def show_chart(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(
            figures[self.index],
            master=self.charts_tab
        )
        self.canvas.draw()

        widget = self.canvas.get_tk_widget()
        widget.pack(padx=10, pady=10)

    def next_chart(self):
        self.index = (self.index + 1) % len(figures)
        self.show_chart()

    def prev_chart(self):
        self.index = (self.index - 1) % len(figures)
        self.show_chart()

# ============================
# 4. RUN APP
# ============================
if __name__ == "__main__":
    root = tk.Tk()
    CrimeDashboard(root)
    root.mainloop()