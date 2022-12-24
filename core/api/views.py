from django.contrib.gis.geos import Point
from rest_framework.exceptions import APIException
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer


class ProviderView(ListCreateAPIView):
    """
       API endpoint that allows provider to be viewed or edited.

       create:
       Return a new provider.

       read:
       Return all providers.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ProviderDetails(RetrieveUpdateDestroyAPIView):
    """
       API endpoint that allows Provider to be viewed or edited or deleted.

       read:
       Return  provider.

       update:
       edit provider.

       destroy:
       delete provider.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaView(ListCreateAPIView):
    """
       API endpoint that allows Service Area to be created or listed.

       create:
       Return a new service_area.

       read:
       Return all Service Area.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer


class ServiceAreaDetails(RetrieveUpdateDestroyAPIView):
    """
       API endpoint that allows Service Area to be viewed or edited or deleted.

       retrieve:
       Return  service_area instance.

       update:
       edit service_area instance.

       destroy:
       delete service_area instance
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer


class ServiceAreaAPI(APIView):
    """
        Return a list of services areas that contais the required Point
        :param lng
        :param lat
    """
    def get(self, request, *args, **kwargs):
        try:
            params = request.query_params
            latitude = float(params.get('lat', None))
            longitude = float(params.get('lng', None))
            point = Point(latitude, longitude)
            service_areas = ServiceArea.objects.filter(
                polygon__intersects=point)
            serializer = ServiceAreaSerializer(service_areas, many=True)
            return Response(serializer.data)
        except (TypeError, ValueError):
            raise APIException('Params format is invalid')
