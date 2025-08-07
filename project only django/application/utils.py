import pandas as pd
import sys
from rapidfuzz import fuzz
def comparaison_processe(path1, path2, threshold=80):
    result = []

    #extraction de l'extention
    def extension(path):
        return path.split(".")[-1].lower()

    ext1 = extension(path1)
    ext2 = extension(path2)
    #s'assurer que les deux fichier on les memes extensions
    if ext1 != ext2:
        return ["Files have different extensions. Comparison aborted."]
    #recuperer les fichier à comparer
    try:
        df1 = pd.read_csv(path1)
        df2 = pd.read_csv(path2)
    except Exception as e:
        return [f"Error reading CSV files: {str(e)}"]

    #procedure de comparaison
    for i in range(max(len(df1), len(df2))):
        # Get rows (handle cases where DataFrames have different lengths)
        row_file1 = df1.iloc[i].tolist()
        row_file2 = df2.iloc[i].tolist()
            
        # Convert rows to comparable strings
        concat_row1 = ';'.join(str(cell) for cell in row_file1)
        concat_row2 = ';'.join(str(cell) for cell in row_file2)
            
        # Separate back to original components
        separated_row1 = concat_row1.split(';')
        separated_row2 = concat_row2.split(';')
            
        # Calculate similarity
        comp_level = fuzz.token_sort_ratio(concat_row1, concat_row2)
        
    
    # Create DataFrame from results
    df3 = pd.DataFrame(result)
            
    return result
