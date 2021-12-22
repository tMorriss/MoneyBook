from django.contrib import admin

from .models import (BankBalance, Category, CheckedDate, CreditCheckedDate,
                     Data, Direction, Method, SeveralCosts)

admin.site.register(Direction)
admin.site.register(Method)
admin.site.register(Category)
admin.site.register(Data)
admin.site.register(CheckedDate)
admin.site.register(CreditCheckedDate)
admin.site.register(BankBalance)
admin.site.register(SeveralCosts)
