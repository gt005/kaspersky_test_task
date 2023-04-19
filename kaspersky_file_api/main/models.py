from django.db import models


class Search(models.Model):
    tag = models.CharField(max_length=255, unique=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Search object'
        verbose_name_plural = 'Search objects'


class Path(models.Model):
    search = models.ForeignKey(
        Search,
        on_delete=models.CASCADE,
        related_name='paths'
    )
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.path

    class Meta:
        verbose_name = 'Path'
        verbose_name_plural = 'Paths'
