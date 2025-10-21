# coding=utf-8

from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=200)  
    author = models.CharField(max_length=100)
    pub_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.author}"