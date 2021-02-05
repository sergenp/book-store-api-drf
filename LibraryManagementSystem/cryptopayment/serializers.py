from libraryfrontend.serializers import LibraryBaseSerializer
from .models import Invoice

class Invoice(LibraryBaseSerializer):
    class Meta(LibraryBaseSerializer.Meta):
        model = Invoice