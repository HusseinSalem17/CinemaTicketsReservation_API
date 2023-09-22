from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins


# 1 without REST and no model query (if want the return data from request is json direct without any serializer)
def no_rest_no_model(request):
    guests = [
        {
            "id": 1,
            "Name": "Omar",
            "mobile": 78495,
        },
        {
            "id": 2,
            "Name": "Hussein",
            "mobile": 5949,
        },
    ]
    return JsonResponse(guests, safe=False)


# 2 model data default django without rest
def no_rest_from_model(request):
    data = Guest.objects.all()  # to get all guests in the data
    response = {
        "guests": list(
            data.values(
                "name", "mobile"
            ),  # to just return name and mobile from all data (return as list)
        ),
    }
    return JsonResponse(response)


# Queries
# list == (GET)
# create == (POST)
# pk queru == (GET)
# update == (PUT)
# delete destroy == (DELETE)


# 3 Function based views
# 3.1 GET POST (use @api_view)
@api_view(["GET", "POST"])  # this means this function handle type of request
def FBV_List(request):
    # GET
    if request.method == "GET":
        try:
            guests = Guest.objects.all()
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GuestSerializer(
            guests, many=True
        )  # send the data from model to serializer (json)
        return Response(serializer.data)
    # POST
    elif request.method == "POST":
        serializer = GuestSerializer(
            data=request.data
        )  # send data to serializer (json)
        if serializer.is_valid():
            # means if the data don't contain values (name or mobile)
            serializer.save()  # to save data in admin panal
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )  # response will bet the data and the status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3.1 GET PUT DELETE (use @api_view)
@api_view(["GET", "PUT", "DELETE"])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)  # Get the user with this primary key (pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == "GET":
        serializer = GuestSerializer(
            guest
        )  # send the data from model to serializer (json)
        return Response(serializer.data)
    # PUT
    elif request.method == "PUT":
        serializer = GuestSerializer(
            guest, data=request.data
        )  # send data to serializer (json)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    elif request.method == "DELETE":
        guest.delete()
        Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# CBV class based views (Get and Post)
# 4.1 List and Create == GET and POST (Here take APIView as parameter) from rest_framework.views import APIView
# don't put @api_view above the function (APIView is the type and request), it came with many attributes
class CBV_List(APIView):
    # For get request
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    # for post request
    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get Put Delete class based views -- pk (use class with little conditions but function(above) is better for conditions)
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Mixins (to don't write many code)
# 5.1 Mixins list
class mixins_list(
    
)