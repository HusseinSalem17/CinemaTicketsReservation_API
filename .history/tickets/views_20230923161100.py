from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation, Post
from rest_framework.decorators import api_view
from .serializers import (
    GuestSerializer,
    MovieSerializer,
    ReservationSerializer,
    PostSerializer,
)
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly


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
# parameters is that will write the code in the class and the class, and generics get the response of API
class mixins_list(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 5.2 Mixins pk(get put delete)
# get => mixins.RetrieveModelMixin
# put => mixins.UpdateModelMixin
# delete => mixins.DestroyModelMixin
class mixins_pk(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


# 6 Generics
# 6.1 GET POST the return is list (have built in get and put)
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # to put permissions on this view (api endpoint)
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# 6.2 GET PUT DELETE
class generic_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # to make authentication with token (TokenAuthentication)
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# 7 ViewSets for GET PUT POST DELETE (with pk also)
class viewSets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "mobile"]


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["movie"]


class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# 8 Find movie (using function will be more easy)
@api_view(["GET"])
def find_movie(request):
    try:
        movies = Movie.objects.filter(
            hall=request.data["hall"],
            movie=request.data["movie"],
        )
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 9 create new reservation(using function will be easy to make reservation)
@api_view(["POST"])
def new_reservation(request):
    try:
        guest = Guest()
        guest.name = request.data["name"]
        guest.mobile = request.data["mobile"]
        guest.save()
        movie = Movie.objects.get(
            hall=request.data["hall"],
            movie=request.data["movie"],
        )
        reservation = Reservation()
        reservation.guest = guest
        reservation.movie = movie
        reservation.save()
        serializer = ReservationSerializer(reservation)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
