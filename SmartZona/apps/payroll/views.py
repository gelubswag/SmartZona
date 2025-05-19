from datetime import datetime

from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator

from SmartZona.utils import model_crud
from SmartZona.apps.users.decorators import allowed_roles
from .models import SalaryReport, Salary
from .forms import SalaryReportForm, SalaryForm
from SmartZona.apps.users.models import CustomUser


@method_decorator(allowed_roles(['manager']), 'dispatch')
class IndexView(View):
    def get(self, request):
        return model_crud(
            request,
            SalaryReportForm,
            SalaryReport,
            'payroll/index.html'
            )

    def post(self, request):
        report = SalaryReport.objects.create(
            manager=request.user,
            date=datetime.now(),
            total_amount=0,
        )
        error: str | None = None
        try:
            report.save()
            for worker in CustomUser.objects.all():
                if worker.role.name == 'customer':
                    continue
                salary = Salary.objects.create(
                    report=report,
                    worker=worker,
                )
                salary.rate = worker.salary_rate
                salary.save()
        except Exception as e:
            error = "Ошибка при добавлении"
            print(e)

        return render(
            request,
            'payroll/index.html',
            {
                'objects': SalaryReport.objects.all(),
                'error': error,
            }
        )


@method_decorator(allowed_roles(['manager']), 'dispatch')
class DetailSalaryReportView(View):
    def get(self, request, pk):
        form = SalaryForm()
        salaries = Salary.objects.filter(report=pk).all()
        return render(
            request,
            'payroll/detail.html',
            {
                'objects': salaries,
                'form': form,
                'report': SalaryReport.objects.get(pk=pk),
            }
        )

    def post(self, request, pk):
        form = SalaryForm(request.POST)
        salaries = Salary.objects.filter(report=pk).all()
        worker = request.POST.get('worker')
        if not worker:
            error = "Выберите работника"
        elif form.is_valid() and 'change' in request.POST:
            salary = Salary.objects.get(report=pk, worker=worker)
            salary.report = SalaryReport.objects.get(pk=pk)
            salary.shifts_worked = request.POST.get('shifts_worked')
            salary.save()
            s = 0
            for salary in salaries:
                s += salary.current_amount
            salary.report.total_amount = s
            salary.report.save()
            return render(
                request,
                'payroll/detail.html',
                {
                    'objects': salaries,
                    'form': form,
                    'report': SalaryReport.objects.get(pk=pk),
                }
            )
        elif 'delete' in request.POST:
            salary = Salary.objects.get(report=pk, worker=worker)
            s = 0
            for sal in salaries:
                s += sal.current_amount
            s -= salary.current_amount
            salary.report.total_amount = s
            salary.report.save()
            salary.delete()
            return render(
                request,
                'payroll/detail.html',
                {
                    'objects': salaries,
                    'form': form,
                    'report': SalaryReport.objects.get(pk=pk),
                }
            )
        return render(
            request,
            'payroll/detail.html',
            {
                'objects': salaries,
                'form': form,
                'report': SalaryReport.objects.get(pk=pk),
                'error': error
            }
        )
