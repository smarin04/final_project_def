from typing import List, Dict, Any

from sklearn.model_selection import train_test_split                                                                  #, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor                                         #!
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
)
import polars as pl
import os                                                                                                             #!



class HousePricePredictor:
    def __init__(self, train_data_path: str, test_data_path: str):
        try:
            self.train_data = pl.read_csv(train_data_path,
                                          null_values="NA")
            self.test_data = pl.read_csv(test_data_path,
                                         null_values="NA")
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")
        self.models = {}



    def clean_data(self):
        def clean(df: pl.DataFrame) -> pl.DataFrame:
            #Missing Values
            threshold = len(df) * 0.75
            cols_to_keep = [
                col for col in df.columns if df[col].null_count() < threshold
            ]

            df = df.select(cols_to_keep)

            #Fill with Mean (Numeric)
            numeric_cols = df.select(pl.col(pl.Float64),
                                     pl.col(pl.Int64)).columns
            for col in numeric_cols:
                mean_value = df[col].mean()
                df = df.with_columns(
                    pl.col(col).fill_null(mean_value).alias(col)
                )

            #Fill with Placeholder (Categorical)
            categorical_cols = df.select(pl.col(pl.Utf8)).columns
            for col in categorical_cols:
                df = df.with_columns(
                    pl.col(col).fill_null("Missing").alias(col)
                )

            return df

        self.train_data = clean(self.train_data)
        self.test_data = clean(self.test_data)



    def prepare_features(self, target_column: str = "SalePrice",
                         selected_predictors: List[str] = None):
        X = self.train_data.drop(target_column)
        y = self.train_data[target_column]

        if selected_predictors:
            X = X.select(selected_predictors)

        #Split Numeric and Categorical Features
        numeric_features = X.select(pl.col(pl.Float64),
                                    pl.col(pl.Int64)).columns
        categorical_features = X.select(pl.col(pl.Utf8)).columns

        #Preprocessing Pipeline (Numeric)
        numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler())
        ])

        #Preprocessing Pipeline (Categorical)
        categorical_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="constant",
                                      fill_value="Missing1")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ])

        #combine both
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features)
            ]
        )

        X_train, X_test, y_train, y_test = train_test_split(X.to_pandas(),                                            #!
                                                            y.to_pandas(),
                                                            test_size=0.2,
                                                            random_state=42)

        return X_train, X_test, y_train, y_test



    def train_baseline_models(self) -> Dict[str, Dict[str, float]]:
        X_train, X_test, y_train, y_test = self.prepare_features()

        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(random_state=42)
        }

        results = {}

        for model_name, model in models.items():
            pipeline = Pipeline(steps=[("preprocessor", self.preprocessor), ("model", model)])
            pipeline.fit(X_train, y_train)
            self.models[model_name] = pipeline

            y_train_pred = pipeline.predict(X_train)
            y_test_pred = pipeline.predict(X_test)

            results[model_name] = {
                "metrics": {
                    "MSE": mean_squared_error(y_test, y_test_pred),
                    "MAE": mean_absolute_error(y_test, y_test_pred),
                    "R2": r2_score(y_test, y_test_pred),
                    "MAPE": mean_absolute_percentage_error(y_test, y_test_pred)
                },
                "model": pipeline
            }

        return results



    def forecast_sales_price(self, model_type: str = "Linear Regression"):
        #model_type
        if model_type not in self.models:
            raise ValueError(f"Model type {model_type} is not trained. Available models: {list(self.models.keys())}")

        #Preprocessing
        pipeline = self.models[model_type]

        #Generate Predictions
        predictions = pipeline.predict(self.test_data.to_pandas())                                                    #!



        #Create a Submission pl.DataFrame
        submission = pl.DataFrame({
            "Id": self.test_data["Id"],
            "SalePrice": predictions
        })

        #Save the File
        output_dir = "src/real_estate_toolkit/ml_models/outputs/"
        os.makedirs(output_dir, exist_ok=True)
        submission_path = os.path.join(output_dir, "submission.csv")
        submission.write_csv(submission_path)


        return submission_path


