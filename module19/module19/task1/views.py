from django.shortcuts import render
from .forms import UserRegister
from .models import Buyer
from .models import Game


# Create your views here.
def main_page(requset):
    return render(requset, 'index2.html')


def store_games(requset):
    Games = Game.objects.all()
    context = {'Games': Games}
    return render(requset, 'first_page.html', context)


def cart_page(request):
    cart_items = {
        'GTA 5': {'price': 3, 'quantity': 1},
        'Mario': {'price': 3, 'quantity': 1},
        'Wukong': {'price': 3, 'quantity': 1}
    }

    total = sum(item['price'] * item['quantity'] for item in cart_items.values())
    discount = 0.1 if total > 200 else 0
    final_total = total - (total * discount)
    discount_percent = discount * 100
    return render(request, 'second_page.html', {
        'cart_items': cart_items,
        'total': total,
        'final_total': final_total,
        'discount_percent': discount_percent
    })


users = ['Anton', 'Vitya', 'Vitalya']


def sign_up_by_django(request):
    info = {}
    form = UserRegister(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            existing_users = Buyer.objects.values_list('name', flat=True)

            if username in existing_users:
                info['error'] = 'Пользователь уже существует'
            elif password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif age < 18:
                info['error'] = 'Вы должны быть старше 18'
            else:
                Buyer.objects.create(name=username, age=age, balance=1000)
                info['message'] = f'Приветствуем, {username}!'

        info['form'] = form

    return render(request, 'registration_page.html', info)


def sign_up_by_html(request):
    info = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age'))

        existing_users = Buyer.objects.values_list('name', flat=True)

        if username in existing_users:
            info['error'] = 'Пользователь уже существует'
        elif password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        elif age < 18:
            info['error'] = 'Вы должны быть старше 18'
        else:
            Buyer.objects.create(name=username, age=age, balance=1000)
            info['message'] = f'Приветствуем, {username}!'

    return render(request, 'registration_page.html', info)