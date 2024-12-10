from django.db import models

class Studio(models.Model):
    name = models.TextField("Название")
    
    class Meta:
        verbose_name = "Студия"
        verbose_name_plural = "Студии"
    def __str__(self) -> str:
        return self.name
    

class Genre (models.Model):
    name = models.TextField("Название")
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
    def __str__(self) -> str:
        return self.name
    

class Director(models.Model):
    name = models.TextField("Имя")
    surname = models.TextField("Фамилия")
    picture = models.ImageField("Картинка", upload_to="directors", null=True, blank=True)

    class Meta:
        verbose_name = "Руководитель"
        verbose_name_plural = "Руководители"

    def __str__(self):
        return self.name

    


class Platform (models.Model):
    name = models.TextField("Название")

    class Meta:
        verbose_name = "Платформа"
        verbose_name_plural = "Платформы"
    def __str__(self) -> str:
        return self.name


# Create your models here.
class Games (models.Model):
    name = models.TextField("Название")
    
    studio = models.ForeignKey("Studio", on_delete=models.CASCADE, null=True)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE, null=True)
    director = models.ForeignKey("Director", on_delete=models.CASCADE, null=True)
    platform = models.ForeignKey("Platform", on_delete=models.CASCADE, null=True)

    picture = models.ImageField("Картинка",upload_to="games", null=True)


    class Meta:
        verbose_name ="Игра"
        verbose_name_plural = "Игры"

