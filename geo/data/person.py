from django.db import models


# ----------------------------------
# люди


class Person(models.Model):

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['id']