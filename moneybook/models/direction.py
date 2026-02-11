from django.db import models


class Direction(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    @staticmethod
    def get(pk):
        return Direction.objects.get(pk=pk)

    @staticmethod
    def list():
        return Direction.objects.order_by('pk')
