from django.forms import ModelForm
from .models import SalaryReport, Salary


class SalaryReportForm(ModelForm):
    class Meta:
        model = SalaryReport
        fields = []


class SalaryForm(ModelForm):
    class Meta:
        model = Salary
        fields = ['worker', 'shifts_worked']