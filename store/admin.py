from django.contrib import admin
from .models import *

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','added','updated')

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name','added','updated')

class genresAdmin(admin.ModelAdmin):
    list_display = ('name','added','updated')

class BookAdmin(admin.ModelAdmin):
    list_display = ('isbn','title','author','publisher','description','publish_date','price','stock','edition','cover_image','added','updated')

class book_genresAdmin(admin.ModelAdmin):
    list_display = ('book','genre','added','updated')
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book','customer','publish_date','text','rate','added','updated')




admin.site.register(Book,BookAdmin)
admin.site.register(genres,genresAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Publisher,PublisherAdmin)
admin.site.register(book_genres,book_genresAdmin)





# Register your models here.
