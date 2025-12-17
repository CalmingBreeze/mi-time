from django.core.management.base import BaseCommand, CommandError
from core import stripeviews

class Command(BaseCommand):
    help = "Send a giftcard voucher, usage : <command> client_email massage_name code expiry_date"

    def add_arguments(self, parser):
        parser.add_argument(
            'customer_email'
        )
        parser.add_argument(
            'gcinfos', nargs=3
        )
    
    def handle(self, *args, **options):
        # self.stdout.write(f"Send GC : customer_email : {args['customer_email']}, gcinfo : {args['gcinfos']}")
        # self.stdout.write(f"Args {options['customer_email']} {options['gcinfos']}")
        self.stdout.write(f"Sending Giftcard with following parameters : receiver {options['customer_email']}, gc_infos {options['gcinfos']}")
        stripeviews.send_giftcardmail(options['customer_email'], options['gcinfos'])
