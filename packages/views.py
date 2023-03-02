from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.status import HTTP_201_CREATED
from packages.serializers import (Package, PackageSerializer,
                                  Service, ServiceSerializer,
                                  Period, PeriodSerializer)
from invoices.serializers import ServicePaymentSerializer
from rest_framework.response import Response


class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    permission_classes = (AllowAny,)

    @action(methods=['post'],
            detail=False,
            url_path="initiate_payment",
            url_name="initiate_service_payment",
            serializer_class=ServicePaymentSerializer)
    def initiate_payment(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class PeriodViewSet(ModelViewSet):
    serializer_class = PeriodSerializer
    queryset = Period.objects.all()
    permission_classes = (AllowAny,)


class PackageViewSet(ModelViewSet):
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    permission_classes = (AllowAny,)
