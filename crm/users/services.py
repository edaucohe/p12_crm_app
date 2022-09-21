from users.models import User
from customers.models import Customer


def can_user_edit_customer(customer: Customer, user: User) -> bool:
    if User.role == 'SALE':
        return customer.objects.filter(user=user).exists()
    else:
        return False
