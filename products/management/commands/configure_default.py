from django.core.management.base import BaseCommand, CommandError
from products.models import Count

class Command(BaseCommand):
    help = 'Set Maximum Values of Average Area, Average Volume, Box to be added per week and Box to be added' \
           'per week per user. Enter these values in respective order'

    def add_arguments(self, parser):
        parser.add_argument('values', nargs='+', type=int)

    def handle(self, *args, **options):
        if len(options['values']) < 4 or len(options['values']) > 4:
            raise CommandError("Enter exactly 4 values")
        else:
            try:
                inputs = Count.objects.get(id=1)
                inputs.average_area = options['values'][0]
                inputs.average_volume = options['values'][1]
                inputs.box_added_in_week = options['values'][2]
                inputs.box_added_by_user_in_week = options['values'][3]
                inputs.save()
            except Exception as e:
                c = Count(average_area=options['values'][0], average_volume=options['values'][1],
                          box_added_in_week=options['values'][2], box_added_by_user_in_week=options['values'][3])
                c.save()

            self.stdout.write(self.style.SUCCESS('Configuration Successful'))
