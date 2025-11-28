from rest_framework import serializers

class StatystykiPytaniaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    pytanie_id = serializers.IntegerField(read_only=True)
    ilosc_odpowiedzi = serializers.IntegerField()
    poprawne_odpowiedzi = serializers.IntegerField()
    procent_poprawnych = serializers.SerializerMethodField()
    
    def get_procent_poprawnych(self, obj):
        if obj.get('ilosc_odpowiedzi', 0) > 0:
            return round((obj['poprawne_odpowiedzi'] / obj['ilosc_odpowiedzi']) * 100, 2)
        return 0.0

class StatystykaUpdateInputSerializer(serializers.Serializer):
    pytanie_id = serializers.IntegerField()
    is_correct = serializers.BooleanField(
        help_text="Czy odpowiedź na to pytanie była poprawna (True/False)"
    )