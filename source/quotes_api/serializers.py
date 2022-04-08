from rest_framework import serializers

from quotes_api.models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('id', 'text', 'name', 'email', 'ranking', 'status',)
        read_only_fields = ('id', 'user_id')


class QuoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quote
        exclude = ('ranking', 'status',)
        read_only_fields = ('id', 'user_id')


class QuoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('text', 'status', )


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('ranking',)
