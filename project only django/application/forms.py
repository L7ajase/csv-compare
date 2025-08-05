from django import forms

class FileUploadForm(forms.Form):
    file1 =  forms.FileField(label="First file")
    file2 =  forms.FileField(label="Second file")