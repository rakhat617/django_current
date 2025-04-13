from django.urls import path

from comments.views import CommentsView


urlpatterns = [
    path(route="", view=CommentsView.as_view(), name="comments")
]

# ДЕЛАЕМ РОУТИНГ ДЛЯ КОММЕНТОВ, 
# ХОТЯ НЕ ЗНАЮ ЗАЧЕМ, ИБО КОММЕНТЫ ЖЕ ВМЕСТЕ С ПОСТАМИ ДОЛЖНЫ ОТОБРАЖАТЬСЯ
# НО ПО-ДРУГОМУ НЕ ПОНИМАЮ КАК "ЗАРЕГИСТРИРОВАТЬ КОНТРОЛЛЕР"