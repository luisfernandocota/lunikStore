from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db.models import Prefetch
from panel.products.forms import CouponForm, CouponProductForm

from panel.products.models import Coupon, Product, CouponProduct

def coupons_list(request):
    context = {}

    context['coupons_list'] = Coupon.objects.filter(status=True)

    return render(request, 'coupons/coupons_list.html', context)

def coupons_add(request):
    context = {}

    if request.method == 'POST':
        context['coupon_form'] = CouponForm(request.POST)
        coupon_product_form = CouponProductForm(request.POST, products=None)
        # Get list of table products
        result = [i.split('-') for i in request.POST if i.startswith('PROD-')]

        if result:
            index = []
            for r in result:
                index.append(r[1])
            products = Product.objects.filter(pk__in=index)

        if context['coupon_form'].is_valid():
            coupon = context['coupon_form'].save()
            if result:
                for product in products:
                    CouponProduct.objects.get_or_create(coupon=coupon, product=product)
            return redirect('products:coupons_list')
            
    else:
        context['coupon_form'] = CouponForm()
        context['coupon_product_form'] = CouponProductForm(products=None)

    return render(request, 'coupons/coupons_form.html', context)

def coupons_edit(request, coupon_pk):
    context = {}



    context['coupon_obj'] = get_object_or_404(Coupon, pk=coupon_pk)
    context['coupon_products_list'] = CouponProduct.objects.filter(coupon=context['coupon_obj'])
    if request.method == 'POST':
        context['coupon_form'] = CouponForm(request.POST, instance=context['coupon_obj'])
        # coupon_product_form = CouponProductForm(request.POST, request=request)
        # Get list of table products
        result = [i.split('-') for i in request.POST if i.startswith('PROD-')]
        if result:
            index = []
            for r in result:
                index.append(r[1])
            store_products = Product.objects.filter(pk__in=index)

        if context['coupon_form'].is_valid():
            coupon = context['coupon_form'].save()

            if result:
                for product in store_products:
                    CouponProduct.objects.get_or_create(coupon=coupon, product=product)
            return redirect('products:coupons_list')
            
    else:
        context['coupon_form'] = CouponForm(instance=context['coupon_obj'])
        context['coupon_product_form'] = CouponProductForm(products=context['coupon_products_list'])
    return render(request, 'coupons/coupons_form.html', context)


@csrf_exempt
def get_product(request):
    data = {}
    if request.is_ajax() and request.method == 'POST':
        product_pk = request.POST.get('product_pk')
        # product = serializers.serialize("json",StoreProduct.objects.get(pk=product_pk), use_natural_foreign_keys=True)
        try:
            product = Product.objects.get(pk=product_pk)
            # storeProduct = serializers.serialize("json", [product] , use_natural_foreign_keys=True)
            data['product'] = {
                'pk' : product.pk,
                'name': product.name, 
                'image': product.products_gallery.first().image.url,
                'price': product.products_properties.sell_price,
                'brandModel': '%s-%s' %(product.brand,product.model)
                }
            return JsonResponse(data, safe=False)

        except Product.DoesNotExist as e:
            return JsonResponse({'result': str(e)})

def delete_coupon_product(request, coupon_pk):
    from panel.core.utils import delete_item
    data = {}
    coupon_product = CouponProduct.objects.get(pk=coupon_pk)

    data = delete_item(request, coupon_product, '/panel/products/coupons/delete_product/', 'Producto quitado del cupón')
    data['url_redirect'] = reverse('products:coupons_edit',kwargs={'coupon_pk':coupon_product.coupon.pk})
    return JsonResponse(data, safe=True)
