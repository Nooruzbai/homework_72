from django.urls import path

from quotes_api.views import QuoteListCreateView, QuoteEditView

app_name = 'quotes_api'

urlpatterns = [
    path('get/quotes/', QuoteListCreateView.as_view(), name='article_list_create_view'),
    path('quotes/<int:pk>/', QuoteEditView.as_view(), name='article_single_object_view')
]
