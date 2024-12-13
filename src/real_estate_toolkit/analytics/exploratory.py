from typing import List, Dict
import polars as pl
import plotly.express as px # type: ignore
import plotly.graph_objects as go # type: ignore

class MarketAnalyzer:
    def __init__(self, data_path: str):
        """
        Initialize the analyzer with data from a CSV file.
        
        Args:
            data_path (str): Path to the Ames Housing dataset
        """
        self.data_path = data_path
        self.real_state_data = pl.read_csv(data_path, null_values="NA")
        self.real_state_clean_data = None
    
    def clean_data(self) -> None:
        """
        Perform comprehensive data cleaning:
        
        Tasks to implement:
        1. Identify and handle missing values
            - Decide strategy for each column (drop, fill with mean/median, no change)
        2. Convert columns to appropriate data types if needed.
            - Ensure numeric columns are numeric
            - Ensure categorical columns are categorized
        
        Returns:
            Cleaned and preprocessed dataset assigned to self.real_state_clean_data
        """
        df = self.real_state_data
        
       
        
        
        # Convert columns to appropriate data types
        for column in df.columns:
            if df[column].dtype == pl.Utf8:
                df = df.with_columns([pl.col(column).cast(pl.Categorical)])
            elif df[column].dtype == pl.Float64 or df[column].dtype == pl.Int64:
                df = df.with_columns([pl.col(column).cast(pl.Float64)])
        
        df = df.fill_null(strategy="mean")
        self.real_state_clean_data = df
    
    def generate_price_distribution_analysis(self) -> pl.DataFrame:
        """
        Analyze sale price distribution using clean data.
        
        Tasks to implement:
        1. Compute basic price statistics and generate another data frame called price_statistics:
            - Mean
            - Median
            - Standard deviation
            - Minimum and maximum prices
        2. Create an interactive histogram of sale prices using Plotly.
        
        Returns:
            - Statistical insights dataframe
            - Save Plotly figures for price distribution in src/real_estate_toolkit/analytics/outputs/ folder.
        """
        if self.real_state_clean_data is None:
            raise ValueError("Cleaned data is not available. Please run clean_data() first.")
        df = self.real_state_clean_data
        price_statistics = df.select([
            pl.col("SalePrice").mean().alias("mean"),
            pl.col("SalePrice").median().alias("median"),
            pl.col("SalePrice").std().alias("std_dev"),
            pl.col("SalePrice").min().alias("min"),
            pl.col("SalePrice").max().alias("max")
        ])
        
        fig = px.histogram(df.to_pandas(), x="SalePrice", title="Sale Price Distribution")
        fig.write_html("src/real_estate_toolkit/analytics/outputs/sale_price_distribution.html")
        
        return price_statistics
    
    def neighborhood_price_comparison(self) -> pl.DataFrame:
        """
        Create a boxplot comparing house prices across different neighborhoods.
        
        Tasks to implement:
        1. Group data by neighborhood
        2. Calculate price statistics for each neighborhood
        3. Create Plotly boxplot with:
            - Median prices
            - Price spread
            - Outliers
        
        Returns:
            - Return neighborhood statistics dataframe
            - Save Plotly figures for neighborhood price comparison in src/real_estate_toolkit/analytics/outputs/ folder.
        """
        if self.real_state_clean_data is None:
            raise ValueError("Cleaned data is not available. Please run clean_data() first.")

        df = self.real_state_clean_data
       
        neighborhood_stats = df.groupby("Neighborhood") .agg([ 
            pl.col("SalePrice").median().alias("median_price"),
            pl.col("SalePrice").mean().alias("mean_price"),
            pl.col("SalePrice").std().alias("std_dev_price"),
            pl.col("SalePrice").min().alias("min_price"),
            pl.col("SalePrice").max().alias("max_price")
        ])
    
        fig = px.box(df.to_pandas(), x="Neighborhood", y="SalePrice", title="Neighborhood Price Comparison")
        fig.write_html("src/real_estate_toolkit/analytics/outputs/neighborhood_price_comparison.html")
        
        return neighborhood_stats # type: ignore
    
    def feature_correlation_heatmap(self, variables: List[str]) -> None:
        """
        Generate a correlation heatmap for variables input.
        
        Tasks to implement:
        1. Pass a list of numerical variables
        2. Compute correlation matrix and plot it
        
        Args:
            variables (List[str]): List of variables to correlate
        
        Returns:
            Save Plotly figures for correlation heatmap in src/real_estate_toolkit/analytics/outputs/ folder.
        """
        if self.real_state_clean_data is None:
            raise ValueError("Cleaned data is not available. Please run clean_data() first.")
        df = self.real_state_clean_data.select(variables)
        correlation_matrix = df.to_pandas().corr()
        
        fig = px.imshow(correlation_matrix, text_auto=True, title="Correlation Heatmap")
        fig.write_html("src/real_estate_toolkit/analytics/outputs/correlation_heatmap.html")
    
    def create_scatter_plots(self) -> Dict[str, go.Figure]:
        """
        Create scatter plots exploring relationships between key features.
        
        Scatter plots to create:
        1. House price vs. Total square footage
        2. Sale price vs. Year built
        3. Overall quality vs. Sale price
        
        Tasks to implement:
        - Use Plotly Express for creating scatter plots
        - Add trend lines
        - Include hover information
        - Color-code points based on a categorical variable
        - Save them in src/real_estate_toolkit/analytics/outputs/ folder.
        
        Returns:
            Dictionary of Plotly Figure objects for different scatter plots. 
        """
        if self.real_state_clean_data is None:
            raise ValueError("Cleaned data is not available. Please run clean_data() first.")
        df = self.real_state_clean_data.to_pandas()
        figures = {}
        
        fig1 = px.scatter(df, x="GrLivArea", y="SalePrice", trendline="ols", title="House Price vs. Total Square Footage")
        fig1.write_html("src/real_estate_toolkit/analytics/outputs/price_vs_square_footage.html")
        figures["price_vs_square_footage"] = fig1
        
        fig2 = px.scatter(df, x="YearBuilt", y="SalePrice", trendline="ols", title="Sale Price vs. Year Built")
        fig2.write_html("src/real_estate_toolkit/analytics/outputs/price_vs_year_built.html")
        figures["price_vs_year_built"] = fig2
        
        fig3 = px.scatter(df, x="OverallQual", y="SalePrice", trendline="ols", title="Overall Quality vs. Sale Price")
        fig3.write_html("src/real_estate_toolkit/analytics/outputs/quality_vs_price.html")
        figures["quality_vs_price"] = fig3
        
        return figures # type: ignore