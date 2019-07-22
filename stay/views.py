from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.urls import reverse
from .forms import ReservationForm
from django.db.models import Q
import re
from django.http import JsonResponse


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
    # 검색 방법 1) 유저가 지역 선택하여 숙소 검색하는 경우
    if request.GET.get('selectRegion', None):
        print("지역선택하셨구만")
        # 프론트단으로부터 (모텔, 호텔/리조트, 펜션/풀빌라, 게스트하우스 중 1 택) 정보를 category라는 문자열 형태의 변수로 받는다.
        category_str = request.GET.get('category', None)
        category_obj = Category.objects.get(staying=category_str)

        # 특정 category에 해당하는 숙소 필터링
        stays = Stay.objects.filter(category=category_obj)

        # 유저가 지역 선택 시, 해당 데이터를 문자열 형태로 select_region으로 수신
        # ex. '강남/역삼/삼성/논현'
        select_region = request.GET.get('selectRegion')

        # 사용자가 입력한 키워드에 해당하는 숙소 객체 선별
        # 검색 키워드에서 한글 키워드만 필터링하여 리스트로 변환
        # ex. "강남/역삼/삼성/논현 --> ['강남','역삼','삼성','논현']
        not_hangul = re.compile('[^가-힣]+')
        result_str = not_hangul.sub(' ', select_region)
        result_list = result_str.split(' ')

        # Stay 모델의 name에 검색 키워드가 있는 숙소 필터링
        que_name = Q(name__icontains=result_list[0])
        for keyword in result_list[1:]:
            que_name |= Q(name__icontains=keyword)

        # Stay 모델의 location에 검색 키워드가 있는 숙소 필터링
        que_location = Q(location__icontains=result_list[0])
        for keyword in result_list[1:]:
            que_location |= Q(location__icontains=keyword)

        # 유저가 선택한 지역에 해당하는 숙소 필터링
        stays = Stay.objects.filter(que_name|que_location)

        # 지역별 숙소 목록에서 인기검색어 클릭한 경우(ex. #프랜차이즈)
        if request.GET.get('popularKeyword', None):
            popular_keyword = request.GET.get('popularKeyword')
            not_hangul = re.compile('[^가-힣]+')
            result_str = not_hangul.sub(' ', popular_keyword)
            result_list = result_str.split(' ')

            # 유저가 선택한 지역에 해당하는 숙소 중에서 인기검색어에 해당하는 숙소 필터링
            stays = stays.filter(keywords__name__in=result_list)
            print(stays)

        if not stays.exists():
            return JsonResponse({'searchResult':False})

        # ---------메인페이지 검색페이지에서 사용자가 총 인원수(성인+아동) 설정한 경우 해당 숙소 필터링하는 코드---------
        # 프론트단으로부터 총 인원 수를 'personnel'이라는 변수(int type)로 받는다.
        # default값으로 성인2, 아동0 --> 총 인원수 2명으로 설정 필수 (프론트단에서 설정)
        personnel = request.GET.get('personnel', None)
        # 사용자가 설정한 인원수를 수용할 수 있는 숙소 객체 선별
        stays = stays.filter(rooms__maximumPersonnel__gte=personnel).distinct()
        # !!stays.exists() 필요없도록 프론트단에서 반드시 personnel 데이터 받을 것

        # ---------메인페이지 검색페이지에서 사용자가 체크인/체크아웃 설정한 경우 해당 숙소 필터링하는 코드---------
        # default값으로 체크인 날짜는 현재일로 하여 1박2일 설정 필수 (프론트단에서 설정)
        # 프론트단으로부터 사용자의 체크인/체크아웃 데이터를 받는다.(가급적 datetime 타입으로 받을 것 - 시간은 체크인 22시, 체크아웃 11시)
        # 체크인/체크아웃 데이터가 str 형태라면,
        # str -> datetime 타입 변환 필요(ex. str = '2019-07-01')  ex) 2019-07-01 11:00:00
        #     방법1) datetime.strptime(str+' 00:00:00', '%Y-%m-%d %H:%M:%S')
        #           00:00:00 부분에 체크인 시간은 22:00:00, 체크아웃 시간은 11:00:00 로 설정할 것
        #     방법2) datetime(2019, 7, 1, 0, 0, 0)

        requestCheckIn = request.GET.get('requestCheckIn', None)
        requestCheckOut = request.GET.get('requestCheckOut', None)

        # 사용자가 요청한 체크아웃 시간이 체크인 시간보다 앞서 있을 때,
        # searchResult를 False 값으로 설정하여 전송
        if requestCheckOut < requestCheckIn:
            return JsonResponse({'searchResult': False})

        # 사용자가 요청한 체크인/체크아웃 시간에 예약 가능한 숙소 객체 선별
        finalStays = []
        for stay in stays:
            rooms = stay.rooms.all()
            for room in rooms:
                roomReservation = room.reservations.all()
                # 사용자가 요청한 체크인아웃 시간에 예약가능한 룸 --> 룸의 전체 checkInOut 객체수 == 사용자가 요청한 체크인/체크아웃시간과 겹치지 않는 룸의 checkInOut 객체 수
                if roomReservation.count() == roomReservation.filter \
                            (Q(checkIn__gte=requestCheckOut) \
                             | Q(checkOut__lte=requestCheckIn)).count():
                    # 예약가능한 룸의 숙소 객체를 stay 변수에 저장
                    stay = room.stay
                    # finalObjects에 해당 숙소 객체 없다면 추가(숙소 객체 중복 방지)
                    if stay not in finalStays:
                        finalStays.append(stay)
        # list 를 queryset 형태로 변경하고 싶은 경우
        finalStays = Stay.objects.filter(id__in=[object.id for object in finalStays])

        if not finalStays.exists():
            return JsonResponse({'searchResult':False})

        return render(request, 'stay/stay_list.html', {'objects': finalStays})

    # 검색 방법2) 유저가 키워드로 숙소 검색하는 경우
    elif request.GET.get('searchKeyword', None):
        # ---------메인페이지 검색페이지에서 사용자가 키워드 입력한 경우 해당 숙소 필터링하는 코드---------
        # 프론트단으로부터 검색 키워드를 'searchKeyword'라는 문자열 형태의 변수로 받는다.
        # ex) searchKeyword = "강남/역삼/선릉/삼성" or "서울 송파구 올림픽대로" or "역삼 마레" or "#프렌차이즈" ...
        search_keyword = request.GET.get('searchKeyword', None)

        # 사용자가 입력한 키워드에 해당하는 숙소 객체 선별
        # 검색 키워드에서 한글, 정수, 영문 키워드만 필터링하여 리스트로 변환
        # ex. "강남,역삼/삼성, 테헤란로2길 artist" --> ['강남','역삼','삼성','테헤란로2길, 'artist']
        removed_str = re.compile('[^가-힣\da-zA-Z]+')
        result_str = removed_str.sub(' ',search_keyword)
        result_list = result_str.split(' ')
        print(result_list)

        # 사용자가 정확한 주소가 아닌 다른 키워드로 검색한 경우
        # Stay 모델의 name에 검색 키워드가 있는 숙소 필터링
        que_name = Q(name__icontains=result_list[0])
        for keyword in result_list[1:]:
            que_name |= Q(name__icontains=keyword)

        # Stay 모델의 location에 검색 키워드가 있는 숙소 필터링
        que_location = Q(location__icontains=result_list[0])
        for keyword in result_list[1:]:
            que_location |= Q(location__icontains=keyword)

        # Stay 모델의 serviceKinds에 검색 키워드가 있는 숙소 필터링
        # 인기검색어 중 '파티룸', '수영장' 시설 갖춘 숙소 목록 제공
        que_service = None
        for i in range(len(SERVICE_CHOICES)):
            if SERVICE_CHOICES[i][1] in result_list:
                que_temp = Q(serviceKinds__icontains=SERVICE_CHOICES[i][0])
                que_service = que_service | que_temp if que_service else que_temp

        # Stay 모델의 name 또는 location 또는 keywords 필드에 검색 키워드가 있는 숙소 필터링(숙소 객체 중복 불가)
        # 검색 키워드에 serviceKinds 키워드가 있는 경우
        if que_service:
            stays = Stay.objects.filter(Q(keywords__name__in=result_list)|que_name|que_location|que_service).distinct()
        # 검색 키워드에 serviceKinds 키워드가 없는 경우
        else:
            stays = Stay.objects.filter(Q(keywords__name__in=result_list)|que_name|que_location).distinct()

        # 검색 키워드에 해당하는 숙소가 없을 경우
        if not stays.exists():
            return JsonResponse({'searchResult':False})

        personnel = request.GET.get('personnel', None)
        stays = stays.filter(rooms__maximumPersonnel__gte=personnel).distinct()

        requestCheckIn = request.GET.get('requestCheckIn', None)
        requestCheckOut = request.GET.get('requestCheckOut', None)

        if requestCheckOut < requestCheckIn:
            return JsonResponse({'searchResult':False})

        finalStays = []
        for stay in stays:
            rooms = stay.rooms.all()
            for room in rooms:
                roomReservation = room.reservations.all()

                if roomReservation.count() == roomReservation.filter\
                            (Q(checkIn__gte=requestCheckOut) \
                               | Q(checkOut__lte=requestCheckIn)).count():
                    stay = room.stay

                    if stay not in finalStays:
                        finalStays.append(stay)

        finalStays = Stay.objects.filter(id__in=[object.id for object in finalStays])

        if not finalStays.exists():
            return JsonResponse({'searchResult':False})

        return render(request, 'stay/stay_list.html', {'objects': finalStays})

    # 검색 방법3) 특정 위치 지정하여 검색하는 경우(프론트단에서 특정위치 주소로 변환 필요 ex. 서울특별시 강남구 테헤란로2길 ..)
    elif request.GET.get('currentAddress', None):
        # !! naver direction api 적용하여 현재위치로부터 일정 반경 내에 위치하는 숙소 필터링 하는 방향으로 진행 필요 !!
        #   --> 실제 야놀자에서는 서울시 성동구로 현재주소 설정되어 있어도 광진구와 같이 지역명 달라도 가까운 숙소 필터링됨
        # 임시로 구 혹은 길 지명이 일치하는 숙소 필터링 진행

        current_address = request.GET.get('currentAddress')
        # current_address = ['서울특별시', '강남구', '테헤란로2길', ...]
        current_address = current_address.split(' ')

        # que_location_ku --> 유저 현재위치의 '~구' 지명까지 일치하는 숙소 객체 필터링
        # que_location_gil --> 유저 현재위치의 '~길' 지명까지 일치하는 숙소 객체 필터링
        que_location_ku = None
        que_location_gil = None
        for i in range(len(current_address)):
            # ~시 ~구 ~길 까지만 필터링
            if i == 3:
                break
            elif i <= 1:
                que_temp = Q(location__icontains=current_address[i])
                que_location_gil = que_location_gil & que_temp if que_location_gil else que_temp
                que_location_ku = que_location_ku & que_temp if que_location_ku else que_temp
            else:
                que_temp = Q(location__icontains=current_address[i])
                que_location_ku = que_location_ku & que_temp if que_location_ku else que_temp

        # 유저 현재위치의 '~구' 지명까지 일치하거나 혹은 '~길' 지명까지 일치하는 숙소 필터링
        stays = Stay.objects.filter(que_location_ku|que_location_gil)

        # 검색 키워드에 해당하는 숙소가 없을 경우
        if not stays.exists():
            return JsonResponse({'searchResult': False})

        personnel = request.GET.get('personnel', None)
        stays = stays.filter(rooms__maximumPersonnel__gte=personnel).distinct()

        requestCheckIn = request.GET.get('requestCheckIn', None)
        requestCheckOut = request.GET.get('requestCheckOut', None)

        if requestCheckOut < requestCheckIn:
            return JsonResponse({'searchResult': False})

        finalStays = []
        for stay in stays:
            rooms = stay.rooms.all()
            for room in rooms:
                roomReservation = room.reservations.all()

                if roomReservation.count() == roomReservation.filter \
                            (Q(checkIn__gte=requestCheckOut) \
                             | Q(checkOut__lte=requestCheckIn)).count():
                    stay = room.stay

                    if stay not in finalStays:
                        finalStays.append(stay)

        finalStays = Stay.objects.filter(id__in=[object.id for object in finalStays])

        if not finalStays.exists():
            return JsonResponse({'searchResult':False})

        return render(request, 'stay/stay_list.html', {'objects': finalStays})

    # request method가 GET 아닌 경우
    else:
        stays = Stay.objects.all()
        return render(request, 'stay/stay_list.html', {'objects':stays})

@login_required
def stay_detail(request, stay_id):
    pass

@login_required
def stay_update(request, stay_id):
    pass

@login_required
def stay_delete(request, stay_id):
    pass

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



# 마이페이지 구현할