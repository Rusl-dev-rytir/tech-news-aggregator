from django.db import models

class News(models.Model):
    source = models.CharField(max_length=100)      # Откуда новость (CNN, Lenta, Habr)
    title = models.CharField(max_length=200)       # Заголовок
    link = models.URLField(unique=True)            # Ссылка (unique=True, чтобы не было дублей)
    pub_date = models.CharField(max_length=100)    # Дата
    image_url = models.URLField(blank=True, null=True) # Ссылка на картинку (может быть пустой)
    description = models.TextField(blank=True)     # Краткое описание (TextField - для длинного текста)

    def __str__(self):
        return f"{self.source}: {self.title}"