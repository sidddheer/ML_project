import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'expanded_dataset.csv'  # Replace with actual file path
df = pd.read_csv(file_path)

# Ensure all numerical columns are correctly typed
if 'TotalCharges' in df.columns:
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Step 1: Visualize Missing Values
missing_values = df.isnull().sum()
plt.figure(figsize=(10, 6))
sns.barplot(x=missing_values.index, y=missing_values.values)
plt.title("Missing Values in Each Column")
plt.xlabel("Columns")
plt.ylabel("Count of Missing Values")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Step 2: Analyze and Visualize Capped Values
# Analyze extreme percentiles
capped_values = df.describe(percentiles=[0.01, 0.99]).T
print("Capped Values (1st and 99th Percentiles):")
print(capped_values)

# Plot capped values for numerical columns
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
for col in numerical_columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x=col)
    plt.title(f"Box Plot of {col} (Capped Values)")
    plt.show()

# Step 3: Observations about Features
# Distributions of numerical features
df[numerical_columns].hist(bins=20, figsize=(15, 10))
plt.suptitle("Distributions of Numerical Features", y=1.02)
plt.tight_layout()
plt.show()

# Distributions of categorical features
categorical_columns = df.select_dtypes(include=['object', 'category']).columns
for col in categorical_columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y=col, order=df[col].value_counts().index)
    plt.title(f"Distribution of {col}")
    plt.show()

# Step 4: Correlation Matrix and Heatmap
# Compute the correlation matrix for numerical columns
correlation_matrix = df[numerical_columns].corr()

# Plot the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title("Correlation Matrix of Numerical Features")
plt.tight_layout()
plt.show()
