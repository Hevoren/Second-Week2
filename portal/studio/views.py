from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView
from .forms import RegisterUserForm, RegisterOrderForm
from django.urls import reverse_lazy
from .models import User, Order, Customer, OrderInstance
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


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 10
    context_object_name = 'order_list'
    template_name = 'orders/order_list.html'


class OrderDetailView(generic.DetailView):
    model = Order


class CustomerListView(generic.ListView):
    model = Customer
    paginate_by = 10
    context_object_name = 'customer_list'
    template_name = 'customers/customer_list.html'


class CustomerDetailView(generic.DetailView):
    model = Customer


class LoanedOrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = OrderInstance
    template_name = 'studio/orderinstance_list_customer_user.html'
    paginate_by = 10

    def get_queryset(self):
        return OrderInstance.objects.filter(customer_order=self.request.user).filter(status__exact='').order_by(
            'due_back')


class LoanedOrdersAllListView(PermissionRequiredMixin, generic.ListView):
    model = OrderInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'studio/orderinstance_list_customer_all.html'
    paginate_by = 10

    def get_queryset(self):
        return OrderInstance.objects.filter(status__exact='').order_by('due_back')


def create_order(request, pk):
    #  Функция просмотра для обновления определенного BookInstance библиотекарем
    order_inst = get_object_or_404(OrderInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RegisterOrderForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            # (здесь мы просто присваиваем их полю due_back)
            order_inst.due_back = form.cleaned_data['renewal_date']
            order_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('my-order'))

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RegisterOrderForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'studio/order_create.html', {'form': form, 'order_inst': order_inst})


class OrderCreate(CreateView):
    model = Order
    fields = '__all__'


class OrderUpdate(UpdateView):
    model = OrderInstance
    fields = ['id', 'order', 'summary', 'customer_order']
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
