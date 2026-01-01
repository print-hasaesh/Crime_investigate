# Simple Crime Data Analysis

This project is a basic crime data analysis program written in Python using pandas and matplotlib. The program loads crime data from a CSV file, cleans the data, performs simple analysis, generates visualizations, and validates the results using automated tests.

The program reads a CSV file placed in the same directory and prints the total number of records loaded. It then removes rows with missing critical values such as crime outcome or area and prints the number of records remaining after cleaning.

After cleaning, the program analyzes the data to find the most common crime outcomes and the areas with the highest number of crimes. It also compares crime solving rates for cases that include location data versus those that do not. The solving rate with location data is expected to be higher.

Three bar charts are generated and saved as image files:
- chart1_outcomes.png showing common crime outcomes  
- chart2_areas.png showing areas with the highest crime counts  
- chart3_solving_rates.png comparing solving rates  

To run the program, place the CSV file in the same folder and execute:
```bash
python simple_crime_analysis.py
