from django.core.management.base import BaseCommand, CommandError
from food.recipes_cmd import insert_data


class Command(BaseCommand):
    help = "Import recipes to database :)"

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs="+", type=str)
        parser.add_argument("email", nargs="+", type=str)

    def handle(self, *args, **options):
        if insert_data(options["filename"][0], options["email"][0]):
            self.stdout.write(self.style.SUCCESS("Successfully import data to db :)"))
        else:
            self.stdout.write(self.style.ERROR("Failed to execute command :/"))
