from django.core.management.base import BaseCommand, CommandError
from food.openfactfood_cmd import insert_data


class Command(BaseCommand):
    help = "Import 'open fact food' to database. "

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs="+", type=str)
        parser.add_argument("category", nargs="+", type=str)

    def handle(self, *args, **options):
        if insert_data(options["filename"][0], options["category"][0]):
            self.stdout.write(self.style.SUCCESS("Successfully imported data :)"))
        else:
            self.stdout.write(self.style.ERROR("Failed to run command"))
