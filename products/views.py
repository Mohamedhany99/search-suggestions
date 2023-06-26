from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
import csv
import io
from uuid import uuid4
from decimal import Decimal
from rest_framework import generics


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(["POST"])
def import_products(request):
    csv_file = request.FILES["file"]
    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=",", quotechar="|"):
        # print(column[0])
        obj, created = Product.objects.update_or_create(
            id=column[0],
            defaults={
                "name": column[1],
                "category": column[2],
                "price": Decimal(column[3]),
            },
        )
        # print(obj)
        obj.save()
        if created:
            obj.save()
        else:
            pass
            # print(obj)

    return Response(data="importing completed!", status=201)


@api_view(["GET"])
def search(request):
    try:
        query = request.GET.get("q", "")
        suggestions = Product.objects.filter(name__icontains=query)[:10]
        serializer = ProductSerializer(suggestions, many=True)
        return Response(serializer.data)
    except:
        return Response(
            data="cannot find product info", status=status.HTTP_409_CONFLICT
        )


class ListProducts(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        try:
            queryset = Product.objects.all()
            return queryset
        except Product.DoesNotExist:
            return ValueError

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except:
            return Response(
                data="cannot list products", status=status.HTTP_409_CONFLICT
            )
