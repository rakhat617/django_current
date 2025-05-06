from django.db import models
from django.db import models
from django.utils import timezone

from clients.models import Client
from posts.models import Posts

# Create your models here.

class Comments(models.Model):
    user = models.ForeignKey( # ПОЛЕ ДЛЯ АВТОРА. СКОПИРОВАЛ С ПОСТС  
        to=Client,
        verbose_name="автор",
        on_delete=models.SET_DEFAULT,
        default="Unknown author",
        related_name="comment_author",
    )
    text = models.TextField( # ПОЛЕ ДЛЯ ТЕКСТА
        verbose_name="Текст комментария",
        max_length=5000,
    )
    date_publication = models.DateTimeField( # ПОЛЕ ДЛЯ ДАТЫ ПУБЛИКАЦИИ, СКОПИРОВАЛ С ПОСТС
        verbose_name="дата публикации",
        default=timezone.now,
    )
    likes = models.PositiveBigIntegerField( # ПОЛЕ ДЛЯ ЛАЙКОВ, СКОПИРОВАЛ С ПОСТС
        verbose_name="лайки",
        default=0,
    )
    dislikes = models.PositiveBigIntegerField( # ПОЛЕ ДЛЯ ДИЗЛАЙКОВ, СКОПИРОВАЛ С ПОСТС
        verbose_name="дизлайки",
        default=0,
    )
    post = models.ForeignKey( # ЭТОГО НЕ БЫЛО В ЗАДАНИИ, НО Я ПОДУМАЛ ЧТО ЭТО НУЖНО, 
                            # ПОТОМУ ЧТО ИНАЧЕ КАК ОН ПОЙМЕТ ПОД КАКОЙ ПОСТ КОММЕНТ ПРИВЯЗЫВАТЬ
        to=Posts,
        verbose_name="родительский пост",
        on_delete=models.CASCADE,
        related_name="parent_post"
    )
    parent_comment = models.ForeignKey( # ЭТО ВОТ ДЛЯ ТОГО ЧТОБЫ НАШ КОММЕНТАРИЙ МОГ БЫТЬ ОТВЕТОМ К ДРУГОМУ КОММЕНТАРИЮ
                                        # ПО СУТИ ТУТ ТАКАЯ ЖЕ ЛОГИКА КАК И В ПОЛЕ ВЫШЕ, 
                                        # ТОЛЬКО ТАМ МЫ К ПОСТУ ПРИВЯЗЫВАЕМ, А ТУТ МЫ ЕЩЕ И К ДРУГОМУ КОММЕНТУ ПРИВЯЗЫВАЕМ
                                        # НО Я НЕ УВЕРЕН БУДЕТ ЛИ ЭТО РАБОТАТЬ, ПОТОМУ ЧТО ТУТ РЕКУРСИЯ, И Я ХЗ ПРАВИЛЬНО ЛИ Я ЕЕ СДЕЛАЛ
        to='self', # self БЕЗ КОВЫЧЕК КАК ОШИБКА ПОДЧЕРКИВАЛСЯ, И МНЕ ГПТ СКАЗАЛ ЧТО НУЖНЫ КОВЫЧКИ, НО ЧТО-ТО ЭТО ПОДОЗРИТЕЛЬНО
        verbose_name="родительский комментарий",
        null=True, # ЕСЛИ ЭТО ПОЛЕ НУЛЛ, ЗНАЧИТ У КОММЕНТА НЕТ РОДИТЕЛЬСКОГО КОММЕНТА, ТО ЕСТЬ ЭТО ПРЯМОЙ КОММЕНТАРИЙ К ПОСТУ
        blank=True, # БЛАНК ТРУ НА ВСЯКИЙ СЛУЧАЙ ТОЖЕ ДОБАВИЛ
        on_delete=models.CASCADE,
        related_name="reply_to_comment",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"