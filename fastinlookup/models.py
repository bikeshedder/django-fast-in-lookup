from django.db import models


class Item(models.Model):
    name = models.CharField(unique=True, max_length=20)
    fk = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
