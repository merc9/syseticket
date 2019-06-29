from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.urls import path


from .views import (
    DashboardView,
    EditRateView,
    ListRateView,
    CreateRateView,
    CreateInvoiceView,
    CreateAuthUserView,
    ListAuthUserView,
    EditAuthUserView,
    PasswordChangeView,
    PrintInvoiceView,
    ListInvoiceView,
    DetailCompanyView,
    EditCompanyView,
    InvoiceReportView,
    DetailInvoiceView,
    ajax_get_rateprice,
    ajax_get_firstinvoicedate,
    ajax_generate_report,
    ajax_deactivate_invoice,
    render_pdf_view,
    ajax_change_user_password,
    ajax_remove_rate,
    ajax_remove_user,
    ajax_get_dashboard_data,
)


app_name = "home"

urlpatterns = [


    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('list_rate/', ListRateView.as_view(), name="list-rate"),
    path('create_rate/', CreateRateView.as_view(), name="create-rate"),
    path('<int:id>/edit_rate/', EditRateView.as_view(), name="edit-rate"),

    path('create_invoice/', CreateInvoiceView.as_view(), name="create-invoice"),
    path('list_invoice/', ListInvoiceView.as_view(), name="list-invoice"),
    path('<int:invoiceid>/print_invoice/', PrintInvoiceView.as_view(), name="print-invoice"),
    path('<str:fromDate>/<str:toDate>/invoice_report/', InvoiceReportView.as_view(), name="report-invoice"),
    path('<int:invoiceid>/invoice_detail/', DetailInvoiceView.as_view(), name="detail-invoice"),

    path('create_user/', CreateAuthUserView.as_view(), name="create-user"),
    path('list_user/', ListAuthUserView.as_view(), name="list-user"),
    path('<int:id>/edit_user/', EditAuthUserView.as_view(), name="edit-user"),
    path('<int:id>/password_change/',PasswordChangeView.as_view(),name="password-change"),

    path('<str:companyid>/edit_company/', EditCompanyView.as_view(), name="edit-company"),
    path('detail_company/', DetailCompanyView.as_view(), name="detail-company"),

    path('ajax_get_rateprice', ajax_get_rateprice, name="ajax-get-rateprice"),
    path('ajax_get_dashboard_data', ajax_get_dashboard_data, name="ajax-get-dashboard-data"),
    path('ajax_get_firstinvoicedate', ajax_get_firstinvoicedate, name="ajax-get-firstinvoicedate"),
    path('ajax_generate_report', ajax_generate_report, name="ajax-generate-report"),
    path('<int:invoiceid>/ajax_deactivate_invoice', ajax_deactivate_invoice, name="ajax-deactivate-invoice"),
    path('ajax_change_user_password', ajax_change_user_password, name="ajax-change-user-password"),
    path('<int:rateid>/ajax_remove_rate', ajax_remove_rate, name="ajax-remove-rate"),
    path('<int:userid>/ajax_remove_user', ajax_remove_user, name="ajax-remove-user"),
    path("report_pdf/",render_pdf_view, name="pdf-report"),


]
