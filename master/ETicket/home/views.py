import os
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView, CreateView
from .forms import RateForm, InvoiceForm, AuthUserForm, CompanyForm, AuthUserUpdateForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Rate, Invoice, AuthUser, Company
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.conf import settings
from django.db import connection
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.hashers import make_password


#region Report PDF methods

def link_callback(uri, rel):

    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def render_pdf_view(request, **kwargs):
    content = request.POST.get('content', '')
    template_path = 'home/invoice/report_pdf.html'
    context = {'content': content, 'h':5}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#endregion

#region Home

class DashboardView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def post(self, request):
        return render(request, 'home/Home.html')

    def get(self, request):
        return render(request, 'home/Home.html')

#endregion

# region Rate


class CreateRateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('is_superuser')
    login_url = settings.LOGIN_URL
    template_name = "home/rate/edit.html"
    model = Rate
    form_class = RateForm
    success_url = '/home/list_rate/'


class EditRateView(LoginRequiredMixin, PermissionRequiredMixin ,UpdateView):
    permission_required = ('is_superuser')
    login_url = settings.LOGIN_URL

    template_name = "home/rate/edit.html"
    form_class = RateForm
    success_url = "/home/list_rate/"

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Rate, rateid=id_)

    def get_context_data(self, **kwargs):
        context = super(EditRateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = RateForm(self.request.POST, instance=self.object)

        else:
            context['form'] = RateForm(instance=self.object)
        return context


class ListRateView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('is_superuser')
    login_url = settings.LOGIN_URL

    model = Rate
    template_name = "home/rate/list.html"


# endregion

# region Invoice

class ListInvoiceView(LoginRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
    model = Invoice
    template_name = "home/invoice/list.html"
    queryset = Invoice.objects.all()
   

class CreateInvoiceView(LoginRequiredMixin, CreateView):
    login_url = settings.LOGIN_URL

    template_name = "home/invoice/create.html"
    model = Invoice
    form_class = InvoiceForm
    success_url = '/home/list_invoice/'


class PrintInvoiceView(LoginRequiredMixin, DetailView):
    login_url = settings.LOGIN_URL
    template_name = "home/invoice/print.html"
    model = Invoice

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("invoiceid")
        return get_object_or_404(Invoice, invoiceid=id_)

    def get_context_data(self, **kwargs):
         context = super(PrintInvoiceView, self).get_context_data(**kwargs)
         context['company'] = Company.objects.get()
         return context


class DetailInvoiceView(LoginRequiredMixin, DetailView):
    login_url = settings.LOGIN_URL
    template_name = "home/invoice/detail.html"
    model = Invoice

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("invoiceid")
        return get_object_or_404(Invoice, invoiceid=id_)

    def get_context_data(self, **kwargs):
         context = super(DetailInvoiceView, self).get_context_data(**kwargs)
         return context


class InvoiceReportView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ("is_superuser")
    login_url = settings.LOGIN_URL
    template_name = "home/invoice/report.html"
    model = Invoice

    def post(self):
        print("hello")
        return redirect("home:list-invoice")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InvoiceReportView, self).get_context_data(**kwargs)
        from_date = self.kwargs.get('fromDate')
        to_date = self.kwargs.get('toDate')
        object_list = Invoice.objects.filter(invoiceactive = True, invoicedate__range=(str(from_date), str(to_date)))
        total = Invoice.objects.filter(invoiceactive = True, invoicedate__range=(str(from_date), str(to_date))).aggregate(Sum('total'))['total__sum']
        total_cash = object_list.aggregate(cash=Count('paymenttype',filter=Q(paymenttype=1)))['cash']
        total_card = object_list.aggregate(card=Count('paymenttype',filter=Q(paymenttype=2)))['card']
        invoice_quantity = object_list.aggregate(quantity=Count('invoiceid'))['quantity']

        total_cash_perc = (total_cash/invoice_quantity)*100
        total_card_perc = (total_card/invoice_quantity)*100

        context['object_list'] = object_list
        context['report_total'] = total
        context['from_date'] = from_date
        context['to_date'] = to_date
        context['total_cash'] = total_cash
        context['total_cash_perc'] = total_cash_perc
        context['total_card'] = total_card
        context['total_card_perc'] = total_card_perc
        context['invoice_quantity'] = invoice_quantity
        return context
    

# endregion

# region User

class ListAuthUserView(LoginRequiredMixin, PermissionRequiredMixin ,ListView):
    permission_required = ('is_superuser')
    login_url = settings.LOGIN_URL

    model = AuthUser
    template_name = "home/user/list.html"


class CreateAuthUserView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = ('is_superuser')
    login_url = settings.LOGIN_URL
    template_name = "home/user/create.html"
    model = AuthUser
    form_class = AuthUserForm
    success_url = "/home/list_user/"


class EditAuthUserView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = ('is_superuser')
    login_url = settings.LOGIN_URL
    template_name = "home/user/edit.html"
    form_class = AuthUserUpdateForm
    success_url = "/home/list_user/"


    def get_object(self, queryset=None):
        id_ = self.kwargs.get("id")
        return get_object_or_404(AuthUser, id=id_)


    def get_context_data(self, **kwargs):
        context = super(EditAuthUserView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = AuthUserForm(self.request.POST, instance=self.object)
        else:
            context['form'] = AuthUserForm(instance=self.object)
        return context


class PasswordChangeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('is_superuser')
    login_url = settings.LOGIN_URL

    def post(self, request, **kwargs):
        return render(request, 'home/user/password_change.html')

    def get(self, request, **kwargs):
        id_ = self.kwargs.get("id")
        user = get_object_or_404(AuthUser, id=id_)
        context = {
            'changePasswordUser':user
        }
        return render(request, 'home/user/password_change.html', context)

# endregion

#region Company

class DetailCompanyView(LoginRequiredMixin, PermissionRequiredMixin,DetailView):
    permission_required = ('is_superuser')
    login_url = settings.LOGIN_URL
    model = Company
    template_name = 'home/company/detail.html'

    def get_object(self, queryset=None):
        companyid = ''
        with connection.cursor() as cursor:
            cursor.execute("SELECT CompanyID FROM Company")
            companyid = str(cursor.fetchone()[0])
        return get_object_or_404(Company, companyid=companyid)

class EditCompanyView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = ('is_superuser')
    login_url = settings.LOGIN_URL
    model = Company
    form_class = CompanyForm
    template_name = 'home/company/edit.html'
    success_url = '/home/detail_company/'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get("companyid")
        return get_object_or_404(Company, companyid=id_)

    def get_context_data(self, **kwargs):
        context = super(EditCompanyView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CompanyForm(self.request.POST, instance=self.object)

        else:
            context['form'] = CompanyForm(instance=self.object)
        return context

#endregion

# region AJAX

def ajax_get_rateprice(request, **kwargs):
    rate = Rate.objects.get(rateid=request.POST.get('rateid', ''))
    data = {
        'rateprice': rate.rateprice,
        'ratetime': rate.ratetime,
        'ratename': rate.ratename
    }
    return HttpResponse(JsonResponse(data), content_type="application/json")

def ajax_get_firstinvoicedate(request, **kwargs):
    invoice = Invoice.objects.all().order_by('invoicedate')[0]
    data = {
        'first_invoicedate': invoice.invoicedate
    }
    return HttpResponse(JsonResponse(data), content_type="application/json")


def ajax_generate_report(request, **kwargs):
    from_date = request.POST.get('fromDate', '')
    to_date = request.POST.get('toDate', '')
    url = reverse("home:report-invoice", kwargs={"fromDate":from_date, "toDate":to_date})
    data = {
       'url' : url
    }
    return HttpResponse(JsonResponse(data), content_type="application/json")

def ajax_deactivate_invoice(request, **kwargs):
    invoiceid = kwargs.get('invoiceid')
    invoice = Invoice.objects.get(invoiceid=invoiceid)
    invoice.invoiceactive = False
    invoice.save()
    message = "Done"
    data = {
        'message':message
    }
    return redirect("home:list-invoice")

def ajax_change_user_password(request, **kwargs):
    userid = request.POST.get('userid', '')
    password = request.POST.get('password', '')
    user = get_object_or_404(AuthUser, id=userid)
    user.password = make_password(password)
    user.save()
    url = reverse("home:list-user")
    data = {
        'url': url
    }
    return HttpResponse(JsonResponse(data), content_type="application/json")

def ajax_remove_rate(request, **kwargs):
    rateid = kwargs.get('rateid')
    Rate.objects.get(rateid=rateid).delete()
    return redirect("home:list-rate")

def ajax_remove_user(request, **kwargs):
    userid = kwargs.get('userid')
    AuthUser.objects.get(id=userid).delete()
    return redirect("home:list-user")

def ajax_get_dashboard_data(request, **kwargs):
    date = request.POST.get('date')
    object_list = Invoice.objects.filter(invoiceactive=True, invoicedate=(date))
    if(object_list):
        total_cash = object_list.aggregate(cash=Count('paymenttype', filter=Q(paymenttype=1)))['cash']
        total_card = object_list.aggregate(card=Count('paymenttype', filter=Q(paymenttype=2)))['card']
        invoice_quantity = object_list.aggregate(quantity=Count('invoiceid'))['quantity']
        total = int(object_list.aggregate(total=Sum('total'))['total'])
    else:
        total_card = 0
        total_cash = 0
        invoice_quantity = 0
        total = 0

    data = {
        'total_cash':total_cash,
        'total_card':total_card,
        'total_invoices':invoice_quantity,
        'total':total,
        'data': [int(total_cash), int(total_card)],
        'labels': ['Efectivo', 'Tarjeta'],
    }
    return JsonResponse(data)
#endregion