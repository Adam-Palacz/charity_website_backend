from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from .models import Category, Donation, Institution, CustomUser, DonationModelForm, CustomUserForm


class LandingPageView(View):
    def get(self, request):
        quantity_counter = sum(Donation.objects.values_list('quantity', flat=True))

        institution_counter = len(Donation.objects.values_list('institution', flat=True).distinct())

        foundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        fundraisings = Institution.objects.filter(type=3)

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

    def post(self, request):
        logout_button = request.POST.get('logout')
        if logout_button:
            logout(request)
            return render(request, "index.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class AddDonationView(View):
    def get(self, request):
        form = DonationModelForm()
        user = request.user
        if not user.is_authenticated:
            return redirect("/login")
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, "form.html",
                      context={"categories": categories, "institutions": institutions, form: "form"})

    def post(self, request):
        form = DonationModelForm(request.POST)
        categories = request.POST['categories'].split(",")
        institution = Institution.objects.get(pk=request.POST['institution'])
        user = request.user
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            for category in categories:
                instance.categories.add(Category.objects.get(name=category))
                instance.save()
            instance.institution = institution
            instance.save()
            return render(request, 'form-confirmation.html')
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        return render(request, "register.html")


class RegisterView(View):
    def get(self, request):
        logout(request)
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
            user = CustomUser.objects.create_user(email=email, password=password)
            user.first_name = name
            user.last_name = surname
            user.save()
            return render(request, "login.html")


class ProfileView(View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user_id=user.pk)
        return render(request, "user_profile.html", context={'donations': donations})

    def post(self, request):
        pk_donation = int(request.POST.get('pk_donation'))
        is_taken = request.POST.get('is_taken')
        donation = Donation.objects.get(pk=pk_donation)
        if is_taken:
            donation.is_taken =True
            donation.save()
        else:
            donation.is_taken = False
            donation.save()
        return redirect("/profile/")


class FormConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class EditProfileView(View):
    def get(self, request):
        return render(request, 'edit_profile.html')

    # def post(self,request):
    #     form = CustomUserForm(request.POST)
    #     user = request.user
    #     user_model = CustomUser.objects.get(pk=user.pk)
    #     passoword = request.POST.get('password')
    #     passoword2 = request.POST.get('password2')
    #     instance = form.save(commit=False)
    #     if passoword != passoword2:
    #         instance.password = passoword
    #     instance
