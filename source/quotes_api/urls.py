from django.urls import path

from quotes_api.views import QuoteListCreateView, QuoteEditView, IndexView, get_csrf_token, RankingView

app_name = 'quotes_api'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('get/quotes/', QuoteListCreateView.as_view(), name='article_list_create_view'),
    path('quotes/<int:pk>/', QuoteEditView.as_view(), name='article_single_object_view'),
    path("get-csrf-token/", get_csrf_token, name="get_csrf_token"),
    path('quote/ranking/<int:pk>/', RankingView.as_view(), name="raking_view")
]
