"""
Crime Analysis Dashboard (Interactive Version)
----------------------------------------------
This application demonstrates:
- Data cleaning & normalization
- Duplicate removal
- Transparent preview of cleaned data
- Interactive Plotly visualizations

UI: Tkinter (control & data preview)
Charts: Plotly (dynamic, interactive)

Color Index:
Solved   -> Green
Unsolved -> Red
"""

# ============================
# IMPORTS
# ============================
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
import plotly.express as px


# ============================
# CONFIGURATION
# ============================
FILE_NAME = "crime_data.csv"

STATUS_COLORS = {
    "solved": "green",
    "unsolved": "red"
}


# ============================
# DATA LOADING & CLEANING
# ============================
if not os.path.exists(FILE_NAME):
    raise FileNotFoundError("crime_data.csv not found")

# Load raw data
df_raw = pd.read_csv(FILE_NAME)
df_raw.columns = df_raw.columns.str.strip().str.lower()

# Remove duplicates
df = df_raw.drop_duplicates().copy()

# Normalize outcome → status
df["outcome"] = df["outcome"].astype(str).str.strip().str.lower()

SOLVED_VALUES = {"solved", "closed", "resolved"}
UNSOLVED_VALUES = {"unsolved", "open", "under investigation", "pending"}

def normalize_status(value: str):
    if value in SOLVED_VALUES:
        return "solved"
    if value in UNSOLVED_VALUES:
        return "unsolved"
    return None

df["status"] = df["outcome"].apply(normalize_status)
df = df.dropna(subset=["status"])


# ============================
# PLOTLY VISUALIZATIONS
# ============================
def show_status_plot():
    """Interactive solved vs unsolved chart"""
    data = df["status"].value_counts().reset_index()
    data.columns = ["status", "count"]

    fig = px.bar(
        data,
        x="status",
        y="count",
        color="status",
        color_discrete_map=STATUS_COLORS,
        title="Solved vs Unsolved Crimes",
        text="count"
    )

    fig.update_layout(
        xaxis_title="Crime Status",
        yaxis_title="Number of Cases",
        template="plotly_white"
    )

    fig.show()


def show_crime_type_plot():
    """Top crime types"""
    data = df["crime_type"].value_counts().head(10).reset_index()
    data.columns = ["crime_type", "count"]

    fig = px.bar(
        data,
        x="count",
        y="crime_type",
        orientation="h",
        title="Top Crime Types",
        text="count"
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        template="plotly_white"
    )

    fig.show()


def show_area_plot():
    """Crime distribution by area"""
    data = (
        df["area"]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )
    data.columns = ["area", "count"]
    data["percentage"] = (data["count"] / data["count"].sum()) * 100

    fig = px.bar(
        data,
        x="area",
        y="count",
        text=data["percentage"].round(1).astype(str) + "%",
        title="Top Crime Areas (Count & Percentage)"
    )

    fig.update_layout(
        xaxis_title="Area",
        yaxis_title="Number of Crimes",
        template="plotly_white"
    )

    fig.show()


# ============================
# DASHBOARD UI
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

        self.build_data_tab()
        self.build_status_tab()
        self.build_type_tab()
        self.build_area_tab()

    # ============================
    # CLEANED DATA TAB
    # ============================
    def build_data_tab(self):
        columns = list(df.columns)
        tree = ttk.Treeview(self.tab_data, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=150, anchor="center")

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scrollbar = ttk.Scrollbar(self.tab_data, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ============================
    # STATUS TAB
    # ============================
    def build_status_tab(self):
        ttk.Label(
            self.tab_status,
            text="Interactive visualization of solved vs unsolved crimes",
            font=("Segoe UI", 11)
        ).pack(pady=20)

        ttk.Button(
            self.tab_status,
            text="Open Interactive Chart",
            command=show_status_plot
        ).pack(pady=10)

    # ============================
    # CRIME TYPE TAB
    # ============================
    def build_type_tab(self):
        ttk.Label(
            self.tab_type,
            text="Top crime types based on frequency",
            font=("Segoe UI", 11)
        ).pack(pady=20)

        ttk.Button(
            self.tab_type,
            text="Open Interactive Chart",
            command=show_crime_type_plot
        ).pack(pady=10)

    # ============================
    # AREA TAB
    # ============================
    def build_area_tab(self):
        ttk.Label(
            self.tab_area,
            text="Crime distribution by area",
            font=("Segoe UI", 11)
        ).pack(pady=20)

        ttk.Button(
            self.tab_area,
            text="Open Interactive Chart",
            command=show_area_plot
        ).pack(pady=10)


# ============================
# RUN APPLICATION
# ============================
if __name__ == "__main__":
    root = tk.Tk()
    CrimeDashboard(root)
    root.mainloop()
