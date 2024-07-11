from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Expense(models.Model):
    amount = models.FloatField()
    date=models.DateField(default=now)
    description=models.TextField()
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    category=models.CharField(max_length=256)
    
    def __str__(self):
        return f'{self.amount} - {self.description}'
    
    class Meta:
        ordering: ['-date']
    
class Category(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'

class Income(models.Model):
    amount = models.FloatField()
    date=models.DateField(default=now)
    description=models.TextField()
    owner = models.ForeignKey(to=User,on_delete=models.CASCADE)
    source=models.CharField(max_length=256)
    
    def __str__(self):
        return f'{self.amount} - {self.description}'
    
    class Meta:
        ordering: ['-date']
    
class Source(models.Model):
    name=models.CharField(max_length=255)
    class Meta:
        verbose_name_plural = 'Sources'
        
class UserPreferences(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency=models.CharField(max_length=255, blank=True,null=True)
    def __str__(self):
        return f"{self.currency}'s preferences"