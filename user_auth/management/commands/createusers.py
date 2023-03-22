from django.core.management.base import BaseCommand
from user_auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser by username'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']
        password = input('Enter password: ')
        email = input('Enter email: ')

        User.objects.create_superuser(username=username, email=email, password=password)
