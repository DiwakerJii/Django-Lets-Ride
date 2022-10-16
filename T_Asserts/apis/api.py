from django.http import JsonResponse
from django.shortcuts import render
from django.core import serializers
from apis.models import RideInfo, TravelInfo, User
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

@csrf_exempt
@api_view(('GET','POST'))
@renderer_classes((JSONRenderer,))
def signup(request):
    if request.method == "POST":
        name = request.data.get("name",None)
        mobile = request.data.get("mobile",None)
        user_name = request.data.get("user_name",None)
        user_type = request.data.get("user_type",None)
        email = request.data.get("email",None)
        password = request.data.get("password",None)

        if name and mobile and user_type and email and password:
            if len(str(mobile)) != 10:
                try:
                    mobile = int(mobile)
                except:
                    return Response({"status":False,"message":"Please eneter valid mobile number"},status=status.HTTP_400_BAD_REQUEST)
                return Response({"status":False,"message":"Please eneter valid mobile number"},status=status.HTTP_400_BAD_REQUEST)

            if not user_name:
                short_user_name = str(email).split("@")
                user_name = str(short_user_name[0]) + "@t_asserts"

            if User.objects.filter(email=email).exists():
                return Response({"status":True,"message":"User already exists"},status=status.HTTP_200_OK)

            created = User.objects.create(name=name,mobile=int(mobile),user_type=user_type,user_name=user_name,email=email,password=str(password))
            if created:
                return Response({"status":True,"message":"User created succefully","uid":created.uid},status=status.HTTP_201_CREATED)
            else:
                return Response({"status":False,"message":"Something went Wrong"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status":False,"message":"Please provide required credentials"},status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(('GET','POST'))
@renderer_classes((JSONRenderer,))
def login(request):
    if request.method == "POST":
        email = request.data.get("email",None)
        password = request.data.get("password",None)

        if email and password:
            if User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).order_by('-created').last()
                if user.password == str(password):
                    user_data = {
                        "uid" : user.uid,
                        "name" : user.name,
                        "user_name" : user.user_name,
                        "email" : user.email,
                        "user_type" : user.user_type,
                        "mobile" : user.mobile,
                    }
                    return Response({"status":True,"message":"User succefully Login","data":user_data},status=status.HTTP_202_ACCEPTED)
            return Response({"status":False,"message":"Wrong password or email ID"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status":False,"message":"Please provide email and password"},status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(('GET','POST'))
@renderer_classes((JSONRenderer,))
def CreateTravelInfo(request):
    if request.method == "POST":
        going_from = request.data.get("going_from",None)
        date_time = request.data.get("date_time",None)
        going_to = request.data.get("going_to",None)
        created_by = request.data.get("created_by",None)
        medium = request.data.get("medium",None)
        assets_quantity = request.data.get("quantity",None)
        assets_type = request.data.get("type",None)
        assest_sensitivity = request.data.get("sensitivity",None)
        delivered_to = request.data.get("delivered_to",None)

        if going_from and going_to and date_time and created_by and medium and assets_quantity and assets_type and assest_sensitivity and delivered_to:
            try:
                assets_type = str(assets_type).lower()
                assets_type = 1 if assets_type == 'laptop' else 2 if assets_type == 'travel_bag' else 3 if assets_type == 'packages' else 0
                assest_sensitivity = str(assest_sensitivity).lower()
                assest_sensitivity = 1 if assest_sensitivity == 'normal' else 2 if assest_sensitivity == 'sensitive' else 3 if assest_sensitivity == 'highly sensitive' else 0
                created = TravelInfo.objects.create(
                    going_from=going_from,going_to=going_to,created_by=int(created_by),
                    preferred_medium=medium,assets_quantity=int(assets_quantity),assets_type=int(assets_type),
                    assest_sensitivity=int(assest_sensitivity),delivered_to=delivered_to,date_time=str(date_time)
                )
                if created:
                    created_data = created.__dict__
                    del created_data['_state']
                    created_data["created"] = created_data["created"].strftime("%d %B,%y - %I:%M %p")
                    created_data["assets_type"] = "Laptop" if created_data["assets_type"]==1 else "Travel Bag" if created_data["assets_type"]==2 else "Packages" if created_data["assets_type"]==3 else None
                    created_data["assest_sensitivity"] = "Normal" if created_data["assest_sensitivity"]==1 else "Sensitive" if created_data["assest_sensitivity"]==2 else "Highly Sensitive" if created_data["assest_sensitivity"]==3 else None
                    created_data["created_by"] = User.objects.filter(uid=int(created_data["created_by"])).values('uid','name','user_name')
                    return Response({"status":True,"message":"Data succefully created","data":created_data},status=status.HTTP_202_ACCEPTED)
                
            except Exception as e:
                pass
            return Response({"status":False,"message":"Something went Wrong"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status":False,"message":"Please provide required credentials"},status=status.HTTP_400_BAD_REQUEST)


    if request.method == "GET":
        user_id = request.GET.get("user_id")
        if user_id:
            try:
                travel_info = TravelInfo.objects.filter(created_by=user_id).order_by("-created").values()
                for item in travel_info:
                    item["created"] = item["created"].strftime("%d %B,%y - %I:%M %p")
                    item["assets_type"] = "Laptop" if item["assets_type"]==1 else "Travel Bag" if item["assets_type"]==2 else "Packages" if item["assets_type"]==3 else None
                    item["assest_sensitivity"] = "Normal" if item["assest_sensitivity"]==1 else "Sensitive" if item["assest_sensitivity"]==2 else "Highly Sensitive" if item["assest_sensitivity"]==3 else None
                    item["created_by"] = User.objects.filter(uid=int(item["created_by"])).values('uid','name','user_name')
                    if item['accepted_by_id']:
                        item["accepted_by_id"] = User.objects.filter(uid=int(item["accepted_by_id"])).values('uid','name','user_name')
                return Response({"sucess":True,"data":travel_info},status=status.HTTP_200_OK)
            except:
                return Response({"status":False,"message":"Something went Wrong"},status=status.HTTP_404_NOT_FOUND) 
        else:
            travel_info = TravelInfo.objects.all().order_by("-created").values()
            for item in travel_info:
                item["created"] = item["created"].strftime("%d %B,%y - %I:%M %p")
                item["assets_type"] = "Laptop" if item["assets_type"]==1 else "Travel Bag" if item["assets_type"]==2 else "Packages" if item["assets_type"]==3 else None
                item["assest_sensitivity"] = "Normal" if item["assest_sensitivity"]==1 else "Sensitive" if item["assest_sensitivity"]==2 else "Highly Sensitive" if item["assest_sensitivity"]==3 else None
                item["created_by"] = User.objects.filter(uid=int(item["created_by"])).values('uid','name','user_name')
                if item['accepted_by_id']:
                    item["accepted_by_id"] = User.objects.filter(uid=int(item["accepted_by_id"])).values('uid','name','user_name')
            return Response({"sucess":True,"data":travel_info},status=status.HTTP_200_OK)



        
@csrf_exempt
@api_view(('GET','POST'))
@renderer_classes((JSONRenderer,))
def AcceptTravel(request):
    if request.method == "POST":
        travel_info_id = request.data.get("travel_info_id",None)
        accepted_by = request.data.get("accepted_by",None)
        if travel_info_id and accepted_by:
            try:
                user = User.objects.get(uid=int(accepted_by))
                travel_info = TravelInfo.objects.get(id=int(travel_info_id))
                travel_info.accepted_by = user
                travel_info.save()
                updated_data = travel_info.__dict__
                del updated_data['_state']
                updated_data["created"] = updated_data["created"].strftime("%d %B,%y - %I:%M %p")
                updated_data["assets_type"] = "Laptop" if updated_data["assets_type"]==1 else "Travel Bag" if updated_data["assets_type"]==2 else "Packages" if updated_data["assets_type"]==3 else None
                updated_data["assest_sensitivity"] = "Normal" if updated_data["assest_sensitivity"]==1 else "Sensitive" if updated_data["assest_sensitivity"]==2 else "Highly Sensitive" if updated_data["assest_sensitivity"]==3 else None
                updated_data["created_by"] = User.objects.filter(uid=int(updated_data["created_by"])).values('uid','name','user_name')
                updated_data["accepted_by_id"] = User.objects.filter(uid=int(updated_data["accepted_by_id"])).values('uid','name','user_name')
                return Response({"status":True,"message":"Data succefully created","data":updated_data},status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                print(e)    
            return Response({"status":False,"message":"Something went Wrong"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status":False,"message":"Please provide required credentials"},status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(('GET','POST'))
@renderer_classes((JSONRenderer,))
def CreateRideInfo(request):
    if request.method == "POST":
        created_by = request.data.get("created_by",None)
        going_from = request.data.get("going_from",None)
        date_time = request.data.get("date_time",None)
        going_to = request.data.get("going_to",None)
        medium = request.data.get("medium",None)
        assets_quantity = request.data.get("quantity",None)
        if created_by and going_from and date_time and going_to and medium and assets_quantity:
            try:
                user = User.objects.get(uid=int(created_by))
                created = RideInfo.objects.create(
                    created_by=user,going_from=going_from,going_to=going_to,travel_medium=medium,date_time=date_time,assets_quantity=assets_quantity
                )
                if created:
                    ride_info_data = created.__dict__
                    del ride_info_data["_state"]
                    ride_info_data["created"] = ride_info_data["created"].strftime("%d %B,%y - %I:%M %p")
                    ride_info_data["created_by_id"] = User.objects.filter(uid=int(ride_info_data["created_by_id"])).values('uid','name','user_name')
                    return Response({"status":True,"message":"Data succefully created","data":ride_info_data},status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                pass
            return Response({"status":False,"message":"Something went Wrong"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status":False,"message":"Please provide required credentials"},status=status.HTTP_400_BAD_REQUEST)


    if request.method == "GET":
        user_id = request.GET.get("user_id")
        if user_id:
            try:
                ride_info = RideInfo.objects.filter(created_by=user_id).order_by("-created").values()
                for item in ride_info:
                    item["created"] = item["created"].strftime("%d %B,%y - %I:%M %p")
                    item["created_by_id"] = User.objects.filter(uid=int(item["created_by_id"])).values('uid','name','user_name')
                return Response({"sucess":True,"data":ride_info},status=status.HTTP_200_OK)
            except:
                return Response({"message":"Something went Wrong"},status=status.HTTP_404_NOT_FOUND) 
        else:
            ride_info = RideInfo.objects.all().order_by("-created").values()
            for item in ride_info:
                item["created"] = item["created"].strftime("%d %B,%y - %I:%M %p")
                item["created_by_id"] = User.objects.filter(uid=int(item["created_by_id"])).values('uid','name','user_name')
            return Response({"sucess":True,"data":ride_info},status=status.HTTP_200_OK)