from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from quotes_api.models import Quote
from quotes_api.serializers import QuoteSerializer, QuoteUpdateSerializer, QuoteCreateSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(status=204)


class QuoteListCreateView(APIView):

    def get(self, request, *args, **kwargs):
        serializer_class = QuoteSerializer
        quotes = Quote.objects.all()
        serializer = serializer_class(quotes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = QuoteCreateSerializer
        print(request.data)
        serializer = serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.validated_data,
            status=HTTPStatus.CREATED
        )

    def handle_exception(self, exc):
        if isinstance(exc, Exception):
            print(exc)
            return JsonResponse(data={'error': "Something went wrong"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return super().handle_exception(exc)


class QuoteEditView(APIView):

    def get(self, request, *args, pk=None, **kwargs):
        serializer_class = QuoteSerializer
        quote = get_object_or_404(Quote, pk=pk)
        serializer = serializer_class(quote)

        return Response(serializer.data)

    def put(self, request, *args, pk=None, **kwargs):
        serializer_class = QuoteUpdateSerializer
        quote = get_object_or_404(Quote, pk=pk)
        serializer = serializer_class(data=request.data, instance=quote)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as err:
            return Response(data=err.detail, status=HTTPStatus.BAD_REQUEST)

        return Response(
            data=serializer.validated_data,
        )

    def delete(self, request, *args, pk=None, **kwargs):
        serializer_class = QuoteSerializer
        quote = get_object_or_404(Quote, pk=pk)
        serializer = serializer_class(quote)
        quote_ready = serializer.data['id']
        quote.delete()
        return Response({'pk': quote_ready})