'''
PRACTICAL EXAM

PROJECT TITLE:- Retail Sales Data Analyzer

OBJECTIVE:- Develop a Python-based Retail Sales Data Analyzer tool to process, 
            analyze, and visualize sales data. The project must integrate Control 
            Structure, Arrays, OOP, NumPy, Pandas with Datasets, and Matplotlib & 
            Seaborn to deliver meaningful insights. 

'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 🏪 Class to Analyze Retail Sales Data
class RetailAnalyzer:
    def __init__(self):
        """Constructor to initialize class attributes"""
        self.data = None
        print("\n\n✅ RetailAnalyzer object created.")

    def load_data(self, file_path):
        """Load CSV file and validate"""
        if file_path.endswith(".csv"):
            try:
                self.data = pd.read_csv(file_path)
                print("📂 File loaded successfully.")
            except FileNotFoundError:
                print("❌ File not found. Check the path.")
        else:
            print("❌ Invalid file format. Please use a .csv file.")

    def check_missing_values(self):
        """Check and report missing values"""
        if self.data is not None:
            print("\n🧼 Missing Values Check:")
            print(self.data.isnull().sum())
        else:
            print("⚠️ No data loaded.")

    def clean_data(self):
        """Drop rows with any missing values"""
        if self.data is not None:
            self.data.dropna(inplace=True)
            print("✅ Missing values dropped.")
        else:
            print("⚠️ No data to clean.")

    def calculate_metrics(self):
        """Calculate total sales, average sales, and most popular product"""
        if self.data is not None:
            total_sales = self.data["Total Sales"].sum()
            average_sales = self.data["Total Sales"].mean()
            popular_product = self.data["Product"].value_counts().idxmax()

            pd.set_option('display.max_colwidth', None)
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            print("\n📊 Sales Metrics:")
            print("🧾 Total Sales: ₹", round(total_sales, 2))
            print("📈 Average Sales: ₹", round(average_sales, 2))
            print("🏆 Most Popular Product:", popular_product)
        else:
            print("⚠️ No data loaded.")

    def filter_data(self):
        """Allow user to filter data by Category or Date Range, or return to main menu"""
        if self.data is None:
            print("⚠️ No data loaded.")
            return

        while True:
            print("\n📍 Filter Options:")
            print("1. Filter by Category")
            print("2. Filter by Date Range")
            print("3. 🔙 Return to Main Menu")

            choice = input("Enter your choice (1–3): ").strip()

            if choice == "1":
                column = "Category"
                unique_categories = self.data[column].dropna().unique()

                pd.set_option('display.max_colwidth', None)
                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                print("\n📦 Available Categories:")
                for i, cat in enumerate(unique_categories, 1):
                    print(f"{i}. {cat}")

                value = input("Enter exact category name from above: ").strip()
                filtered = self.data[self.data[column] == value]

            elif choice == "2":
                # Ensure 'Date' column is datetime
                self.data["Date"] = pd.to_datetime(self.data["Date"], errors='coerce')
                print("\n📅 Filter by Date Range")
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()

                try:
                    start = pd.to_datetime(start_date)
                    end = pd.to_datetime(end_date)
                    filtered = self.data[(self.data["Date"] >= start) & (self.data["Date"] <= end)]
                except:
                    print("❌ Invalid date format.")
                    continue

            elif choice == "3":
                print("🔙 Returning to main menu...")
                break

            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                continue

            total = len(filtered)
            print(f"\n🔍 Total matching records: {total}")
            if total > 0:
                print("\n📌 Top 10 records:")
                print(filtered.head(10))
            else:
                print("⚠️ No matching records found.")

    def display_summary(self):
        """Display dataset summary"""
        if self.data is not None:
            print("\n📄 Data Summary:")
            print(self.data.describe())
        else:
            print("⚠️ No data loaded.")
    
    def generate_computed_columns(self):
        """Generate new computed metric columns and add to the dataset"""
        if self.data is None:
            print("⚠️ No data loaded.")
            return

        print("\n🧮 Generating computed columns...")

        # Ensure 'Date' column is in datetime format
        self.data["Date"] = pd.to_datetime(self.data["Date"], errors='coerce')

        # 1. Sales Percentage of each row
        total_sales = self.data["Total Sales"].sum()
        self.data["Sales %"] = (self.data["Total Sales"] / total_sales) * 100

        # 2. Cumulative Sales (running total)
        self.data = self.data.sort_values("Date")  # sort by date first
        self.data["Cumulative Sales"] = self.data["Total Sales"].cumsum()

        # 3. Is High Sale? → Boolean flag
        avg_sale = self.data["Total Sales"].mean()
        self.data["Is High Sale?"] = self.data["Total Sales"] > avg_sale

        pd.set_option('display.max_colwidth', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        print("✅ Computed columns added: 'Sales %', 'Cumulative Sales', 'Is High Sale?'")
        print("\n📌 Preview of updated data (top 5 rows):")
        print(self.data.head())


    def compute_numpy_metrics(self):
        """Use NumPy to calculate sales percentage and growth rates"""
        if self.data is not None:
            print("\n📊 NumPy Metrics: Sales % and Growth Rate\n")

            # Step 1: Convert "Total Sales" column to NumPy array
            sales_array = np.array(self.data["Total Sales"])

            # Step 2: Total sum of all sales
            total_sales = sales_array.sum()

            # Step 3: Sales Percentage = (individual sale / total sales) * 100
            sales_percentages = (sales_array / total_sales) * 100

            print("📌 First 10 Sales Percentage Values (% of total sales):")
            print(np.round(sales_percentages[:10], 2))  # rounded to 2 decimal places

            # Step 4: Growth Rate = ((current - previous) / previous) * 100
            growth_rates = np.diff(sales_array) / sales_array[:-1] * 100

            print("\n📈 First 10 Growth Rates (% change from previous):")
            print(np.round(growth_rates[:10], 2))  # only first 10 for display
        else:
            print("⚠️ No data loaded.")

    def aggregate_sales_data(self):
        """Aggregate total sales by Product, Category, or Date"""
        if self.data is None:
            print("⚠️ Please load the data first.")
            return

        while True:
            print("\n🔢 Sales Aggregation Menu:")
            print("1. Group by Product")
            print("2. Group by Category")
            print("3. Group by Date")
            print("4. 🔙 Return to Main Menu")

            choice = input("Enter your choice (1–4): ").strip()

            if choice == "1":
                grouped = self.data.groupby("Product")["Total Sales"].sum().sort_values(ascending=False)
                print("\n📦 Top 10 Products by Total Sales:")
                print(grouped.head(10))

            elif choice == "2":
                grouped = self.data.groupby("Category")["Total Sales"].sum().sort_values(ascending=False)
                print("\n🏷️ Total Sales by Category:")
                print(grouped)

            elif choice == "3":
                # Make sure Date column is datetime
                self.data["Date"] = pd.to_datetime(self.data["Date"], errors='coerce')
                grouped = self.data.groupby("Date")["Total Sales"].sum().sort_index()
                print("\n📅 Total Sales by Date (Top 10):")
                print(grouped.head(10))

            elif choice == "4":
                print("🔙 Returning to main menu...")
                break

            else:
                print("❌ Invalid choice. Please try again.")

    def visualize_data(self):
        """Generate visualizations using Matplotlib and Seaborn"""
        if self.data is not None:
            sns.set_theme(style="whitegrid")

            while True:
                print("\n📊 Visualization Menu:")
                print("1. Bar Chart - Total Sales by Category")
                print("2. Line Chart - Sales Over Time")
                print("3. Heatmap - Correlation between Price and Quantity")
                print("4. Exit Visualization")

                choice = input("Enter your choice (1-4): ")

                if choice == "1":
                    plt.figure(figsize=(10, 5))
                    category_sales = self.data.groupby("Category")["Total Sales"].sum()
                    sns.barplot(x=category_sales.index, y=category_sales.values, palette="viridis")
                    plt.title("Total Sales by Category")
                    plt.xlabel("Category")
                    plt.ylabel("Sales")
                    plt.xticks(rotation=30)
                    plt.tight_layout()

                elif choice == "2":
                    self.data["Date"] = pd.to_datetime(self.data["Date"])
                    daily_sales = self.data.groupby("Date")["Total Sales"].sum()
                    plt.figure(figsize=(12, 6))
                    plt.plot(daily_sales.index, daily_sales.values, color="blue")
                    plt.title("Sales Over Time")
                    plt.xlabel("Date")
                    plt.ylabel("Total Sales")
                    plt.xticks(rotation=30)
                    plt.tight_layout()

                elif choice == "3":
                    plt.figure(figsize=(8, 5))
                    corr = self.data[["Price", "Quantity Sold"]].corr()
                    sns.heatmap(corr, annot=True, cmap="YlGnBu", linewidths=0.5)
                    plt.title("Correlation Heatmap")
                    plt.tight_layout()

                elif choice == "4":
                    print("Returning to main menu...")
                    break

                else:
                    print("❌ Invalid choice.")
                    continue

                # Ask to save BEFORE showing the chart
                save = input("💾 Do you want to save this chart? (y/n): ").lower()
                if save == 'y':
                    filename = input("Enter filename (e.g., chart.png): ").strip()
                    if not filename.endswith(".png"):
                        filename += ".png"
                    try:
                        plt.savefig(filename, dpi=300, bbox_inches='tight')
                        print(f"✅ Chart saved as '{filename}'.")
                    except Exception as e:
                        print("❌ Error saving chart:", e)

                # Now show the chart after saving
                plt.show()

        else:
            print("⚠️ Please load data first.")


# ================================
# 🎬 MAIN MENU DRIVEN PROGRAM
# ================================

def main():
    analyzer = RetailAnalyzer()

    while True:
        print("""
================ Retail Sales Data Analyzer ================
1. Load Data
2. Check Missing Values
3. Clean Data
4. Calculate Metrics
5. Filter Data by Category
6. Display Summary
7. Generate Computed Metric Columns
8. NumPy Growth Metrics
9. Aggregate Sales Data
10. Visualize Data
11. Exit
============================================================
        """)

        choice = input("Enter your choice: ")

        if choice == "1":
            path = input("Enter path to CSV file: ")
            analyzer.load_data(path)

        elif choice == "2":
            analyzer.check_missing_values()

        elif choice == "3":
            analyzer.clean_data()

        elif choice == "4":
            analyzer.calculate_metrics()

        elif choice == "5":
            analyzer.filter_data()

        elif choice == "6":
            analyzer.display_summary()

        elif choice == "7":
            analyzer.generate_computed_columns()


        elif choice == "8":
            analyzer.compute_numpy_metrics()

        elif choice == "9":
            analyzer.aggregate_sales_data()

        elif choice == "10":
            analyzer.visualize_data()

        elif choice == "11":
            print("👋 Exiting program.")
            break

        else:
            print("❌ Invalid choice. Try again.")

# Program entry point
if __name__ == "__main__":
    main()
