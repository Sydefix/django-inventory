from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category
from config.settings import LOW_QUANTITY
from django.contrib import messages

class Index(TemplateView):
	template_name = 'inventory/index.html'

class Stock(LoginRequiredMixin, View):
	def get(self, request):
		items = InventoryItem.objects.all().order_by('id')

		return render(request, 'inventory/stock.html', {'items': items})

class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'inventory/signup.html', {'form': form})

class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('stock')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('stock')

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('stock')
	context_object_name = 'item'

# Todo: dashboard( some recent, some analytics and some tables) 
# credit, factures, invoices(sales, purchases,), analytics, excel order generators

