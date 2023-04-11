from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django import forms
from django.forms.widgets import Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.forms.widgets import Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

class CustomSelectDateWidget(SelectDateWidget):
    def __init__(self, *args, decade_ranges=None, **kwargs):
        super().__init__(*args, **kwargs)
        if decade_ranges is None:
            decade_ranges = range(0, 100, 10)
        self.decade_ranges = decade_ranges

    def create_select(self, name, field, value, val, choices):
        if name == 'year':
            decades = []
            for decade_start in self.decade_ranges:
                decade_end = decade_start + 9
                decade_label = f"{decade_start}s"
                decade_choices = [(y, y) for y in range(decade_start, decade_end+1)]
                decades.append((decade_label, decade_choices))
            return forms.Select(choices=[("", "--------")] + decades, attrs=self.attrs)

        return super().create_select(name, field, value, val, choices)

    def render_options(self, choices, selected_choices):
        option_html = super().render_options(choices, selected_choices)
        option_html = option_html.replace('<option value=""', '<option disabled selected value=""')
        return option_html

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['decade_ranges'] = self.decade_ranges
        return context

    def decompress(self, value):
        if value:
            return [value.year, value.month, value.day]
        return [None, None, None]


class CustomDateField(forms.DateField):
    widget = CustomSelectDateWidget(years=range(timezone.now().year - 100, timezone.now().year + 1), decade_ranges=range(0, 100, 20))
class MyForm(forms.Form):
    date = CustomDateField()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    date = CustomDateField(label='Дата рождения')            
    users = (('1','Студент'), ('2','Преподаватель'), ('3','Администратор'))
    choice = forms.ChoiceField(choices = users, label= 'Статус')
    print(users)
    class Meta:
        model = User                
        fields = ['username', 'email', 'password1', 'password2', 'date', 'choice']
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Сохранить'))
        self.helper.layout = Layout(
            Fieldset(
                'Изменить информацию профиля',
                'first_name',
                'last_name'
            ),
        )