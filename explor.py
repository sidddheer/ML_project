import pandas as pd
from sklearn.model_selection import train_test_split

# Load the data (replace with your database query result)
df = pd.read_csv('preprocessed_dataset.csv')  # Replace with actual file or DataFrame

# Step 1: Analyze Attribute Distribution
# Check the distribution of the target variable
if 'Churn' in df.columns:
    print("Distribution of 'Churn':")
    print(df['Churn'].value_counts(normalize=True))
else:
    raise ValueError("Target column 'Churn' not found in the dataset.")

# Step 2: Decide on Stratification
# Stratify by 'Churn' to maintain its distribution in train/test sets

# Step 3: Train/Test Split
# Prepare features (X) and target variable (y)
X = df.drop(columns=['Churn'])  # Features (all columns except the target)
y = df['Churn']  # Target variable

# Perform stratified train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Verify the split
print("\nTrain set 'Churn' distribution:")
print(y_train.value_counts(normalize=True))

print("\nTest set 'Churn' distribution:")
print(y_test.value_counts(normalize=True))

