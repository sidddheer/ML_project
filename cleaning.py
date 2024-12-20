import pandas as pd
import numpy as np

# Load the dataset
file_path = 'expanded_dataset.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Step 1: Handle Mismatched String Formats
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip().str.lower()

# Step 2: Remove Duplicate Rows
df.drop_duplicates(inplace=True)

# Step 3: Handle Missing Entries
# Step 3: Handle Missing Entries
for col in df.columns:
    if df[col].dtype in ['float64', 'int64']:
        df[col] = df[col].fillna(df[col].mean())  # Fill numerical with mean
    else:
        df[col] = df[col].fillna(df[col].mode()[0])  # Fill categorical with mode


# Step 4: Convert Data Types
for col in df.columns:
    if df[col].dtype == 'object':
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            pass

# Step 5: Handle Outliers
def remove_outliers(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

for col in df.select_dtypes(include=['float64', 'int64']).columns:
    df = remove_outliers(df, col)

# Step 6: Convert String Columns to Categorical
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype('category')

# Step 7: Perform Binning
# Example: Bin 'MonthlyCharges' into 5 equal-sized bins
if 'MonthlyCharges' in df.columns:
    df['MonthlyCharges_Binned'] = pd.cut(df['MonthlyCharges'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])

# Save the preprocessed dataset
preprocessed_file_path = 'preprocessed_dataset.csv'
df.to_csv(preprocessed_file_path, index=False)

print(f"Preprocessing completed. Preprocessed data saved to '{preprocessed_file_path}'")
