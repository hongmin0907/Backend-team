from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.urls import reverse
from .forms import ReservationForm
from django.db.models import Q
from search.models import Search
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
    # 사용자가 메인 페이지의 검색 기능 사용 시,
    if request.GET.get('mainSearch', request.POST.get('mainSearch', None)):
        # ---------메인페이지 검색페이지에서 사용자가 키워드 입력한 경우 해당 숙소 필터링하는 코드---------
        # !! 키워드 검색 방법 보류(Search app 삭제 예정) !!
        # 프론트단으로부터 검색 키워드를 'searchKeyword'라는 변수로 받는다.
        keyword = request.GET.get('searchKeyword', None)
        # 사용자가 입력한 키워드에 해당하는 숙소 객체 선별
        search = Search.objects.filter(searchKey=keyword)
        if search.exists():
            # stays -> queryset type
            stays = search.stays.all()
        # !! search가 존재하지 않을 경우도 추가해줘야 한다. !!

        # ---------메인페이지 검색페이지에서 사용자가 총 인원수(성인+아동) 설정한 경우 해당 숙소 필터링하는 코드---------
        # 프론트단으로부터 총 인원 수를 'personnel'이라는 변수(int type)로 받는다.
        personnel = request.GET.get('personnel', None)
        # 사용자가 설정한 인원수를 수용할 수 있는 숙소 객체 선별
        stays = stays.filter(rooms__maximumPersonnel__gte=personnel).distinct()
        # !!stays.exists() 필요없도록 프론트단에서 반드시 personnel 데이터 받을 것

        # ---------메인페이지 검색페이지에서 사용자가 체크인/체크아웃 설정한 경우 해당 숙소 필터링하는 코드---------
        # !!협의 필요!!
        # 체크인/체크아웃 데이터 받는 방법
        # 방법1) 프론트단으로부터 사용자의 체크인/체크아웃 데이터를 받는다.(가급적 datetime 타입으로 받을 것 - 시간은 체크인 22시, 체크아웃 11시)
        #       str형태라면, str = '2019-07-01'이라면,
        #       str -> datetime 변환 방법1) datetime.strptime(str+' 00:00:00', '%Y-%m-%d %H:%M:%S')
        #       00:00:00 부분에 체크인 시간은 22:00:00, 체크아웃 시간은 11:00:00 로 설정할 것
        #       str -> datetime 변환 방법2)datetime(2019, 7), 1, 0, 0, 0)
        # 방법2) 백단에서 checkInOut form 을 이용하여 데이터 입력 받는다.
        requestCheckIn = request.GET.get('requestCheckIn', None)
        requestCheckOut = request.GET.get('requestCheckOut', None)
        # 사용자가 요청한 체크인/체크아웃 시간에 예약 가능한 숙소 객체 선별
        finalStays = []
        # # !! 이중 for문 -> 성능 저하 우려 -> 개선 방법 모색 !!
        for stay in stays:
            rooms = stay.rooms.all()
            for room in rooms:
                roomReservation = room.reservations.all()
                # 사용자가 요청한 체크인아웃 시간에 예약가능한 룸 --> 룸의 전체 checkInOut 객체수 == 사용자가 요청한 체크인/체크아웃시간과 겹치지 않는 룸의 checkInOut 객체 수
                if roomReservation.count() == roomReservation.filter\
                            (Q(checkIn__gte=requestCheckOut) \
                               | Q(checkOut__lte=requestCheckIn)).count():
                    # 예약가능한 룸의 숙소 객체를 stay 변수에 저장
                    stay = room.stay
                    # finalObjects에 해당 숙소 객체 없다면 추가(숙소 객체 중복 방지)
                    if stay not in finalStays:
                        finalStays.append(stay)
        # list 를 queryset 형태로 변경하고 싶은 경우
        finalStays = Stay.objects.filter(id__in=[object.id for object in finalStays])

        return render(request, 'stay/stay_list.html', {'objects': finalStays})

    # 지역별(ex. 서울 -> 강남/역삼/선릉/삼성) 검색할 때 해당 숙소 필터링하는 코드
    # !! 검토 이후, 구현 예정 !!
    stays = Stay.objects.all()

    return render(request, 'stay/stay_list.html', {'objects':stays})


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



