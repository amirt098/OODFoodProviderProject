import random
import string
from tqdm import tqdm

from django.utils.translation import ugettext_lazy as _
from django.core.management.base import BaseCommand

from apps.logistic.models import Driver
from apps.accounts.models import (
    UserRole,
    User,
    Address,
)


class Command(BaseCommand):
    help = _('Generate Users')

    def add_arguments(self, parser):

        parser.add_argument('--total-custommer', '-nC', type=int,
                            help='Total number of custommer')
        parser.add_argument('--total-driver', '-nD', type=int,
                            help='Total number of drivers')

    def handle(self, *args, **kwargs):
        total_custommers = kwargs.get('total_custommer') or 500
        total_drivers = kwargs.get('total_driver') or 100

        custommers, drivers = self.create_users(total_custommers, total_drivers)

        self.stdout.write(self.style.SUCCESS(
            f'{total_custommers} custommers and {total_drivers} drivers were created successfully.'))

    def create_custommers(self, total_custommers: int, total_drivers: int, *args, **kwargs):
        print(f'!!! GENERATING {total_custommers} USERS !!!')
        users = [
            User(
                phone_number= '09' + str(index) + '0' * (9-len(str(index))),
                role= UserRole.CUSTOMER,
                uid= str(index),
                username= f'username-{index}',
                email= f"{index}@gmail.com",
                first_name= "ali-{index}",
                last_name= "alizade-{index}",
            )
            for index in tqdm(range(total_custommers))
        ]
        User.objects.bulk_create(users)

        total_drivers = min(total_custommers, total_drivers)
        print(f'!!! GENERATING {total_drivers} PROFILES !!!')
        drivers = [
            Driver(
                uid=f'{index}',
                user=users[index],
                plate_number=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            )

            for index in tqdm(range(total_drivers))
        ]
        Driver.objects.bulk_create(drivers)

        print(f'!!! GENERATING {total_custommers*2} ADDRESSES !!!')
        addresses = [
            Address(
                user=users[index//2],
                title=f'Address-{index}',
                state='Tehran',
                city='Tehran',
                postal_code=''.join(random.choices(string.digits, k=10))
            ) for index in tqdm(range(total_custommers*2))
        ]
        Address.objects.bulk_create(addresses)
