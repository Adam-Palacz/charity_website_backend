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
            return redirect('/')


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
        return redirect('/form/')


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return redirect('/register/')


class RegisterView(View):
    def get(self, request):
        logout(request)
        return render(request, "register.html")

    def post(self, request):
        form = CustomUserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
            return redirect('/login/')
        return render(request, "register.html", context={"form": form})


class ProfileView(View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user_id=user.pk)
        sorted_donations = donations.order_by('is_taken', '-pick_up_date', '-pick_up_time')
        return render(request, "user_profile.html", context={'donations': sorted_donations})

    def post(self, request):
        pk_donation = int(request.POST.get('pk_donation'))
        is_taken = request.POST.get('is_taken')
        donation = Donation.objects.get(pk=pk_donation)
        if is_taken:
            donation.is_taken = True
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

    def post(self, request):
        form = CustomUserForm(request.POST)
        user = request.user
        password = form.data['password']
        password2 = form.data['password2']
        email = form.data['email']
        first_name = form.data['first_name']
        last_name = form.data['last_name']
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if password != '' and password == password2:
            user.set_password(password)
            user.save()
            return redirect('/login/')
        return redirect('/edit-profile/')


class PasswordAuthorizationView(View):
    def get(self, request):
        return render(request, 'authorization.html')

    def post(self, request):
        user = request.user
        password = request.POST.get('password')
        user_test = authenticate(email=user.email, password=password)
        if user_test is not None:
            return redirect('/edit-profile/')
        return redirect('/authorization/')
