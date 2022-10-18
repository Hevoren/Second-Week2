from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import RegisterUserForm, RegisterOrderForm
from django.urls import reverse_lazy
from .models import User, Order
from django.views.generic.base import TemplateView
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse


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
    template_name = 'studio/order_list_customer_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(customer_order=self.request.user)


class LoanedOrdersAllListView(PermissionRequiredMixin, generic.ListView):
    model = Order
    permission_required = 'catalog.can_mark_returned'
    template_name = 'studio/order_list_customer_all.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.all()


class OrderCreate(CreateView):
    model = Order
    fields = ['name', 'summary', 'category', 'photo_file']

    def form_valid(self, form):
        form.instance.customer_order = self.request.user
        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = ['status']
    permission_required = 'catalog.can_mark_returned'


class OrderUserDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('my-order')


class OrderAdminDelete(PermissionRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('all-order')
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
