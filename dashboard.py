import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
import plotly.express as px

FILE_NAME = "crime_data.csv"

STATUS_COLORS = {
    "solved": "green",
    "unsolved": "red"
}

if not os.path.exists(FILE_NAME):
    raise FileNotFoundError("crime_data.csv not found")

df_raw = pd.read_csv(FILE_NAME)
df_raw.columns = df_raw.columns.str.strip().str.lower()

raw_count = len(df_raw)

df = df_raw.drop_duplicates().copy()
duplicates_removed = raw_count - len(df)

df["outcome"] = df["outcome"].astype(str).str.strip().str.lower()

SOLVED_VALUES = {"solved", "closed", "resolved"}
UNSOLVED_VALUES = {"unsolved", "open", "under investigation", "pending"}

def normalize_status(value):
    if value in SOLVED_VALUES:
        return "solved"
    if value in UNSOLVED_VALUES:
        return "unsolved"
    return None

df["status"] = df["outcome"].apply(normalize_status)
before_status = len(df)
df = df.dropna(subset=["status"])
invalid_status_removed = before_status - len(df)

df["reported_date"] = pd.to_datetime(df["reported_date"], errors="coerce")
df = df.dropna(subset=["reported_date"])

cleaned_count = len(df)

def plot_status():
    data = df["status"].value_counts().reset_index()
    data.columns = ["status", "count"]

    fig = px.bar(
        data,
        x="status",
        y="count",
        color="status",
        color_discrete_map=STATUS_COLORS,
        text="count",
        title="Solved vs Unsolved Crimes"
    )
    fig.update_layout(template="plotly_white")
    fig.show()

def plot_type():
    data = df["crime_type"].value_counts().head(10).reset_index()
    data.columns = ["crime_type", "count"]

    fig = px.bar(
        data,
        x="crime_type",
        y="count",
        text="count",
        title="Top Crime Types"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Crime Type",
        yaxis_title="Number of Cases"
    )

    fig.show()


def plot_area():
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

    fig = px.bar(
        data,
        x="area",
        y="count",
        text="count",
        title="Top Crime Areas"
    )
    fig.update_layout(template="plotly_white")
    fig.show()

def plot_timeline():
    data = df.groupby(df["reported_date"].dt.to_period("M")).size().reset_index(name="count")
    data["reported_date"] = data["reported_date"].astype(str)

    fig = px.line(
        data,
        x="reported_date",
        y="count",
        markers=True,
        title="Crime Trend Over Time"
    )
    fig.update_layout(template="plotly_white")
    fig.show()

PLOTS = [
    ("Solved vs Unsolved", plot_status),
    ("Crime Types", plot_type),
    ("Crime Areas", plot_area),
    ("Timeline", plot_timeline)
]

class CrimeDashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("Crime Analysis Dashboard")
        self.root.geometry("1150x720")
        self.root.resizable(False, False)

        self.plot_index = 0

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        self.tab_summary = ttk.Frame(notebook)
        self.tab_data = ttk.Frame(notebook)
        self.tab_visuals = ttk.Frame(notebook)

        notebook.add(self.tab_summary, text="Summary")
        notebook.add(self.tab_data, text="Cleaned Data")
        notebook.add(self.tab_visuals, text="Visual Analytics")

        self.build_summary_tab()
        self.build_data_tab()
        self.build_visual_tab()

    def build_summary_tab(self):
        container = ttk.Frame(self.tab_summary)
        container.pack(pady=40)

        ttk.Label(
            container,
            text="Data Cleaning Overview",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        stats = [
            ("Raw records loaded", raw_count),
            ("Duplicate records removed", duplicates_removed),
            ("Invalid status removed", invalid_status_removed),
            ("Final cleaned records", cleaned_count)
        ]

        for label, value in stats:
            ttk.Label(
                container,
                text=f"{label}: {value}",
                font=("Segoe UI", 12)
            ).pack(pady=6)

    def build_data_tab(self):
        ttk.Label(
            self.tab_data,
            text="Cleaned & Normalized Crime Data",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        columns = list(df.columns)
        tree = ttk.Treeview(self.tab_data, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col.upper())
            tree.column(col, width=140, anchor="center")

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

        scrollbar = ttk.Scrollbar(self.tab_data, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def build_visual_tab(self):
        ttk.Label(
            self.tab_visuals,
            text="Interactive Crime Analytics",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        self.selected_label = ttk.Label(
            self.tab_visuals,
            text=f"Selected Graph: {PLOTS[self.plot_index][0]}",
            font=("Segoe UI", 11, "italic")
        )
        self.selected_label.pack(pady=8)

        btn_frame = ttk.Frame(self.tab_visuals)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Previous", command=self.prev_plot).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Next", command=self.next_plot).pack(side="left", padx=10)

        ttk.Button(
            self.tab_visuals,
            text="Open Interactive Chart",
            command=self.show_current_plot
        ).pack(pady=20)

    def show_current_plot(self):
        PLOTS[self.plot_index][1]()

    def next_plot(self):
        self.plot_index = (self.plot_index + 1) % len(PLOTS)
        self.update_label()

    def prev_plot(self):
        self.plot_index = (self.plot_index - 1) % len(PLOTS)
        self.update_label()

    def update_label(self):
        self.selected_label.config(
            text=f"Selected Graph: {PLOTS[self.plot_index][0]}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    CrimeDashboard(root)
    root.mainloop()
