# _*_ encoding: utf-8 _*_

"""
@athor: frank
@time: 2017/3/19 17:10
"""
from django import forms
from operation.models import UserAsk
import re

class UserAskForm(forms.ModelForm):
    # myFields =
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code="mobile_invalid")
