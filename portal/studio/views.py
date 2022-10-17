from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView
from .forms import RegisterUserForm, RegisterOrderForm
from django.urls import reverse_lazy
from .models import User, Order
from django.views.generic.base import TemplateView
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime


# Create your views here.


def index(request):
    num_order = Order.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        'index.html',
        context={'num_order': num_order, 'num_visits': num_visits},
    )


class OrderDetailView(generic.DetailView):
    model = Order


class LoanedOrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'studio/orderinstance_list_customer_user.html'
    paginate_by = 10
    context_object_name = 'orderinstance_list'

    def get_queryset(self):
        return Order.objects.all()


class LoanedOrdersAllListView(PermissionRequiredMixin, generic.ListView):
    model = Order
    permission_required = 'catalog.can_mark_returned'
    context_object_name = 'orderinstance_list'
    template_name = 'studio/orderinstance_list_customer_all.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(status__exact='')


def create_order(request, pk):
    #  Функция просмотра для обновления определенного BookInstance библиотекарем
    order_inst = get_object_or_404(Order, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RegisterOrderForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            order_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('my-order'))

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.

    return render(request, 'studio/order_create.html')


class OrderCreate(CreateView):
    model = Order
    fields = ['name', 'summary', 'category', 'photo_file']


class OrderUpdate(UpdateView):
    model = Order
    fields = ['id', 'summary', 'customer_order']
    permission_required = 'catalog.can_mark_returned'


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
