import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================================================
# SAMPLE DATA GENERATOR - Multiple Datasets with Chart Recommendations
# ============================================================================

# Dataset 1: E-commerce Sales (Time Series + Categorical)
def create_sales_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = {
        'Date': dates,
        'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Watch'], len(dates)),
        'Category': np.random.choice(['Electronics', 'Accessories'], len(dates)),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], len(dates)),
        'Sales': np.random.randint(500, 5000, len(dates)),
        'Units_Sold': np.random.randint(1, 50, len(dates)),
        'Discount': np.random.uniform(0, 0.3, len(dates))
    }
    return pd.DataFrame(data)

# Dataset 2: Student Performance (Multiple Metrics)
def create_student_data():
    np.random.seed(42)
    data = {
        'Student_Name': [f'Student_{i}' for i in range(100)],
        'Department': np.random.choice(['CS', 'Physics', 'Chemistry', 'Biology'], 100),
        'Math_Score': np.random.randint(40, 100, 100),
        'Science_Score': np.random.randint(35, 98, 100),
        'English_Score': np.random.randint(30, 95, 100),
        'Attendance': np.random.randint(60, 100, 100),
        'Study_Hours': np.random.uniform(1, 8, 100).round(1),
        'GPA': np.random.uniform(2.0, 4.0, 100).round(2)
    }
    return pd.DataFrame(data)

# Dataset 3: Website Analytics (Traffic Data)
def create_analytics_data():
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    data = {
        'Date': dates,
        'Page': np.random.choice(['Home', 'About', 'Contact', 'Blog', 'Products'], 90),
        'Device': np.random.choice(['Mobile', 'Desktop', 'Tablet'], 90),
        'Sessions': np.random.randint(100, 5000, 90),
        'Users': np.random.randint(50, 3000, 90),
        'Bounce_Rate': np.random.uniform(20, 80, 90).round(1),
        'Avg_Session_Duration': np.random.uniform(1, 10, 90).round(2)
    }
    return pd.DataFrame(data)

# Dataset 4: Company HR Data (Demographics + Performance)
def create_hr_data():
    data = {
        'Employee_ID': range(1, 201),
        'Department': np.random.choice(['HR', 'Sales', 'IT', 'Marketing', 'Finance'], 200),
        'Salary': np.random.randint(30000, 150000, 200),
        'Experience_Years': np.random.randint(0, 25, 200),
        'Performance_Rating': np.random.uniform(1, 5, 200).round(1),
        'Age': np.random.randint(22, 65, 200),
        'Tenure_Years': np.random.randint(0, 20, 200)
    }
    return pd.DataFrame(data)

# Dataset 5: Weather Data (Time Series Multiple Variables)
def create_weather_data():
    dates = pd.date_range(start='2023-01-01', periods=365, freq='D')
    data = {
        'Date': dates,
        'City': np.random.choice(['New York', 'London', 'Tokyo', 'Paris'], 365),
        'Temperature': np.random.uniform(0, 40, 365).round(1),
        'Humidity': np.random.randint(30, 90, 365),
        'Precipitation': np.random.uniform(0, 50, 365).round(1),
        'Wind_Speed': np.random.uniform(0, 30, 365).round(1),
        'Condition': np.random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy'], 365)
    }
    return pd.DataFrame(data)

# ============================================================================
# CHART RECOMMENDATIONS GUIDE
# ============================================================================

