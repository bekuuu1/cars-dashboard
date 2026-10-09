"""
Data loader module for CarScope.
Handles defensive reading of CSV data from file upload or local disk paths,
returning raw DataFrames and dataset metadata.
"""

from typing import Tuple, Dict, Any, Union
import pandas as pd
import io


def load_dataset(file_source: Union[str, io.BytesIO, Any]) -> Tuple[pd.DataFrame, str]:
    """
    Safely load CSV data from a file path or Streamlit UploadedFile object.
    Supports encoding fallbacks (utf-8, latin1, cp1252) and delimiter detection.

    Returns:
        Tuple of (df: pd.DataFrame, dataset_name: str)
    """
    dataset_name = "Uploaded Dataset"
    if isinstance(file_source, str):
        dataset_name = file_source.split("/")[-1]

    encodings = ["utf-8", "latin1", "cp1252"]

    for encoding in encodings:
        try:
            if hasattr(file_source, "seek"):
                file_source.seek(0)
                if hasattr(file_source, "name"):
                    dataset_name = file_source.name

            df = pd.read_csv(file_source, encoding=encoding)
            
            # Trim whitespace from raw column names
            df.columns = [str(col).strip() for col in df.columns]

            if df.empty:
                raise ValueError("The uploaded CSV file is empty.")

            return df, dataset_name
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")

    raise ValueError("Failed to parse CSV file with supported encodings (UTF-8, Latin1, CP1252).")


def get_dataset_metadata(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate summary metadata for a loaded DataFrame.
    """
    total_rows, total_cols = df.shape
    total_cells = total_rows * total_cols
    missing_cells = df.isna().sum().sum()
    missing_pct = (missing_cells / total_cells * 100) if total_cells > 0 else 0.0
    memory_usage_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    return {
        "rows": total_rows,
        "columns": total_cols,
        "total_cells": total_cells,
        "missing_cells": missing_cells,
        "missing_percentage": round(missing_pct, 1),
        "memory_mb": round(memory_usage_mb, 2),
        "dtypes": df.dtypes.to_dict(),
        "null_counts": df.isna().sum().to_dict(),
    }
