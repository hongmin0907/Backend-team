from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.urls import reverse
from .forms import ReservationForm

def main_page(request):
    return render(request, 'stay/main.html')

# 숙소 생성(관리자) 페이지
@login_required
def stay_create(request):
    if request.method == "POST":
        stay_form = StayForm(request.POST, request.FILES)
        if stay_form.is_valid():
            stay_form = stay_form.save(commit=False)
            stay_form.username = request.user

            return redirect(reverse("stay:stay_list"))

    else:
        stay_form = StayForm()

    return render(request, 'stay/stay_create.html', {'stay_form':stay_form})

# 숙소 목록 페이지
def stay_list(request):
    stays = Stay.objects.all()

    return render(request, 'stay/stay_list.html', {'object_list':stays})
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import serializers
# from rest_framework import status
# class StaySearch(APIView):
#     def post(self, request, format=None):
#         keywords = request.POST.get('keywords',None)
#         print(keywords)
#
#         if keywords is not None:
#             keywords = keywords.split(',')
#
#             stays = models.Stay.objects.filter(keywords__name__in=keywords).distinct()
#             return render(request, 'stay/stay_list.html', {'objects':stays})
#             serializer = serializers.CountStaySerializer(stays, many=True)
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         else:
#             stays = models.Stay.objects.all()
#             serializer = serializers.CountStaySerializer(stays, many=True)
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#             return Response(status=status.HTTP_400_BAD_REQEUST)



# 룸 생성 페이지
@login_required
def room_create(request, stay_id):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=10)
    stay = Stay.objects.get(pk=stay_id)
    if request.method == "POST":
        room_form = RoomForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if room_form.is_valid() and formset.is_valid():
            room_form = room_form.save(commit=False)
            room_form.stay = stay
            room_form.username = request.user

            room_form.save()

            for form in formset.cleaned_data:
                # this helps not to crash if the user don't upload all the photos
                if form:
                    image = form['image']
                    photo = Image(stay=stay, room=room_form, image=image)
                    photo.save()

            return redirect(reverse("stay:room_list", args=[stay_id]))
        else:
            print(room_form.errors, formset.errors)
    else:
        room_form = RoomForm()
        formset = ImageFormSet(queryset=Image.objects.none())

    return render(request, 'stay/room_create.html', {'room_form':room_form, 'formset':formset})


def room_list(request, stay_id):
    stay =  Stay.objects.get(pk=stay_id)
    rooms = stay.rooms.all()
    return render(request, 'stay/room_list.html', {'stay':stay,'room_list':rooms})



@login_required
def reservation_create(reqeust, room_id):
    pass
