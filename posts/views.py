import logging

from django.views import View
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
from django.db.models.query import QuerySet

from posts.models import Posts, Images, Categories, Reactions


logger = logging.getLogger()

class BasePostView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        posts: QuerySet[Posts] = Posts.objects.all()
        return render(
            request=request, template_name="posts.html", 
            context={
                "posts": posts,
                "user": is_active
            }
        )


class PostsView(View):
    """Posts controller with all methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        categories = Categories.objects.all()
        if not categories:
            return HttpResponse(
                content="<h1>Something went wrong</h1>"
            )
        if not is_active:
            return redirect(to="login")
        return render(
            request=request, template_name="post_form.html",
            context={"categories": categories}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        images = request.FILES.getlist("images")
        post = Posts.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
        post.categories.set(request.POST.getlist("categories"))
        imgs = [Images(image=img, post=post) for img in images]
        # for img in images:
        #     Images.objects.create(
        #         image=img,
        #         post=post
        #     )
        Images.objects.bulk_create(imgs)
        return redirect(to="base")
        

class ShowDeletePostView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist as e:
            post = None
        author = False
        if request.user == post.user:
            author = True
        return render(request=request, template_name="pk_post.html", context={"post": post, "author": author})

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            pass
        if request.user != post.user:
            return HttpResponse(
                "<h1>You have no power</h1>"
            )
        post.delete()
        return redirect(to="base")

class ReactionView(View): # ЭТО ВЬЮШКА ЧИСТО ПОД ЛАЙКИ ДИЗЛАЙКИ. СНАЧАЛА Я ДЕЛАЛ ОТДЕЛЬНЫЕ ВЬЮШКИ И ДЛЯ ЛАЙКОВ И ДЛЯ ДИЗЛАЙКОВ,
    # ПОТОМУ ЧТО И ДЛЯ КНОПОК ДЕЛАЛ ОТДЕЛЬНЫЕ ФОРМЫ. НО ПОТОМ КАК ДОДУМАЛСЯ ЧТО МОЖНО СДЕЛАТЬ 
    # В ОДНОЙ ФОРМЕ И ПРОСТО ПЕРЕДАТЬ РАЗНЫЕ ЗНАЧЕНИЯ ЧЕРЕЗ КНОПКИ ЖЕЕЕЕЕСТЬ КАК Я ПОУМНЕЛ ТУПА 5HEAD 
    def post(self, request: HttpRequest, pk: int) -> HttpResponse: # ПО СУТИ ТУТ НАМ ГЕТ НЕ НУЖЕН, ТОЛЬКО ПОСТ
        user = request.user # СОХРАНЯЕМ ЮЗЕРА В ПЕРЕМЕННУЮ, ПОТОМ НАДО БУДЕТ
        if user.is_active: # ВОТ ЭТА ШТУКА ВАЖНА, ТОЛЬКО В КОНЦЕ ПОНЯЛ, КОГДА СЛУЧАЙНО НЕЗАЛОГИНИВШИСЬ НАЖАЛ НА ЛАЙК. 
            # КАРОЧ, ЕСЛИ ЮЗЕРА НЕТ АКТИВНОГО, ТОГДА ВООБЩЕ НИЧЕГО НЕ ПРОИСХОДИТ, ПРОСТО СТРАНИЦА ПЕРЕЗАГРУЖАЕТСЯ
            post = Posts.objects.get(pk=pk) # НУ ЭТО КАК И В ПРЕДЫДУЩЕЙ ВЬЮШКЕ, ПРОСТО ПОЛУЧАЕМ ЦЕЛИКОМ ПОСТ ИЗ ДАТАБАЗЫ С КОТОРЫМ РАБОТАЕМ
            reaction = request.POST.get('reaction') # А ВОТ ЭТО УЖЕ МЫ ЗАБИРАЕМ ЗНАЧЕНИЯ КОТОРОЕ ПЕРЕДАЛИ С ПОМОЩЬЮ КНОПКИ, ЧЕРЕЗ ТЕГ БАТТОН В ХТМЛКЕ.
            # У НАС ВСЕГО ДВЕ КНОПКИ, КОТОРЫЕ ПЕРЕДАЮТ СООТВЕТСТВЕННО 2 ЗНАЧЕНИЯ - СТРОКУ 'LIKE' ИЛИ СТРОКУ 'DISLIKE'
            existing_reaction = Reactions.objects.filter(user=user, post=post).first() # ТУТ МЫ ПРОВЕРЯЕМ СТАВИЛ ЛИ ЭТОТ ЮЗЕР ЭТОМУ ПОСТУ УЖЕ КАКУЮ-ТО РЕАКЦИЮ
            if existing_reaction is None: # ЕСЛИ НЕ СТАВИЛ, СРАБАТЫВАЕТ ЭТОТ ИФ
                if reaction == 'like': # ЕСЛИ ОН НАЖАЛ НА ЛАЙК, ТОГДА ДОБАВЛЯЕМ +1 К ЛАЙКАМ В ТАБЛИЦЕ ПОСТОВ В ДАТАБАЗЕ
                    post.likes += 1
                elif reaction == 'dislike': # НУ И СООТВЕТСВЕННО ЕСЛИ НА ДИЗЛАЙК, ТОГДА +1 К ДИЗАМ В ТАБЛИЦЕ
                    post.dislikes += 1
                Reactions.objects.create( # А ТАКЖЕ НУЖНО СОЗДАТЬ НОВУЮ ЗАПИСЬ ДЛЯ ЭТОЙ РЕАКЦИИ В ТАБЛИЦЕ РЕАКЦИЙ. ЧТОБЫ В СЛЕД РАЗ ЭТОТ ИФ УЖЕ НЕ СРАБОТАЛ
                    user = user,
                    post = post,
                    reaction = reaction
                )
            elif existing_reaction.reaction != reaction: # ЕСЛИ ПЕРВЫЙ ИФ НЕ СРАБОТАЛ, ЗНАЧИТ ЮЗЕР УЖЕ РЕАГИРОВАЛ. ПОСЛЕ ЭТОГО ЧЕКАЕТСЯ ЭТО УСЛОВИЕ
            # ЭТОТ ИФ СРАБОТАЕТ ЕСЛИ ЮЗЕР НАЖАЛ НА КНОПКУ, КОТОРАЯ НЕ СООТВЕТСТВУЕТ ЕГО ПРЕДЫДУЩЕЙ РЕАКЦИИ, СОХРАНЕННОЙ В ТАБЛИЦЕ. 
            # НУ И ОЧЕВИДНО ЗАЧЕМ ЭТО НУЖНО: ЧТОБЫ ЮЗЕР МОГ ПОМЕНЯТЬ ЛАЙК НА ДИЗЛАЙК И НАОБОРОТ
                if reaction == 'like': # ТУТ МЕНЯЕТСЯ СЧЕТЧИКИ В ТАБЛИЦЕ ПОСТОВ, В ЗАВИСИМОСТИ ОТ ТОГО ЧТО НА ЧТО МЕНЯЕМ
                    post.likes += 1
                    post.dislikes -= 1
                elif reaction == 'dislike':
                    post.dislikes += 1
                    post.likes -= 1
                existing_reaction.reaction = reaction # ЗДЕСЬ ОБНОВЛЯЕМ РЕАКЦИЮ В ДАТАБАЗЕ
                existing_reaction.save() # СОХРАНЯЕМ ИЗМЕНЕНИЕ В ДАТАБАЗУ
            elif existing_reaction.reaction == reaction: # И НАКОНЕЦ ЕСЛИ ЮЗЕР НАЖИМАЕТ НА РЕАКЦИЮ, КОТОРАЯ УЖЕ У НЕГО СТОИТ, ТО ОНА ОТМЕНЯЕТСЯ
                if reaction == 'like': # УМЕНЬШАЕМ СЧЕТЧИК
                    post.likes -= 1
                elif reaction == 'dislike':
                    post.dislikes -= 1
                existing_reaction.delete() # УДАЛЯЕМ ЭТУ РЕАКЦИЮ ИЗ ТАБЛИЦЫ
            post.save() # СОХРАНЯЕМ ИЗМЕНЕНИЕ СЧЕТЧИКОВ В ДАТАБАЗУ
        return redirect(to="base") # ВОЗВРАЩАЕМСЯ НА ГЛАВНУЮ СТРАНИЦУ. 
    # ЕЩЕ КСТАТИ НУЖНО БЫЛО СДЕЛАТЬ ЧТОБЫ СО СТРАНИЦЫ САМОГО ПОСТА МОЖНО БЫЛО ВСЕ ЭТО ДЕЛАТЬ, НО ЧЕТО МНЕ ЛЕНЬ УЖЕ НАД ЭТИМ ПАРИТЬСЯ