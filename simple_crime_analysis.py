import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# ----------------------------
# 1. Load and clean data
# ----------------------------
FILE_NAME = "crime_data.csv"

try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    print(f"Error: '{FILE_NAME}' not found. Place the CSV in the same folder.")
    exit()

loaded_records = len(df)
df_clean = df.dropna(subset=["outcome", "area"])
cleaned_records = len(df_clean)

# Solved flag
df_clean["solved"] = df_clean["outcome"].str.contains("Solved", case=False, na=False)
with_location = df_clean[df_clean["area"].notna()]
without_location = df[df["area"].isna()]

solve_rate_with_location = with_location["solved"].mean() * 100
solve_rate_without_location = (
    without_location["outcome"].str.contains("Solved", case=False, na=False).mean() * 100
    if len(without_location) > 0
    else 0
)

# ----------------------------
# 2. Prepare charts
# ----------------------------
# Chart 1: Most Common Crime Outcomes
fig1, ax1 = plt.subplots()
df_clean["outcome"].value_counts().plot(kind="bar", ax=ax1)
ax1.set_title("Most Common Crime Outcomes")
ax1.set_xlabel("Outcome")
ax1.set_ylabel("Count")
fig1.tight_layout()
fig1.savefig("chart1_outcomes.png")

# Chart 2: Areas with Highest Crime Counts
fig2, ax2 = plt.subplots()
df_clean["area"].value_counts().head(10).plot(kind="bar", ax=ax2)
ax2.set_title("Areas with Highest Crime Counts")
ax2.set_xlabel("Area")
ax2.set_ylabel("Count")
fig2.tight_layout()
fig2.savefig("chart2_areas.png")

# Chart 3: Crime Solving Rates Comparison
fig3, ax3 = plt.subplots()
ax3.bar(
    ["With Location", "Without Location"],
    [solve_rate_with_location, solve_rate_without_location],
    color=["green", "red"]
)
ax3.set_title("Crime Solving Rates Comparison")
ax3.set_ylabel("Solving Rate (%)")
fig3.tight_layout()
fig3.savefig("chart3_solving_rates.png")

# ----------------------------
# 3. GUI to switch charts
# ----------------------------
class ChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crime Data Charts")
        self.index = 0
        self.figures = [fig1, fig2, fig3]

        # Canvas for matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.figures[self.index], master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.canvas.draw()

        # Buttons to switch charts
        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="<< Previous", command=self.prev_chart).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Next >>", command=self.next_chart).pack(side=tk.LEFT)

    def show_chart(self):
        self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.figures[self.index], master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.canvas.draw()

    def next_chart(self):
        self.index = (self.index + 1) % len(self.figures)
        self.show_chart()

    def prev_chart(self):
        self.index = (self.index - 1) % len(self.figures)
        self.show_chart()

# ----------------------------
# 4. Print summary
# ----------------------------
print(f"Loaded records: {loaded_records}")
print(f"After cleaning: {cleaned_records}")
print(f"Solving rate WITH location: {solve_rate_with_location:.2f}%")
print(f"Solving rate WITHOUT location: {solve_rate_without_location:.2f}%")

# ----------------------------
# 5. Run GUI
# ----------------------------
root = tk.Tk()
app = ChartApp(root)
root.mainloop()
# Program exits automatically when window is closed
