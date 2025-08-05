import pandas as pd
import tempfile
import os
from django.shortcuts import render
from .forms import FileUploadForm
from .utils import comparaison_processe 
# Create your views here.

def compare_files_view(request):
    result = None
    table1 = None 
    table2 = None
    file1_name = None
    file2_name = None

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES['file1']
            file2 = request.FILES['file2']

            file1_name = file1.name
            file2_name = file2.name

            tmp1_path = None
            tmp2_path = None

        try:
            # create temporary files and write content
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp1:
                for chunk in file1.chunks():
                    tmp1.write(chunk)
                tmp1_path = tmp1.name

            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp2:
                for chunk in file2.chunks():
                    tmp2.write(chunk)
                tmp2_path = tmp2.name
                
                
            #read the files with pandas
            df1 = pd.read_csv(tmp1_path)
            df2 = pd.read_csv(tmp2_path)

            # Convertir en HTML ou liste pour affichage
            table1 = df1.to_html(classes='table table-striped', index=False, escape=False)
            table2 = df2.to_html(classes='table table-striped', index=False, escape=False)
                 
            #compare the files
            result = comparaison_processe(tmp1_path, tmp2_path)

        except pd.errors.EmptyDataError:
            result = ["Erreur: Un des fichiers CSV est vide"]
        except pd.errors.ParserError as e:
            result = [f"Erreur lors de l'analyse du CSV: {str(e)}"]
        except Exception as e:
            result = [f"Erreur lors de la lecture des fichiers CSV: {str(e)}"]         

        finally:
            #clean up the temporary files
            for temp_path in [tmp1_path, tmp2_path]:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)       

    else:
        form = FileUploadForm()
   
    return render(request, 'application/compare.html', {
        'form': form, 
        'result': result,
        'table1': table1,
        'table2': table2,
        'file1_name': file1_name,
        'file2_name': file2_name
        })