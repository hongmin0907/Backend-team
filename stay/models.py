from django.db import models

from django.contrib.auth import get_user_model

from multiselectfield import MultiSelectField

from datetime import date, timedelta

class Category(models.Model):
    staying = models.CharField(max_length=50)  # 모텔, 호텔/리조트, 펜션/풀빌라, 게스트하우스

# 편의시설 및 서비스 항목들(multi select)
SERVICE_CHOICES = (
    (1, '주차가능'),
    (2, '레스토랑'),
    (3, '커피숍'),
    (4, '유료세탁'),
    (5, '객실금연'),
    (6, '연회장'),
    (7, '비즈니스'),
    (8, '와이파이'),
    (9, '조식운영'),
    (10, '스파/월풀'),
    (11, '수영장'),
    (12, '파티룸'),
    (13, '커플PC'),
    (14, '무인텔'),
    (15, '바베큐'),
    (16, '족구장'),
)

# 숙소 정보 입력할 모델
class Stay(models.Model):
    # name 앞에 city 이름 붙일 것(ex. '강남', '역삼', '선릉')
    # name에서 해당 city 쿼리셋하거나
    # location 위치정보를 이용하여 해당 위치의 숙소 쿼리셋 실시시

    # 모텔, 호텔,리조트, 펜션/풀빌라, 게스트하우스 선택
    category = models.ForeignKey(Category, on_delete=models.SET, null=True, blank=True, related_name="stays")

    # 숙소 이름(ex. 역삼 바레)
    name = models.CharField(max_length=50)

    # 유저 아이디(ex. positipman)
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="stays")

    # 숙소 위치(ex. 서울특별시 강남구 봉은사로 428)
    location = models.CharField(max_length=100)

    # 건물 지어진 날짜(2019-07-07)
    built_date = models.DateField(auto_now=False, blank=True)

    # 리모델링된 날짜(2019-07-07)
    remodeled_date = models.DateField(auto_now=False, blank=True)

    # 프렌차이즈 여부(true 혹은 false)
    check_franchise = models.BooleanField(default=False)

    # 신축/리모델링 여부(유동적 -> 설정한지 1년 지나면 자동 해제)
    check_new_or_remodeling = models.BooleanField(default=False)

    # 숙소 소개
    introduce = models.TextField()

    # 초특가호텔 --> 초특가할인 변경 (사장이 당일특가로 가격 40% 이상 할인 시, 초특가할인 true로 설정)
    # ForeignKey로 연결되어 있는 아래의 Room 모델에서 초특가할인 여부 확인

    # 편의시설 및 서비스 항목 (상기 SERVICE_CHOICES 참고)
    service_kinds = MultiSelectField(choices=SERVICE_CHOICES, null=True, blank=True)

    # 편의시설 및 서비스 설명
    service_introduce = models.TextField(blank=True)

    # 이용안내
    service_notice = models.TextField()

    # 픽업안내
    pickup_notice = models.TextField(blank=True)

    # 찾아오시는 길
    directions = models.TextField(blank=True)

    # 찜하기
    like = models.ManyToManyField(get_user_model(), related_name="like_stay")

    # 관리자페이지에서 저장될 객체의 순서 기준 설정
    class Meta:
        ordering = ['category']


