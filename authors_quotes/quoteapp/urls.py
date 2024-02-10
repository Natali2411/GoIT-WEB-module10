from django.urls import path
from . import views


app_name = 'quoteapp'

urlpatterns = [
    path('', views.quotes, name='quotes'),
    path('tag/', views.tag, name='tag'),
    path('tag/<int:tag_id>', views.tag_search, name='tag_search'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('author/<int:author_id>', views.detail_author, name='detail_author'),
    path('scrape/', views.scrape_info, name='scrape_info'),
]
