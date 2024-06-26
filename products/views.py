from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory

# Create your views here.
# функции = контроллеры = вьюхи = обработка запроса


class IndexView(TitleMixin, TemplateView):
    template_name = "products/index.html"
    title = "Store"


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 3
    title = "Store - Каталог"

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get("category_id")  # None if key does not exist
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        categories = cache.get("categories")
        if not categories:
            context["categories"] = ProductCategory.objects.all()
            cache.set("categories", context["categories"], 30)
        else:
            context["categories"] = categories
        return context


@login_required
def basket_add(request, product_id):
    Basket.create_or_update(product_id=product_id, user=request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class BasketsListView(TitleMixin, ListView):
    model = Basket
    template_name = "products/baskets_sep.html"

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.object.id,))
