from django.contrib import admin
from .models import Article, Book, Chapter, Endnote, Quote, Source, Webpage


# Register your models here.
admin.site.register(Article)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Endnote)
admin.site.register(Quote)
admin.site.register(Source)
admin.site.register(Webpage)
