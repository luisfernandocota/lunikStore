# -*- coding: utf-8 -*-
from django.urls import reverse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Prefetch

from panel.core.utils import user_logs,delete_record, delete_item
from panel.products.models import Product, ProductHexaCodeM2M, ProductGallery,ProductProperty
from panel.products.forms import ProductForm, ProductSizeForm, ProductColorForm, ProductPropertyForm


# Create your views here.
def products_list(request):
    context = {}

    context['products_list'] = Product.objects.prefetch_related(Prefetch('hexacodes_m2m',queryset=ProductHexaCodeM2M.objects.select_related('hexacode').filter(status=True)))\
                                   .filter(status=True).order_by('name')

    return render(request,'products/products_list.html',context)

def add_product(request):
    context = {}
    if request.method == 'POST':
        files=request.FILES
        context['product_form'] = ProductForm(request.POST, request.FILES)
        if context['product_form'].is_valid():

            product = context['product_form'].save()
            ProductProperty.objects.create(product=product)
            if request.FILES:
                for obj in files:
                    ProductGallery.objects.create(image=files[obj], product=product)
            
            #-- Message to user
            messages.success(request, 'Producto creado satisfactoriamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Producto creado satisfactoriamente')

            return redirect('products:products_list')
    else:
        context['product_form'] = ProductForm()
    return render(request, 'products/products_form.html', context)

def edit_product(request, product_slug):
    context = {}
    context['product_obj'] = get_object_or_404(Product.objects.prefetch_related('products_gallery'), slug=product_slug, status=True)
    product_property = get_object_or_404(ProductProperty, product=context['product_obj'])
    if request.method == 'POST':
        context['product_properties_form'] = ProductPropertyForm(request.POST, request.FILES, instance=product_property)
        context['product_form'] = ProductForm(request.POST, request.FILES, instance=context['product_obj'])

        files=request.FILES

        if context['product_form'].is_valid() and context['product_properties_form'].is_valid():
            product = context['product_form'].save()
            property = context['product_properties_form'].save()
            for obj in files:
                ProductGallery.objects.create(image=files[obj], product=product)
            messages.success(request, 'El producto ha sido modificado satisfactoriamente')

            return redirect('products:products_list')
        

    else:
        hexacodes_ids = context['product_obj'].hexacodes_m2m.values('hexacode').filter(status=True)
        context['product_properties_form'] = ProductPropertyForm(instance=product_property)
        context['product_form'] = ProductForm(instance=context['product_obj'], initial={'sizes':context['product_obj'].sizes.all(),\
                                                                                      'hexacodes':context['product_obj'].hexacodes.filter(pk__in=hexacodes_ids,status=True)})

    return render(request, 'products/products_form.html', context)


def info_product(request, product_slug):
    context = {}
    data = {}
    if request.is_ajax() and request.method == 'GET':
        context['product'] = get_object_or_404(Product.objects.prefetch_related('products_gallery'), slug=product_slug,status=True)
        
        data['html_form'] = render_to_string('products/modals/product_info.html', context, request=request)

    return JsonResponse(data)

def delete_product(request, product_slug):
    data = {}
    product = get_object_or_404(Product.objects.prefetch_related('products_gallery'), slug=product_slug,status=True)
    data = delete_record(request,product,'/panel/products/','/panel/products/delete/%s' %(product.slug))
    return JsonResponse(data)

def delete_product_image(request, product_slug, pk):
    data = {}
    product_image = get_object_or_404(ProductGallery, pk=pk)
    data = delete_item(request,product_image,'/panel/products/edit/%s' %(product_slug),'/panel/products/delete/product/%s/image/' %(product_slug), 'Objeto eliminado correctamente')
    return JsonResponse(data)


def add_size(request):
    context = {}
    data = {}

    if request.is_ajax() and request.method == 'POST':
        context['size_form'] = ProductSizeForm(request.POST)

        if context['size_form'].is_valid():
            context['size_form'].save()

            messages.success(request, 'Registro agregado correctamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Registro agregado correctamente')

            data['form_is_valid'] = True
            data['html_success'] = render_to_string('core/snippets/success_modal.html', context, request=request)
        else:
            data['form_is_valid'] = False
            data['html_failed'] = render_to_string('core/snippets/success_modal.html', context, request=request)
        
    else:
        context['size_form'] = ProductSizeForm()
        context['name_form'] = 'Agregar tamaño'
    #-- Parameters modal form
        context['url_post'] = '/panel/products/add/size'
        data['form_is_valid'] = False
        
        data['html_form'] = render_to_string('products/modals/size_form.html', context, request=request)

    return JsonResponse(data)

def add_hexacode(request):
    context = {}
    data = {}

    if request.is_ajax() and request.method == 'POST':
        context['hexacodes_form'] = ProductColorForm(request.POST)

        if context['hexacodes_form'].is_valid():
            context['hexacodes_form'].save()

            messages.success(request, 'Registro agregado correctamente')

            #-- User Logs (Info, Access, Error)
            user_logs(request,None,'I','Registro agregado correctamente')

            data['form_is_valid'] = True
            data['html_success'] = render_to_string('core/snippets/success_modal.html', context, request=request)
        else:
            data['form_is_valid'] = False
            data['html_failed'] = render_to_string('core/snippets/success_modal.html', context, request=request)
        
    else:
        context['hexacodes_form'] = ProductColorForm()
        context['name_form'] = 'Agregar color'
    #-- Parameters modal form
        context['url_post'] = '/panel/products/add/color'
        data['form_is_valid'] = False
        
        data['html_form'] = render_to_string('products/modals/hexacodes_form.html', context, request=request)

    return JsonResponse(data)
