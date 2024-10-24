from pathlib import Path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from visits.models import PageVisit

this_dir = Path(__file__).resolve().parent

VALID_CODE = 'abc123'

LOGIN_URL = settings.LOGIN_URL

def home_page(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    my_title = "Home"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "total_visit_count": qs.count()
    }
    html_template = "home.html"
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_context)

def about_page(request, *args, **kwargs):
    my_title = "About"
    my_context = {
        "page_title": my_title
    }
    html_template = "home.html"
    return render(request, html_template, my_context)

def pw_protected_page(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    if request.method == 'POST':
        user_pw_sent = request.POST.get('code') or None
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, 'protected/entry.html', {})

@login_required(login_url=LOGIN_URL)
def user_only_page(request, *args, **kwargs):
    return render(request, 'protected/user_only.html', {})

@staff_member_required(login_url=LOGIN_URL)
def staff_only_page(request, *args, **kwargs):
    return render(request, 'protected/user_only.html', {})