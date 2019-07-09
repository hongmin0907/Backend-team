from django.shortcuts import render, redirect

from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from datetime import date, timedelta
from django.urls import reverse
from .forms import ReservationForm


# 숙소 생성(관리자) 페이지
@login_required
def stay_create(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
    if request.method == "POST":
        stay_form = StayForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())


        if stay_form.is_valid() and formset.is_valid():
            stay_form = stay_form.save(commit=False)
            stay_form.username = request.user
            # 건물 지어진지 180일 이내이거나, 리모델링된지 180일 이내이면 신축/리모델링 True, 아니면 False
            if date.today() - stay_form.built_date < timedelta(days=180) \
                    or date.today() - stay_form.remodeled_date < timedelta(days=180):
                stay_form.check_new_or_remodeling = True
            else:
                stay_form.check_new_or_remodeling = False

            stay_form.save()


            for form in formset.cleaned_data:
                # this helps not to crash if the user don't upload all the photos
                if form:
                    image = form['image']
                    photo = Image(stay=stay_form, image=image)
                    photo.save()
            messages.success(request, "check it out on the home page!")

            return redirect(reverse("stay:stay_list"))
        else:
            print(stay_form.errors, formset.errors)
    else:
        stay_form = StayForm()
        formset = ImageFormSet(queryset=Image.objects.none())


    return render(request, 'stay/stay_create.html', {'stay_form':stay_form, 'formset':formset})

# 숙소 목록 페이지
def stay_list(request):
    stays = Stay.objects.all()
    print(stays)
    return render(request, 'stay/stay_list.html', {'object_list':stays})

# 예약 페이지(클라이언트)
def reservation_page(request, stay_id):
    pass