# room --> 멀티 이미지 구현 필요
class Room(models.Model):
    # 숙소 선택(호텔, 모텔, 펜션 외)
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, related_name="rooms")
    # 룸 이름
    name = models.CharField(max_length=50)

    # 누가 어느 방을 예약했는지 확인
    reserved = models.ManyToManyField(get_user_model(), related_name="reserved")

    # 대실 이용시간(ex. 3) --> 0이면 숙박만 가능
    hours_available = models.IntegerField(default=0)
    # 대실 운영시간(ex. 23) --> ~23:00
    hours_until = models.IntegerField(default=0)
    # 숙박 체크인 가능 시간(ex. 22(오후 10시))
    days_check_in = models.IntegerField(default=0)
    # 숙박 체크아웃 마감시간(ex. 11(오전 11시))
    days_check_out = models.IntegerField(default=0)

    # 룸마다 가능한 체크인/체크아웃 시간 설정
    # views.py에서 특정 유저가 해당 룸 예약 시, 그 체크인/체크아웃 시간대는 다른 유저가 사용하지 못하도록 진행 필요
    # 방안 추가 모색 필요
    days_checkin_possible = models.DateTimeField(auto_now=False)

    # 대실 예약가
    hours_price = models.IntegerField(default=0)
    # 숙박 예약가
    days_price = models.IntegerField(default=0)

    # 대실 예약 가능 여부(유저가 예약한 상황에 따라 True, False 자동 설정 필요)
    check_hours = models.BooleanField(default=True)

    # 숙박 예약 가능 여부(유저가 예약한 상황에 따라 True, False 자동 설정 필요)
    check_days = models.BooleanField(default=True)

    # 데이터 있으면, 해당 할인가로 표시
    # views.py에서 할인률 40% 이상이면, 초특가할인으로 지정하도록 구현할 것
    # 대실 예약가 할인
    sale_hours_price = models.IntegerField(default=0)
    # 숙박 예약가 할인
    sale_days_price = models.IntegerField(default=0)

    # 기본정보
    basic_info = models.TextField(blank=True)
    # 예약공지
    reservation_notice = models.TextField()
    # 취소규정
    cancel_regulation = models.TextField()


# 이미지 정보 저장할 모델 (숙소 이미지 사진들)
class Image(models.Model):
    # 특정 숙소의 룸 사진들 정보 저장
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, related_name="images_stay")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images_room")
    # 이미지 저장
    image = models.ImageField(upload_to='room_image/%Y/%m/%d', blank=False)

    def __str__(self):
        return self.stay.name + "image"

# 댓글 저장할 모델
class Comment(models.Model):
    # 특정 숙소에 대한 댓글 저장
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, related_name='comments')
    # 로그인한 유저
    username = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="comments")
    # 댓글 작성 시, 자동으로 댓글 작성한 날짜 저장
    created = models.DateTimeField(auto_now_add=True)
    # 댓글 수정 시, 자동으로 댓글 수정한 날짜 저장
    updated = models.DateTimeField(auto_now=True)
    # 대댓글 기능 구현 위해 대댓글 작성할 특정 댓글 선택
    parent_comment_id = models.IntegerField(default=0)

    # 평가항목 별 점수 선택
    evaluation_items1 = models.IntegerField(default=5) # 친절도
    evaluation_items2 = models.IntegerField(default=5) # 청결도
    evaluation_items3 = models.IntegerField(default=5) # 편의성
    evaluation_items4 = models.IntegerField(default=5) # 서비스 만족도


# 유저가 예약할 때 필요한 정보 저장
class Reservation(models.Model):
    # 예약할 숙소
    stay = models.ForeignKey(Stay, on_delete=models.SET_NULL, null=True, blank=True, related_name="reservations")
    # 예약할 룸
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="reservations")
    # 로그인한 유저아이디
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reservations")
    # 예약자 이름
    booker = models.CharField(max_length=20)
    # 예약자 번호(문자열 형태로 입력받는다)
    phone_number = models.CharField(max_length=30)

    # 유저의 체크인 희망시간 저장(프론트단에서 체크인 시간 데이터 받아서 저장 예정)
    check_in = models.DateTimeField(auto_now=False)
    # 유저의 체크아웃 희망시간 저장(프론트단에서 체크아웃 시간 데이터 받아서 저장 예정)
    check_out = models.DateTimeField(auto_now=False)

    # 유저의 대실 시작 시간(프론트단에서 시작 시간 데이터 받아서 저장)
    hours_start = models.TimeField()
    # 유저의 대실 종료 시간(프론트단에서 시작 시간 데이터 받아서 저장) --> 유저 대실 시작시간 + 해당 룸의 대실 이용시간
    hours_end = models.TimeField()

    # 대실, 숙박 선택(대실 혹은 숙박 예약하기 클릭 시, 해당 항목 True로 자동 변경)
    check_hours = models.BooleanField(default=False)
    check_days = models.BooleanField(default=False)

    # 예약한 날짜 자동 저장
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username