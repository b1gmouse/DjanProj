from django.urls import path
from .views import (NewsList, NewDetail, PostCreate, PostUpdate, PostDelete, PostSearch, PostCreateNew, PostDeleteArticle, PostUpdateArticle, PostCategoryView, subscribe_to_category,
                    )

app_name = 'news'

urlpatterns = [
   path('', NewsList.as_view(), name='new_list'),
   path('search/<int:pk>', NewDetail.as_view(), name='new_detail'),
   path('create/', PostCreateNew.as_view(), name='post_create'),
   path('articles/create/', PostCreate.as_view(), name='post_create'),
   path('articles/<int:pk>/edit/', PostUpdateArticle.as_view(), name='post_update'),
   path('articles/<int:pk>/delete/', PostDeleteArticle.as_view(), name='post_delete'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('category/<int:pk>/', PostCategoryView.as_view(), name='category'),
   path('subscribe/<int:pk>/', subscribe_to_category, name='subscribe'),
]

