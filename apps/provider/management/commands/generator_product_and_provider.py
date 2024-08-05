# apps/provider/management/commands/create_demo_data.py
import uuid

from django.core.management.base import BaseCommand
from apps.provider.models import Provider, Product, Category
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Create demo data for providers and products'

    def handle(self, *args, **kwargs):
        # Create some users for the providers
        users = []
        for i in range(1, 6):
            user = User.objects.create_user(
                username=f'manager{i}{str(uuid.uuid4())}',
                email=f'manager{i}@example.com',
                password='password',
                uid=str(uuid.uuid4())
            )
            users.append(user)

        # Create providers (restaurants)
        providers = []
        for i, user in enumerate(users, 1):
            provider = Provider.objects.create(
                uid=f'prov{i}',
                manager=user,
                name=f'Restaurant {chr(64 + i)}',  # Generates names like Restaurant A, Restaurant B, etc.
                is_available=True
            )
            providers.append(provider)

        # Create categories
        category1 = Category.objects.create(uid='cat1', title='Main Course')
        category2 = Category.objects.create(uid='cat2', title='Desserts')

        # Sample product data
        product_titles = [
            'Pizza', 'Burger', 'Pasta', 'Salad', 'Sandwich',
            'Soup', 'Steak', 'Chicken Wings', 'Sushi', 'Taco',
            'Ice Cream', 'Cake', 'Pie', 'Pudding', 'Brownie',
            'Cookie', 'Donut', 'Muffin', 'Cupcake', 'Cheesecake'
        ]

        product_descriptions = [
            'Delicious', 'Tasty', 'Yummy', 'Scrumptious', 'Mouth-watering'
        ]

        # Create products (food items)
        for i, title in enumerate(product_titles, 1):
            description = f'{title} - {product_descriptions[i % len(product_descriptions)]}'
            category = category1 if i <= 10 else category2
            provider = providers[i % len(providers)]
            Product.objects.create(
                uid=f'prod{i}',
                title=title,
                description=description,
                is_active=True,
                in_stock=10 + i,  # Incremental stock for variety
                image_path=f'path/to/{title.lower()}.jpg',
                provider=provider,
                category=category
            )

        self.stdout.write(self.style.SUCCESS('Successfully created demo data for providers and products'))
