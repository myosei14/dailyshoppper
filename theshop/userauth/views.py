from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import escape
from django.views import View
from .forms import CustomerForm, AccountInfoForm
from .models import Customer, AccountInfo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin


# class Authz(View):
#     template_name = "userauth/account.html"
#
#     def get(self, request):
#         login = reverse_lazy('login')
#         context = {
#             'login': login
#         }
#         return render(request, self.template_name, context)

def login_customer(request):
    if request.user.is_authenticated:
        return redirect('index')
    next = ''
    if request.GET:
        next = request.GET['next']
    if request.method == 'POST':
        email = escape(request.POST.get('email'))
        password = escape(request.POST.get('password'))
        print('this is next ', next)
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            print(user.name)
            messages.success(request, 'Login Successful')
            if next != '':
                return redirect(next)
            else:
                return redirect('login')
        else:
            messages.error(request, 'Email or password is incorrect')

    return render(request, 'userauth/login.html')


def logout_customer(request):
    logout(request)
    return redirect('login')


class Register(View):
    template_name = "userauth/register.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        customer_details_form = CustomerForm(request.POST)
        account_info_form = AccountInfoForm(request.POST)
        context = {
            'customer_form': customer_details_form,
            'account_info_form': account_info_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        customer = CustomerForm(request.POST)
        account_info = AccountInfoForm(request.POST)
        customer_email = customer.data['email']
        customer_exist = False
        try:
            if Customer.objects.get(email=customer_email):
                customer_exist = True
        except:
            print('Customer does not exist')

        if customer_exist:
            customer_form = CustomerForm(data=request.POST)
            account_info_form = AccountInfoForm(data=request.POST)
            messages.error(request, 'Email already exists')
            context = {
                'customer_form': customer_form,
                'account_info_form': account_info_form
            }
            return render(request, self.template_name, context)

        elif customer.is_valid() & account_info.is_valid():
            print('\n\n\n after valid \n\n\n')
            customer_data = customer.cleaned_data
            current_customer, created = Customer.objects.get_or_create(
                name=customer_data['name'],
                email=customer_data['email'],
                password=make_password(customer_data['password'])
            )
            account_info_data = account_info.cleaned_data
            current_account_info, created = AccountInfo.objects.get_or_create(
                house_number=account_info_data['house_number'],
                street=account_info_data['street'],
                town=account_info_data['town'],
                region_or_county=account_info_data['region_or_county'],
                postcode=account_info_data['postcode'],
                country=account_info_data['country'],
                phone=account_info_data['phone'],
                customer=current_customer
            )

            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.error(request, account_info.errors)
            return render(request, self.template_name)


class Account(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'userauth/account.html'
        

    def get(self, request):
        if request.user.is_authenticated:
            customer = Customer.objects.get(email = request.user)
            accountinfo = AccountInfo.objects.get(customer= request.user)

            context = {
                'accountinfo':accountinfo,
            }
        return render(request, self.template_name, context)
