from django.db import models, connection
from django.urls import reverse


class Invoice(models.Model):
    invoiceid = models.BigIntegerField(db_column='InvoiceId', primary_key=True)  # Field name made lowercase.
    invoiceactive = models.BooleanField(db_column='InvoiceActive')  # Field name made lowercase.
    customername = models.CharField(db_column='CustomerName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    customerid = models.CharField(db_column='CustomerId', max_length=10, blank=True, null=True)  # Field name made lowercase.
    customerphone = models.CharField(db_column='CustomerPhone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    customeraddress = models.CharField(db_column='CustomerAddress', max_length=150, blank=True, null=True)  # Field name made lowercase.
    invoicedate = models.DateField(db_column='InvoiceDate')  # Field name made lowercase.
    inithour = models.CharField(db_column='InitHour', max_length=50)  # Field name made lowercase.
    endhour = models.CharField(db_column='EndHour', max_length=50)  # Field name made lowercase.
    chosenrate = models.ForeignKey('Rate', models.DO_NOTHING, db_column='ChosenRate')  # Field name made lowercase.
    tax = models.IntegerField(db_column='Tax', blank=True, null=True)  # Field name made lowercase.
    total = models.DecimalField(db_column='Total', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    paymenttype = models.ForeignKey('Paymenttype', models.DO_NOTHING, db_column='PaymentType')  # Field name made lowercase.
    customeremail = models.CharField(db_column='CustomerEmail', max_length=75, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Invoice'

    def get_invoice_id(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT NEXT VALUE FOR Invoice_Sequence")
            invoiceid = int(str(cursor.fetchone()[0]))
            return invoiceid

    def get_absolute_url_print(self):
        return reverse("home:print-invoice", kwargs={"invoiceid": self.invoiceid})

    def get_abosulte_url_ajax_deactivate(self):
        return reverse("home:ajax-deactivate-invoice", kwargs={'invoiceid':self.invoiceid})

    def get_absolute_url_detail(self):
        return reverse("home:detail-invoice", kwargs={'invoiceid':self.invoiceid})



class Paymenttype(models.Model):
    paymentid = models.AutoField(db_column='PaymentId', primary_key=True)  # Field name made lowercase.
    paymentname = models.CharField(db_column='PaymentName', max_length=25)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PaymentType'

    def __str__(self):
        return self.paymentname



class Rate(models.Model):
    rateid = models.AutoField(db_column='RateId', primary_key=True)  # Field name made lowercase.
    ratename = models.CharField(db_column='RateName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    rateprice = models.IntegerField(db_column='RatePrice', blank=True,
                                    null=True)  # Field name made lowercase.
    ratetime = models.IntegerField(db_column='RateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Rate'

    def get_absolute_url_edit(self):
        return reverse("home:edit-rate", kwargs={"id": self.rateid})

    def get_absolute_url_delete(self):
        return reverse("home:ajax-remove-rate", kwargs={'rateid':self.rateid})

    def __str__(self):
        return self.ratename


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

    def get_absolute_url_edit(self):
        return reverse("home:edit-user", kwargs={"id": self.id})

    def get_absolute_url_change_password(self):
        return reverse("home:password-change", kwargs={"id":self.id})

    def get_absolute_url_delete(self):
        return reverse("home:ajax-remove-user", kwargs={"userid":self.id})


class Company(models.Model):
    companyid = models.CharField(db_column='CompanyID', primary_key=True, max_length=20)  # Field name made lowercase.
    companyname = models.CharField(db_column='CompanyName', max_length=100)  # Field name made lowercase.
    companyphone = models.CharField(db_column='CompanyPhone', max_length=50)  # Field name made lowercase.
    companyaddress = models.CharField(db_column='CompanyAddress', max_length=250)  # Field name made lowercase.
    companyelectronicinvoicecode = models.CharField(db_column='CompanyElectronicInvoiceCode', max_length=300, blank=True, null=True)  # Field name made lowercase.
    companyemail = models.CharField(db_column='CompanyEmail', max_length=254, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Company'

    def get_absolute_url_edit(self):
        return reverse("home:edit-company", kwargs={"companyid":self.companyid})

    def get_absolute_url_detail(self):
        return reverse("home:detail-company")
