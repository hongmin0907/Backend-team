from django import forms

from .models import *


class StayForm(forms.ModelForm):
    class Meta:
        model = Stay
        fields = ('name', 'location', 'introduce',
                  'builtDate', 'remodeledDate', 'serviceKinds',
                  'serviceIntroduce', 'serviceNotice', 'pickupNotice', 'directions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = '상호명'
        self.fields['location'].label = '위치'
        self.fields['introduce'].label = '숙소 소개'
        self.fields['builtDate'].label = '완공 일자'
        self.fields['remodeledDate'].label = '리모델링 일자'
        self.fields['serviceKinds'].label = '편의시설 및 서비스 선택'
        self.fields['serviceIntroduce'].label = '편의시설 및 서비스 소개'
        self.fields['serviceNotice'].label = '이용안내'
        self.fields['pickupNotice'].label = '픽업안내'
        self.fields['directions'].label = '찾아오시는 길'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('stay', 'name', 'hoursAvailable', 'hoursUntil', 'daysCheckIn', 'daysCheckOut', 'hoursPrice', 'daysPrice', 'checkHours', 'checkDays')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='')
    class Meta:
        model = Image
        fields = ('image',)

from django import forms

from accounts.models import User

# 룸 상세 페이지에서 checkInOutForm 먼저 띄우고, 저장받아서 예약 페이지에 보여줌
class CheckInOutForm(forms.Form):
    class Meta:
        fields = ('checkIn', 'checkOut',)

# 예약 폼(클라이언트)
class ReservationForm(forms.ModelForm):
    WAY_CHOICES = (
        (1, "도보"),
        (2, "차량"),
    )
    wayToGo = forms.ChoiceField(choices=WAY_CHOICES, label="", initial="", widget=forms.Select(), required=True)

    class Meta:
        model = Reservation
        fields= ('booker', 'phoneNumber', 'wayToGo')

