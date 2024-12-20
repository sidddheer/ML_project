import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import f1_score, classification_report

# Step 1: Load and preprocess dataset
file_path = 'preprocessed_dataset.csv'  # Adjust as needed
df = pd.read_csv(file_path)

# Convert target labels to numeric
df['Churn'] = df['Churn'].map({'no': 0, 'yes': 1})

# Split data into features and target
X = df.drop(columns=['Churn'])
y = df['Churn']

# Step 2: Define preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), X.select_dtypes(include=['float64', 'int64']).columns),
        ('cat', OneHotEncoder(handle_unknown='ignore'), X.select_dtypes(include=['object']).columns)
    ]
)

# Step 3: Define model pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000))
])

# Step 4: Define hyperparameter grid
param_grid = {
    'classifier__C': [0.01, 0.1, 1, 10, 100],
    'classifier__solver': ['lbfgs']
}

# Step 5: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Hyperparameter tuning
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='f1', verbose=2)
grid_search.fit(X_train, y_train)

# Step 7: Set up MLflow
mlflow.set_tracking_uri("https://dagshub.com/sidd.dheer90/Cust_churn.mlflow")  # Update with your DagsHub details
experiment_name = "logistic_regression_pipeline"

try:
    mlflow.set_experiment(experiment_name)
    print(f"Experiment '{experiment_name}' is ready.")
except mlflow.exceptions.MlflowException as e:
    print(f"Failed to create or get the experiment: {e}")
    print("Ensure the tracking URI and credentials are correct.")
    exit()

# Step 8: Log results to MLflow
with mlflow.start_run():
    # Log best parameters and metrics
    mlflow.log_params(grid_search.best_params_)
    
    y_pred_train = grid_search.best_estimator_.predict(X_train)
    y_pred_test = grid_search.best_estimator_.predict(X_test)
    
    train_f1 = f1_score(y_train, y_pred_train)
    test_f1 = f1_score(y_test, y_pred_test)
    
    mlflow.log_metric("train_f1", train_f1)
    mlflow.log_metric("test_f1", test_f1)
    
    # Log detailed classification report
    print("\nClassification Report (Train):")
    print(classification_report(y_train, y_pred_train))
    print("\nClassification Report (Test):")
    print(classification_report(y_test, y_pred_test))
    
    # Log the model
    mlflow.sklearn.log_model(grid_search.best_estimator_, "logistic_regression_model")

    print("MLflow logging completed successfully.")
