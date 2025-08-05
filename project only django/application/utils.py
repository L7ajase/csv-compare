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
    if len(df1.columns) != len(df2.columns):
        result.append("Files have a different number of columns.")
        if len(df1.columns) < len(df2.columns):
            result.append("First file has fewer columns.")
        else:
            result.append("Second file has fewer columns.")
    else:
        for i in range(max(len(df1), len(df2))):
            # Get rows (handle cases where DataFrames have different lengths)
            try:
                row_file1 = df1.iloc[i].tolist()
            except IndexError:
                row_file1 = ["MISSING"] * len(df1.columns) if len(df1.columns) > 0 else [""]
                
            try:
                row_file2 = df2.iloc[i].tolist()
            except IndexError:
                row_file2 = ["MISSING"] * len(df2.columns) if len(df2.columns) > 0 else [""]
            
            # Convert rows to comparable strings
            concat_row1 = ';'.join(str(cell) for cell in row_file1)
            concat_row2 = ';'.join(str(cell) for cell in row_file2)
            
            # Separate back to original components
        separated_row1 = concat_row1.split(';')
        separated_row2 = concat_row2.split(';')
        
        # Calculate similarity
        comp_level = fuzz.token_sort_ratio(concat_row1, concat_row2)
        
        # Create result dictionary
        result = {
            'Row_Index': i,
            'Similarity_Score': comp_level,
            'Match_Status': 'Match' if comp_level >= threshold else 'No Match'
        }
        
        # Add separated values for df1
        for col_idx, value in enumerate(separated_row1):
            result[f'DF1_Col{col_idx}'] = value
            
        # Add separated values for df2
        for col_idx, value in enumerate(separated_row2):
            result[f'DF2_Col{col_idx}'] = value
        
        result.append(result)
    
    # Create DataFrame from results
    df3 = pd.DataFrame(result)
    
    # Reorder columns for better readability
    cols = ['Row_Index', 'Similarity_Score', 'Match_Status']
    cols += [f'DF1_Col{i}' for i in range(len(df1.columns))] if len(df1.columns) > 0 else []
    cols += [f'DF2_Col{i}' for i in range(len(df2.columns))] if len(df2.columns) > 0 else []
    
    result.append(df3[cols])
            
    return result