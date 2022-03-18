# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings

from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta

import json
import datetime
import stripe

from panel.accounts.models import User, Role
from portal.cover.forms import UserForm, ContactForm
#from panel.stores.models import StripeCustomer
#from panel.stores.forms import StoreForm
#from panel.resellers.forms import ResellerExecutiveForm
#from panel.resellers.models import Director
#from panel.tenants.models import  Tenant
#from panel.website.models import StoreMeta, Info, StripeKey
from panel.core.utils import user_logs, sendmail

# Create your views here.
def index(request):
    context = {}

    return render(request,'shop/shop_list.html',context)