CHART_GUIDE = {
    'Bar Chart': {
        'Best For': 'Comparing values across categories',
        'When to Use': 'Total sales by product, count by department, revenue by region',
        'Example': 'df.groupby("Product")["Sales"].sum() → Bar chart',
        'Dataset': 'Sales Data, HR Data, Student Data'
    },
    'Line Chart': {
        'Best For': 'Showing trends over time',
        'When to Use': 'Daily sales trend, temperature over months, user growth',
        'Example': 'X: Date, Y: Sales → Line chart',
        'Dataset': 'Sales Data, Weather Data, Analytics Data'
    },
    'Scatter Plot': {
        'Best For': 'Finding relationships between two numeric variables',
        'When to Use': 'Salary vs Experience, Score vs Study Hours, Temperature vs Humidity',
        'Example': 'X: Experience, Y: Salary → Scatter with trendline',
        'Dataset': 'HR Data, Student Data, Weather Data'
    },
    'Histogram': {
        'Best For': 'Showing distribution of a single numeric variable',
        'When to Use': 'Distribution of ages, salaries, test scores, session duration',
        'Example': 'X: Salary → Histogram with bins',
        'Dataset': 'HR Data, Student Data, Analytics Data'
    },
    'Box Plot': {
        'Best For': 'Comparing distributions across groups (quartiles, outliers)',
        'When to Use': 'Salary by department, scores by class, performance by team',
        'Example': 'X: Department, Y: Salary → Box plot',
        'Dataset': 'HR Data, Student Data'
    },
    'Pie Chart': {
        'Best For': 'Showing parts of a whole (percentages)',
        'When to Use': 'Market share, budget allocation, product mix, category split',
        'Example': 'Categories: [Laptop, Phone, Tablet], Values: [counts]',
        'Dataset': 'Sales Data, Analytics Data'
    },
    'Donut Chart': {
        'Best For': 'Same as pie chart but with cleaner aesthetics',
        'When to Use': 'Department distribution, device type breakdown',
        'Example': 'Similar to pie but with hollow center',
        'Dataset': 'HR Data, Analytics Data'
    },
    'Sunburst Chart': {
        'Best For': 'Hierarchical data with multiple levels',
        'When to Use': 'Sales by Region → Category → Product, Revenue breakdown',
        'Example': 'Path: [Region, Category], Values: Sales',
        'Dataset': 'Sales Data (advanced)'
    },
    'Heatmap': {
        'Best For': 'Showing correlations or relationships in matrix form',
        'When to Use': 'Correlation between all numeric columns',
        'Example': 'Correlation matrix of: Age, Salary, Experience, Performance',
        'Dataset': 'HR Data, Student Data, Weather Data'
    },
    'Violin Plot': {
        'Best For': 'Comparing distributions with density visualization',
        'When to Use': 'Score distribution by department, salary by gender',
        'Example': 'X: Department, Y: Salary → Violin plot',
        'Dataset': 'HR Data, Student Data'
    },
    'Area Chart': {
        'Best For': 'Cumulative trends or stacked values over time',
        'When to Use': 'Cumulative revenue over months, stacked sales by category',
        'Example': 'X: Date, Y: Sales, Color: Product',
        'Dataset': 'Sales Data, Analytics Data'
    }
}

# ============================================================================
# SAVE SAMPLE DATASETS TO CSV
# ============================================================================

if __name__ == "__main__":
    # Create all datasets
    sales_df = create_sales_data()
    student_df = create_student_data()
    analytics_df = create_analytics_data()
    hr_df = create_hr_data()
    weather_df = create_weather_data()
    
    # Save to CSV
    sales_df.to_csv('sample_sales_data.csv', index=False)
    student_df.to_csv('sample_student_data.csv', index=False)
    analytics_df.to_csv('sample_analytics_data.csv', index=False)
    hr_df.to_csv('sample_hr_data.csv', index=False)
    weather_df.to_csv('sample_weather_data.csv', index=False)
    
    print("✅ Sample datasets created!")
    print("\n📊 FILES CREATED:")
    print("  • sample_sales_data.csv")
    print("  • sample_student_data.csv")
    print("  • sample_analytics_data.csv")
    print("  • sample_hr_data.csv")
    print("  • sample_weather_data.csv")
    
    print("\n" + "="*70)
    print("CHART RECOMMENDATION GUIDE")
    print("="*70)
    
    for chart, details in CHART_GUIDE.items():
        print(f"\n📈 {chart}")
        print(f"   Best For: {details['Best For']}")
        print(f"   Use Cases: {details['When to Use']}")
        print(f"   Example: {details['Example']}")
        print(f"   Try With: {details['Dataset']}")