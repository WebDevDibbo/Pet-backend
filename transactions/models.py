from django.db import models
from users.models import UserProfileModel

# Create your models here.

TRANSACTIONS_TYPES = [
    ('deposit','Deposit'),
    ('adoption','Adoption Payment')
]

class Transaction(models.Model): # transaction is many part
    user = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTIONS_TYPES)
    balance_after_transaction = models.DecimalField(max_digits=10,decimal_places=2) 

    def __str__(self):
        return f'{self.user.user.username} - {self.transaction_type}'