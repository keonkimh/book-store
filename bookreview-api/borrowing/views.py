from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Borrow
from .serializers import BorrowSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None) -> Response:
        borrow = self.get_object()

        try:
            borrow.mark_as_returned()
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        return Response({"detail": "Book returned successfully.",
                        "fees_amount": borrow.fees_amount,
                        "fees_paid": borrow.fees_paid,
                        "paid_at": borrow.paid_at,
                        }, status=200)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Filter borrows by the authenticated user
        return Borrow.objects.filter(user=self.request.user)
