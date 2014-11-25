# from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.views import APIView
from api.serializers import DeviceSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from haus.models import Device, Atom


class DeviceListView(APIView):

    def get(self, request, format=None):
        devices = Device.objects.filter(user_id=request.user.pk)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        # print("\nRequest == " + str(dir(request)))

        # print(request.user.id)

        device = self.get_object(request)
        serializer = DeviceSerializer(device, data=request.DATA)

        print "\nrequest.DATA == " + str(request.DATA)

        print(serializer.is_valid())

        print serializer.attributes()

        if serializer.is_valid():
            serializer.save()
            if serializer.was_created is True:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif serializer.was_created is False:
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, request):

        try:

            return Device.objects.filter(user=request.user.id, name=request.DATA['name']).first()

            #print("device_pk == " + str(device_pk))

            # This is based on the assumption that users can only see
            # devices that include those users as owners. (nb reverse relation)
            # Should this assumption be changed, this code must change as well:
            # return request.user.devices.get(pk=device_pk)

            # Now changed to models and open-access:
            # return Device.objects.get(pk=device_pk)

        except Device.DoesNotExist:
            # The device must then be made inside the serializer,
            # which is expecting None.
            return None

    # def put(self, request, device_pk, format=None):
    #     device = self.get_object(device_pk)
    #     serializer = DeviceSerializer(device, data=request.DATA)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class DeviceDetailView(APIView):

    # NOTE: Unlike in the tutorial, request is passed to get_object()
    # because we're not currently importing models. We can import models
    # and change the query from request.....get() to a more direct model query.
    def get_object(self, device_pk):
        try:
            # This is based on the assumption that users can only see
            # devices that include those users as owners. (nb reverse relation)
            # Should this assumption be changed, this code must change as well:
            # return request.user.devices.get(pk=device_pk)

            # Now changed to models and open-access:
            return Device.objects.get(pk=device_pk)

        except Device.DoesNotExist:
            raise Http404

    def get(self, request, device_pk, format=None):
        device = self.get_object(device_pk)
        serializer = DeviceSerializer(device)
        return Response(serializer.data)

    def put(self, request, device_pk, format=None):
        device = self.get_object(device_pk)
        serializer = DeviceSerializer(device, data=request.DATA)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # url(r'^devices/(?P<device_pk>[0-9]+)/$',
    #     views.DeviceView.as_view()),  # Get device info, put device data
    # url(r'^devices/(?P<device_pk>[0-9]+)/current/$',
    #     views.CurrentDeviceView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/$',
    #     views.AtomView.as_view()),
    # url(r'^devices/(?P<device_pk>[0-9]+)/atom/(?P<atom_pk>[0-9]+)/current/$',
    #     views.CurrentAtomView.as_view()),
