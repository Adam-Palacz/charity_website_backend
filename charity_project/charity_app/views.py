from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Category, Donation, Institution



class LandingPageView(View):
    def get(self, request):
        quantity_counter = sum(
            [Donation.objects.values_list()[i][1] for i in range(len(Donation.objects.values_list()))]
        )
        institution_counter = len(Institution.objects.all())

        foundations = Institution.objects.filter(type=1)
        organizations = [Institution.objects.filter(type=2)[i] for i in range(len(Institution.objects.filter(type=2)))]
        fundraisings = [Institution.objects.filter(type=3)[i] for i in range(len(Institution.objects.filter(type=3)))]

        paginator_foundation = Paginator(foundations, 5)
        paginator_organization = Paginator(organizations, 5)
        paginator_fundraising = Paginator(fundraisings, 5)
        page_number = request.GET.get('page')
        page_obj_foundation = paginator_foundation.get_page(page_number)
        page_obj_organization = paginator_organization.get_page(page_number)
        page_obj_fundraising = paginator_fundraising.get_page(page_number)

        context = {
            'quantity': quantity_counter, 'institution_counter': institution_counter,
            'foundations': foundations, 'organizations': organizations,
            'fundraisings': fundraisings, "page_obj_foundation": page_obj_foundation,
            "page_obj_organization": page_obj_organization, "page_obj_fundraising": page_obj_fundraising,
        }
        return render(request, "index.html", context=context)

    def post(self,request):
        logout_button = request.POST.get('logout')
        if logout_button:
            logout(request)
            return render(request, "index.html")

class AddDonationView(View):
    def get(self, request):

        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self,request):
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            name = user.first_name
            return render(request, "index.html", context={'username':name})
        else:
            return render(request, "register.html")
        # try:
        #     User.objects.get(username=username, password=password)
        #     return render(request, "index.html")
        # except ObjectDoesNotExist:
        #     return render(request, "register.html")

class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password != password2:
            return render(request, "register.html")
        else:
            user = User.objects.create_user(username=email, password=password, email=email)
            user.first_name = name
            user.last_name = surname
            user.save()
            return render(request, "login.html")