# -*- coding: utf-8 -*-
import os
from datetime import datetime
from urllib import request


#import weasyprint

import stripe 
import logging  
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import FileSystemStorage,Storage
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail, BadHeaderError,EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from panel.config.models import Logger
logger = logging.getLogger(__name__)
#-- Rename filename with datetime format
def get_filename(extension):
    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return '%s%s' % (ts, extension)

#-- Sendmail with html template
def sendmail(subject, html_content, from_email, to_email):
    #-- Sendmail: (Subjetc, body, email user, email host, False)

    try:
        #msg = EmailMessage(subject, html_content, from_email, [to_email])
        if type(to_email) == list:
            msg = EmailMultiAlternatives(subject, html_content, from_email, to_email)
        else:
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to_email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send(fail_silently=True)
    except BadHeaderError:
        return HttpResponse('Error al enviar el correo')
    return True

#-- Sendmail with html template and attachments
# def sendmail_attachs(subject, html_content, from_email, to_email, files):
#     #-- Sendmail: (Subjetc, body, email user, email host, False)
#     try:
#         files_list = []

#         for k, f in files.items():

#             files_list.append((f.name,f.read(),magic.from_buffer(f.read(), mime=True)))

#         msg = EmailMessage(subject, html_content, from_email, [to_email],attachments=files_list)
#         msg.content_subtype = "html"  # Main content is now text/html
#         msg.send(fail_silently=True)
#     except BadHeaderError:
#         return HttpResponse('Error al enviar el correo')
#     return True

def pagination(instance, page, num):
    paginator = Paginator(instance, num)

    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)

    return obj_list

def user_logs(request,user,logtype,message):

    if user is None:
        user = request.user

    log = Logger.objects.create(user=user,ip=request.get_host(),\
                                sessionkey=request.COOKIES.get(settings.SESSION_COOKIE_NAME,''),
                                logtype=logtype,user_agent=request.META['HTTP_USER_AGENT'],message=message,url=request.path)

    return log

def delete_record(request,instance,url_redirect,url_post):

    context = {}
    data = {}

    if request.is_ajax and request.method == 'POST':
        instance.status = False
        instance.save()

        messages.success(request, 'Registro eliminado satisfactoriamente')

        #-- User Logs (Info, Access, Error)
        user_logs(request,None,'I','Registro eliminado satisfactoriamente')

        data['form_is_valid'] = True
        data['url_redirect'] = url_redirect
    else:
    #-- Parameters modal form
        context['url_post'] = url_post
        data['form_is_valid'] = False
        data['html_form'] = render_to_string('core/snippets/modal_delete.html', context, request=request)

    return data

def sendmail_activation_record(request,instance,password,url_redirect,url_post):

    context = {}
    data = {}

    if request.is_ajax and request.method == 'POST':

        #-- Call static method
        instance.activation_email(request,instance,password)

        messages.success(request, 'Correo de activación enviado satisfactoriamente')

        #-- User Logs (Info, Access, Error)
        user_logs(request,None,'I','Correo de activación enviado satisfactoriamente')

        data['form_is_valid'] = True
        data['url_redirect'] = url_redirect
    else:
        #-- Parameters modal form
        context['url_post'] = url_post

        data['html_form'] = render_to_string('core/snippets/modal_sendmail.html', context, request=request)

    return data

def delete_item(request,instance,url_redirect, url_post, message):
    context = {}
    data = {}

    if request.is_ajax and request.method == 'POST':
        data['obj_pk'] = instance.pk

        instance.delete()

        messages.success(request, message)

        #-- User Logs (Info, Access, Error)
        user_logs(request,None,'I',message)

        data['form_is_valid'] = True
        data['url_redirect'] = url_redirect

    else:

    #-- Parameters modal form
        context['obj_delete'] = instance
        context['url_post'] = url_post

        data['html_form'] = render_to_string('core/snippets/modal_delete.html', context, request=request)

    return data

def delete_item_store(request,instance,namespace,message):
    context = {}
    data = {}

    if request.is_ajax and request.method == 'POST':
        data['obj_pk'] = instance.pk

        instance.status = False
        instance.save()

        messages.success(request, message)

        #-- User Logs (Info, Access, Error)
        user_logs(request,None,'A',message)

        data['form_is_valid'] = True
        #data['url_redirect'] = url

    else:   

        #-- Parameters modal form
        context['obj_delete'] = instance
        context['url_post'] = namespace

        data['html_delete'] = render_to_string('core/snippets/modal_delete.html', context, request=request)

    return data

# Util view
def filters_by_request(request):
    filters = {}

    pending = request.GET.get('pending')
    process = request.GET.get('process')
    send = request.GET.get('send')
    delivered = request.GET.get('delivered')


    if pending == 'true':
        filter_pending = 'order_payment__status__icontains'
        filters[filter_pending] = 'PE'
    if process == 'true':
        filter_process = 'order_payment__status__icontains'
        filters[filter_process] = 'EP'
    if send == 'true':
        filter_send = 'order_payment__status__icontains'
        filters[filter_send] = 'EE'
    if delivered == 'true': 
        filter_delivered = 'order_payment__status__icontains'
        filters[filter_delivered] = 'EN'

    return filters

# def export_xls_file(filename,sheet,headers,qs):
#     response = HttpResponse(content_type='application/ms-excel')
#     #-- File name
#     response['Content-Disposition'] = 'attachment; filename="%s.xls"' % (filename)
#     #-- Add Workbook and sheet
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet(sheet)

#     # Sheet header, first row
#     row_num = 0
#     #-- Headers Style
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     #-- Header in the first row
#     columns = headers

#     #-- Create Headers
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     font_style = xlwt.XFStyle()

#     #-- Set Queryset to rows
#     rows = qs
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)

#     return response

