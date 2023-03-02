from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from subscriptions.serializers import (Client, ClientSerializer, Company,
                                       CompanySerializer, Subscription,
                                       SubscriptionRenewalSerializer,
                                       SubscriptionSerializer)


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = (AllowAny,)

    @action(methods=['post'],
            detail=False,
            url_path="renew",
            url_name="renew_subscription",
            serializer_class=SubscriptionRenewalSerializer)
    def renew_subscription(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=serializer.status)


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = (AllowAny,)


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (AllowAny, )
