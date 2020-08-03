from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serialize import BoxSerializer
from django.contrib.auth.decorators import login_required
from products.models import *
from datetime import timedelta, date, datetime
from django.db.models import Q

# Create your views here.
@login_required(login_url='/')
def productHomeView(request):
    return render(request, "products/index.html")

@api_view(http_method_names=['GET','POST'])
@login_required(login_url='/')
def addBox(request):
    if request.method == 'GET':
        if request.user.is_staff:
            return render(request, "products/add.html")
        else:
            return Response({'error': 'Access Denined. You must be a staff to add box'}, status=401)
    if request.method == 'POST':
        length = int(request.POST['length'])
        width = int(request.POST['width'])
        height = int(request.POST['height'])
        volume = length * width * height
        area = 2 * (length * width + width * height + height * length)
        last_updated_date = date.today()
        all_box = Box.objects.all()
        total_box = len(all_box)
        total_area = 0
        total_volume = 0
        for box in all_box:
            total_area += box.area
            total_volume += box.volume
        if (total_area + area) / (total_box + 1) < Count.objects.get(id=1).average_area:
            if (total_volume + volume) / (total_box + 1) < Count.objects.get(id=1).average_volume:
                if len(Box.objects.filter(Q(creation_date__gte=date.today()-timedelta(days=7)))) > Count.objects.get(id=1).box_added_in_week:
                    if len(Box.objects.filter(
                            Q(creation_date__gte=date.today() - timedelta(days=7))
                    ).filter(user_id=request.user.id)) > Count.objects.get(
                            id=1).box_added_by_user_in_week:
                        try:
                            box = Box(length=length, width=width, height=height, volume=volume, area=area, last_updated_date=last_updated_date, created_by=request.user.username, user_id=request.user.id)
                            box.save()
                            return Response({'error': 'Box Added Successfully'}, status=200)
                        except Exception as e:
                            return Response({'error': 'Failed to add box. Please try again.'}, status=403)
                    else:
                        return Response({'error': 'You have reached limit for adding box in a week'}, status=403)
                else:
                    return Response({'error': 'Limit Reached for adding Boxes in a Week.'}, status=403)
            else:
                return Response({'error': 'Average Volume exceeded limit.'}, status=403)
        else:
            return Response({'error': "Average area exceeded limit"}, status=403)


@login_required(login_url='/')
@api_view(http_method_names=['GET', 'POST'])
def deleteBox(request):
    if request.method == 'GET':
        return render(request, "products/delete.html")
    if request.method == 'POST':
        box_id = request.POST['id']
        box = Box.objects.get(id=box_id)
        if box.user_id == request.user.id:
            box.delete()
            return Response({'success': 'Box deleted Successfully'}, status=200)
        else:
            return Response({'error': 'Access Denined. You must be creator to delete it.'}, status=401)


@login_required(login_url='/')
@api_view(http_method_names=['GET', 'POST'])
def allBox(request):
    if request.method == 'GET':
        return render(request, "products/allbox.html")
    if request.method == 'POST':
        box = Box.objects.all()
        box = check_request(request, box)
        if box is not None:
            serializer = BoxSerializer(box, many=True)
            return Response(serializer.data, status=200)
        else:
            return  Response({'error': 'User Does not Exists'}, status=401)

