from http import HTTPStatus

from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from quotes_api.models import Quote
from quotes_api.serializers import QuoteSerializer, QuoteUpdateSerializer, QuoteCreateSerializer, RankingSerializer


@ensure_csrf_cookie
def get_csrf_token(request):
    if request.method == "GET":
        return HttpResponse()
    return HttpResponseNotAllowed(['GET'])


class IndexView(TemplateView):
    template_name = "index.html"


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(status=204)


class QuoteListCreateView(APIView):

    def get(self, request, *args, **kwargs):
        serializer_class = QuoteSerializer
        if self.request.user.has_perm('view_quote'):
            quotes = Quote.objects.all()
            serializer = serializer_class(quotes, many=True)
            return Response(serializer.data)
        else:
            quotes = Quote.objects.all().filter(status='moderated')
            serializer = serializer_class(quotes, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = QuoteCreateSerializer
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

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return super().get_permissions()


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
        if self.request.user.has_perm('delete_quote'):
            quote = get_object_or_404(Quote, pk=pk)
            serializer = serializer_class(quote)
            quote_ready = serializer.data['id']
            quote.delete()
            return Response({'pk': quote_ready})
        else:
            return Response({'Error': "You dont have rights."})


# class RankingView(APIView):
#
#     def post(self, request, *args, pk=None, **kwargs):
#         print(self.request.data)
#         # Prihodit + libo - v zavisomosti ot knopki {'sign': '+'}
#         sign = self.request.data.get("sign")
#         quote_pk = pk
#         session = request.session
#         quote = get_object_or_404(Quote, pk=pk)
#         try:
#             if sign in session[quote_pk]['sign']:
#                 return Response({'Error': "You cannot do this operation"})
#         except KeyError as Error:
#             session[quote_pk]['sign'] = sign
#             if session[quote_pk]['sign'] == "+":
#                 quote.ranking += 1
#                 quote.save()
#             if session[quote_pk]['sign'] == "-":
#                 quote.ranking -= 1
#                 quote.save()
#             return Response({"status": "Successfully added"}, status=200)
#


class RankingView(APIView):

    def post(self, request, *args, pk=None, **kwargs):
        # Prihodit + libo - v zavisomosti ot knopki {'sign': '+'}
        sign = self.request.data.get("sign")
        quote_pk = str(pk)
        session = request.session
        quote = get_object_or_404(Quote, pk=pk)
        if not session.get(quote_pk):
            session[quote_pk] = sign
            if session[quote_pk] == "+":
                quote.ranking += 1
                quote.save()
                return Response({"not_error": "No Problem", "ranking": f"{quote.ranking}"}, status=200)
            if session[quote_pk] == "-":
                quote.ranking -= 1
                quote.save()
                return Response({"not_error": "No Problem", "ranking": f"{quote.ranking}"}, status=200)
        else:
            print(session[quote_pk])
            print(sign)
            if sign == session[quote_pk]:
                return Response({"Error": "You cannot perform this aciton"}, status=400)
            else:
                if sign == "+":
                    session[quote_pk] = sign
                    quote.ranking += 1
                    quote.save()
                    return Response({"not_error": "No Problem", "ranking": f"{quote.ranking}"}, status=200)
                if sign == "-":
                    session[quote_pk] = sign
                    quote.ranking -= 1
                    quote.save()
                    return Response({"not_error": "No Problem", "ranking": f"{quote.ranking}"}, status=200)