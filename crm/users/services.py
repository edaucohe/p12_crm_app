from users.models import User
from customers.models import Customer


def is_management_team_user(user: User) -> bool:
    return True if user.role == User.Role.MANAGEMENT else False


def is_sale_team_user(user: User) -> bool:
    return True if user.role == User.Role.SALE else False


def is_a_customer_assigned(user: User, customer: Customer) -> bool:
    return True if user.pk == customer.user.pk else False


def is_support_team_user(user: User) -> bool:
    return True if user.role == User.Role.SUPPORT else False
