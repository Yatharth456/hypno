from django.core.management.base import BaseCommand
from user_auth.models import User

class Command(BaseCommand):
    help = 'Delete a user by email address'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        email = options['email']

        try:
            user = User.objects.get(email=email)
            user.delete()
            self.stdout.write(self.style.SUCCESS('User deleted successfully.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with email {email} does not exist.'))
