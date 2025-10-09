# dashboard/views.py
from django.shortcuts import render
from .models import App


def dashboard_view(request):
    apps = App.objects.all()
    return render(
        request=request,
        template_name="dashboard/dashboard.html",
        context={"apps": apps},
    )
