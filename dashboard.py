"""
Crime Analysis Dashboard
------------------------
Demonstrates data cleaning, normalization,
and visualization of noisy crime data.
"""

# ============================
# IMPORTS
# ============================
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================
# DATA LOADING & CLEANING
# ============================

FILE_NAME = "crime_data.csv"

if not os.path.exists(FILE_NAME):
    raise FileNotFoundError("crime_data.csv not found")

df_raw = pd.read_csv(FILE_NAME)
df_raw.columns = df_raw.columns.str.strip().str.lower()

# Remove duplicates
df = df_raw.drop_duplicates().copy()

# Normalize outcome → status
df["outcome"] = df["outcome"].astype(str).str.strip().str.lower()

SOLVED_VALUES = {"solved", "closed", "resolved"}
UNSOLVED_VALUES = {"unsolved", "open", "under investigation", "pending"}

def normalize_status(val):
    if val in SOLVED_VALUES:
        return "solved"
    if val in UNSOLVED_VALUES:
        return "unsolved"
    return None

df["status"] = df["outcome"].apply(normalize_status)
df = df.dropna(subset=["status"])


# ============================
# DASHBOARD CLASS
# ============================
class CrimeDashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("Crime Analysis Dashboard")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        # Tabs
        self.tab_data = ttk.Frame(notebook)
        self.tab_status = ttk.Frame(notebook)
        self.tab_type = ttk.Frame(notebook)
        self.tab_area = ttk.Frame(notebook)

        notebook.add(self.tab_data, text="Cleaned Data")
        notebook.add(self.tab_status, text="Solved vs Unsolved")
        notebook.add(self.tab_type, text="Crime Types")
        notebook.add(self.tab_area, text="Crime Areas")

        # Render
        self.show_cleaned_data()
        self.plot_status_chart()
        self.plot_type_chart()
        self.plot_area_chart()

    # ============================
    # UTILITY
    # ============================
    def draw_chart(self, frame, fig):
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ============================
    # TAB 1: CLEANED DATA TABLE
    # ============================
    def show_cleaned_data(self):
        cols = list(df.columns)
        tree = ttk.Treeview(self.tab_data, columns=cols, show="headings")

        for col in cols:
            tree.heading(col, text=col.title())
            tree.column(col, width=150, anchor="center")

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scrollbar = ttk.Scrollbar(self.tab_data, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ============================
    # TAB 2: SOLVED vs UNSOLVED
    # ============================
    def plot_status_chart(self):
        counts = df["status"].value_counts()

        colors = ["#4CAF50", "#F44336"]

        fig, ax = plt.subplots(figsize=(6, 5))
        bars = ax.bar(counts.index, counts.values, color=colors)

        ax.set_title("Solved vs Unsolved Crimes")
        ax.set_ylabel("Number of Cases")

        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    int(bar.get_height()),
                    ha="center", va="bottom")

        fig.tight_layout()
        self.draw_chart(self.tab_status, fig)

    # ============================
    # TAB 3: CRIME TYPES
    # ============================
    def plot_type_chart(self):
        type_counts = df["crime_type"].value_counts().head(10)

        colors = plt.cm.tab10(range(len(type_counts)))

        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.barh(type_counts.index, type_counts.values, color=colors)

        ax.set_title("Top Crime Types")
        ax.set_xlabel("Number of Cases")

        for bar in bars:
            ax.text(bar.get_width(),
                    bar.get_y() + bar.get_height() / 2,
                    int(bar.get_width()),
                    va="center")

        fig.tight_layout()
        self.draw_chart(self.tab_type, fig)

    # ============================
    # TAB 4: CRIME AREAS (IMPROVED)
    # ============================
    def plot_area_chart(self):
        area_counts = (
            df["area"]
            .dropna()
            .astype(str)
            .str.strip()
            .value_counts()
            .head(10)
        )

        total = area_counts.sum()
        colors = plt.cm.viridis(range(len(area_counts)))

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(area_counts.index, area_counts.values, color=colors)

        ax.set_title("Top Crime Areas (Count & Percentage)")
        ax.set_ylabel("Number of Crimes")

        for bar, value in zip(bars, area_counts.values):
            percent = (value / total) * 100
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"{value} ({percent:.1f}%)",
                    ha="center", va="bottom")

        fig.tight_layout()
        self.draw_chart(self.tab_area, fig)


# ============================
# RUN APPLICATION
# ============================
if __name__ == "__main__":
    root = tk.Tk()
    CrimeDashboard(root)
    root.mainloop()
