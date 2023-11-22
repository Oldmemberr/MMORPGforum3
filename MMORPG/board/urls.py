from django.urls import path
from .views import PostsList, AddList, DetailList, DeleteView, EditList, CommentView, SubscribeToCategory, UnSubscribeToCategory


urlpatterns = [
    path('', PostsList.as_view(), name='board'),
    path('add', AddList.as_view(), name='add'),
    path('<int:pk>', DetailList.as_view(), name='detail'),
    path('edit/<int:pk>', EditList.as_view(), name='edit'),
    path('edit/<int:pk>', DeleteView.as_view(), name='delete'),
    path('comments/<int:pk>', CommentView.as_view(), name='comments'),
    path('<int:pk>/subscribe/', SubscribeToCategory.as_view(), name='subscribe'),
    path('<int:pk>/unsubscribe/', UnSubscribeToCategory.as_view(), name='unsubscribe'),
]