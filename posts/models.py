from django.db import models
from django.utils import timezone

from clients.models import Client

class Categories(models.Model):
    title = models.CharField(
        verbose_name="название категории",
        max_length=50,
    )
    class Meta:
        ordering = ("id",)
        verbose_name = "категория"
        verbose_name_plural = "категории"
    
    def __str__(self):
        return f"{self.pk} | {self.title}"

class Posts(models.Model):
    title = models.CharField(
        verbose_name="Название поста",
        max_length=200,
    )
    description = models.TextField(
        verbose_name="Описание",
        max_length=5000,
    )
    date_publication = models.DateTimeField(
        verbose_name="дата публикации",
        default=timezone.now,
    )
    user = models.ForeignKey(
        to=Client,
        verbose_name="автор",
        on_delete=models.SET_DEFAULT,
        default="Unknown author",
        related_name="client_posts",
    )
    likes = models.PositiveBigIntegerField(
        verbose_name="лайки",
        default=0,
    )
    dislikes = models.PositiveBigIntegerField(
        verbose_name="дизлайки",
        default=0,
    )
    categories = models.ManyToManyField(
        to=Categories,
        verbose_name="категории поста",
        related_name="post_categories",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "пост"
        verbose_name_plural = "посты"

    def __str__(self):
        return f"{self.title} | {self.date_publication}"


class Images(models.Model):
    image = models.ImageField(
        verbose_name="изображение",
        upload_to="images/posts/",
    )
    post = models.ForeignKey(
        to=Posts, 
        on_delete=models.CASCADE,
        related_name="post_images",
        verbose_name="статья",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self):
        return f"{self.pk} | {self.image}"
    

class Reactions(models.Model): # НОВАЯ МОДЕЛЬКА, СПЕЦИАЛЬНО ДЛЯ РЕАКЦИЙ. ДОЛГО Я ДУМАЛ ДУМАЛ, И ПРИШЕЛ К ВЫВОДУ ЧТО БЕЗ НЕЕ НИКУДА
        # ЭТО ПО СУТИ СВЯЗУЮЩАЯ ТАБЛИЦА МЕЖДУ ПОСТАМИ И ЮЗЕРАМИ, КАК ТИПА КОГДА ДЕЛАЕШЬ МЭНИ ТУ МЭНИ СВЯЗЬ
        # НО В ДЖАНГО ПРИ МЭНИ ТУ МЭНИ ТРЕТЬЯ ТАБЛИЦА НЕ ОБЯЗАТЕЛЬНА, ПОТОМУ ЧТО МОЖНО МЭНИ ТУ МЭНИ ФИЛД ПРОПИСАТЬ
        # НО ТУТ ДЕЛО НЕ В МЭНИ ТУ МЭНИ СВЯЗИ, А В ТОМ ЧТО МНЕ КОНКРЕТНО НУЖНА ЭТА ОТДЕЛЬНАЯ ТАБЛИЦА, ГДЕ БУДЕТ ЕЩЕ ОДНО ПОЛЕ
        # КОТОРОЕ БУДЕТ ХРАНИТЬ РЕАКЦИЮ: ЛАЙК ИЛИ ДИЗЛАЙК. 
        # НУ И ЕЩЕ С ОТДЕЛЬНОЙ ТАБЛИЦЕЙ КУДА ЛЕГЧЕ РАБОТАТЬ. ТИПА ПРОВЕРЯТЬ ПОСТАВИЛ ЛИ ЧЕЛ УЖЕ ЛАЙК ДИЗЛАЙК
        # НУ ТУТ ВСЕ ПОНЯТНО ДУМАЮ ПО ЭТОЙ МОДЕЛИ. ПРОСТО ДВА ФОРЭЙН (НЕ ФОРИДЖН, ФОРЭЙН) КЕЯ, И САМО ПОЛЕ С РЕАКЦИЕЙ
    user = models.ForeignKey(
        to=Client,
        verbose_name="реактор",
        on_delete=models.CASCADE,
        related_name="client_reactions",
    )
    post = models.ForeignKey(
        to=Posts, 
        on_delete=models.CASCADE,
        related_name="post_reactions",
        verbose_name="статья",
    )
    reaction = models.CharField(
        verbose_name="реакция юзера",
        max_length=10,
    )