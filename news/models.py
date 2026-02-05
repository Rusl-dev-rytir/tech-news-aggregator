from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    source = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    link = models.URLField(unique=True)
    pub_date = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return f"{self.source}: {self.title}"