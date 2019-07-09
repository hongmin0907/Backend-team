from django import forms

from .models import *


class StayForm(forms.ModelForm):
    class Meta:
        model = Stay
        fields = ('name', 'location', 'introduce',
                  'built_date', 'remodeled_date', 'check_franchise',
                  'check_new_or_remodeling', 'service_kinds',
                  'service_introduce', 'service_notice', 'pickup_notice', 'directions')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = '상호명'
        self.fields['location'].label = '위치'
        self.fields['introduce'].label = '숙소 소개'
        self.fields['built_date'].label = '완공 일자'
        self.fields['remodeled_date'].label = '리모델링 일자'
        self.fields['check_franchise'].label = '프렌차이즈 여부'
        self.fields['check_new_or_remodeling'].label = '신축/리모델링 여부'
        self.fields['service_kinds'].label = '편의시설 및 서비스 선택'
        self.fields['service_introduce'].label = '편의시설 및 서비스 소개'
        self.fields['service_notice'].label = '이용안내'
        self.fields['pickup_notice'].label = '픽업안내'
        self.fields['directions'].label = '찾아오시는 길'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('stay', 'name', 'hours_available', 'hours_until', 'days_check_in', 'days_check_out', 'days_checkin_possible', 'hours_price', 'days_price', 'check_hours', 'check_days')

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

class ReservationForm(forms.ModelForm):
    WAY_CHOICES = (
        (1, "도보"),
        (2, "차량"),
    )
    way_to_go = forms.ChoiceField(choices=WAY_CHOICES, label="", initial="", widget=forms.Select(), required=True)

    class Meta:
        model = Reservation
        fields=('username', 'phone_number', 'way_to_go',)


