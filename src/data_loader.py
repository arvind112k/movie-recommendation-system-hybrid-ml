# src/data_loader.py

import pandas as pd
import os
import sys
from src.logger import logging
from src.exception import CustomException

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load TMDB movie dataset from a CSV file and perform initial cleaning.
    """
    try:
        logging.info(f"Reading data from: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at path: {file_path}")
        
        df = pd.read_csv(file_path)
        logging.info(f"Data loaded successfully. Initial shape: {df.shape}")

        # Drop rows with nulls in important fields
        df.dropna(subset=['title', 'genre', 'overview', 'release_date'], inplace=True)

        # Convert release_date to datetime format
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        df.dropna(subset=['release_date'], inplace=True)

        # Convert genre and original_language to lowercase
        df['genre'] = df['genre'].str.lower()
        df['original_language'] = df['original_language'].str.lower()

        logging.info(f"Data cleaned. Final shape: {df.shape}")
        return df

    except Exception as e:
        logging.error(f"Exception occurred during data loading: {str(e)}")
        raise CustomException(e, sys)