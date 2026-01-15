from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField() # Hum Email ko Unique mankar check karenge
    address = models.TextField()
    date_joined = models.DateTimeField(auto_now_add=True)
    is_online = models.BooleanField(default=False)
    
    # YE NAYI LINE ADD KARO (Sorting ke liye)
    # auto_now=True ka matlab jab bhi save() hoga, ye time update ho jayega
    last_active = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name