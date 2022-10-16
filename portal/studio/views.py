from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import RegisterUserForm
from django.urls import reverse_lazy
from .models import User, Order
from django.views.generic.base import TemplateView
from django.views import generic
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.


def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        'index.html',
        context={'num_visits': num_visits},  # num_visits appended
    )


@login_required
def profile(request):
    order_num = Order.objects.all()
    return render(request, 'studio/profile.html', context={'order_num': order_num})


class StudioLoginView(LoginView):
    template_name = 'registrations/login.html'


class StudioLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'registrations/login.html'


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    #  Функция просмотра для обновления определенного Order
    order_create = get_object_or_404(Order, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса:
        form = RegisterUserForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            order_create.save()

            # Переход по адресу 'profile':
            return HttpResponseRedirect(reverse('profile'))

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        form = RegisterUserForm()

    return render(request, 'studio/profile.html', {'form': form})


class OrderCreate(CreateView):
    model = Order
    fields = '__all__'


class OrderListViews(generic.ListView):
    model = Order
    paginate_by = 10
    context_object_name = 'order'
    template_name = 'studio/order_form.html'
