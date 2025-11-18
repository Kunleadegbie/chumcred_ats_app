import pandas as pd

def export_results_to_excel(df, output_path):
    """
    Save final ATS results.
    """
    df.to_excel(output_path, index=False)
