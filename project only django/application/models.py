from django.db import models

# Create your models here.
class path_input(models.Model):
    path_input1=models.CharField(max_length=250)
    path_input2=models.CharField(max_length=250)
    upload_date=models.DateTimeField("date uploaded")
    def __str__(self):
            return f"{self.path_input1} | {self.path_input2} | {self.upload_date.strftime('%d-%m-%Y %H-%M-%S')}"
          