@api_view(http_method_names=['GET', 'POST'])
@login_required(login_url='/')
def updateBox(request):
    if request.method == "GET":
        return render(request, "products/update.html")
    if request.method == 'POST':
        if request.user.is_staff:
            if 'creation_date' in request.POST or 'created_by' in request.POST:
                return Response({'error': 'Access Denined. You cannot edit creation_date or created_by'}, status=401)
            else:
                box_id = int(request.POST['id'])
                length = int(request.POST['length'])
                width = int(request.POST['width'])
                height = int(request.POST['height'])

                volume = length * width * height
                area = 2 * (length * width + width * height + height * length)

                all_box = Box.objects.all()
                total_box = len(all_box)
                total_area = 0
                total_volume = 0
                for box in all_box:
                    total_area += box.area
                    total_volume += box.volume

                if (total_area + area) / (total_box + 1) < Count.objects.get(id=1).average_area:
                    if (total_volume + volume) / (total_box + 1) < Count.objects.get(id=1).average_volume:
                        try:
                            box = Box.objects.get(id=box_id)
                        except Exception as e:
                            box = None
                        if box:
                            try:
                                box.length = length
                                box.width = width
                                box.height = height
                                box.last_updated_date = date.today()
                                box.save()
                                return Response({'message': 'Box Updated Successfully'}, status=200)
                            except Exception as e:
                                return Response({'error': 'Error Occured While Updating Box. Please try Again'}, status=403)

                        else:
                            return Response({'error': 'Box Does not exists'}, status=403)
                    else:
                        return Response({'error': 'Average Volume exceeded limit.'}, status=403)
                else:
                    return Response({'error': "Average area exceeded limit"}, status=403)

        else:
            return Response({'error': 'Access Denined. You must be a staff to update'}, status=401)




@login_required(login_url='/')
@api_view(http_method_names=['GET', 'POST'])
def myBox(request):
    if request.method == 'GET':
        if request.user.is_staff:
            return render(request, 'products/mybox.html')
        else:
            return Response({'error': 'You must be a staff to access this info.'},status=401)
    if request.method == 'POST':
        user_id = request.user.id
        box = Box.objects.filter(user_id=user_id)
        box = check_request(request, box)
        if box is not None:
            serialize = BoxSerializer(box, many=True)
            return Response(serialize.data, status=200)
        else:
            return Response({'error': 'User Does not Exists'}, status=401)


def check_request(request, box):
    if 'min_length' in request.POST and request.POST['min_length'] != '':
        min_length = int(request.POST['min_length'])
        box = box.filter(Q(length__gte=min_length))
    if 'max_length' in request.POST and request.POST['max_length'] != '':
        max_length = int(request.POST['max_length'])
        box = box.filter(Q(length__lte=max_length))
    if 'min_width' in request.POST and request.POST['min_width'] != '':
        min_width = int(request.POST['min_width'])
        box = box.filter(Q(width__gte=min_width))
    if 'max_width' in request.POST and request.POST['max_width'] != '':
        max_width = int(request.POST['max_width'])
        box = box.filter(Q(width__lte=max_width))
    if 'min_height' in request.POST and request.POST['min_height'] != '':
        min_height = int(request.POST['min_height'])
        box = box.filter(Q(height__gte=min_height))
    if 'max_height' in request.POST and request.POST['max_height'] != '':
        max_height = int(request.POST['max_height'])
        box = box.filter(Q(height__lte=max_height))
    if 'min_area' in request.POST and request.POST['min_area'] != '':
        min_area = int(request.POST['min_area'])
        box = box.filter(Q(area__gte=min_area))
    if 'max_area' in request.POST and request.POST['max_area'] != '':
        max_area = int(request.POST['max_area'])
        box = box.filter(Q(area__lte=max_area))
    if 'min_volume' in request.POST and request.POST['min_volume'] != '':
        min_volume = int(request.POST['min_volume'])
        box = box.filter(Q(volume__gte=min_volume))
    if 'max_volume' in request.POST and request.POST['max_volume'] != '':
        max_volume = int(request.POST['max_volume'])
        box = box.filter(Q(volume__lte=max_volume))
    if 'min_date' in request.POST and request.POST['min_date'] != '':
        min_date = datetime.strptime(request.POST['min_date'], '%Y-%m-%d').date()
        box = box.filter(Q(creation_date__gte=min_date))
    if 'max_date' in request.POST and request.POST['max_date'] != '':
        max_date = datetime.strptime(request.POST['max_date'], '%Y-%m-%d').date()
        box = box.filter(Q(creation_date__lte=max_date))
    if 'username' in request.POST and request.POST['username'] != '':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            user = None
            box = None
        if user:
            box = box.objects.filter(user_id=user.id)

    return box