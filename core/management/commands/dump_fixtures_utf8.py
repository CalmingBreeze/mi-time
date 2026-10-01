from pathlib import Path
from django.core.management import BaseCommand, call_command

class Command(BaseCommand):
    help = "Generate fixtures for tests and db populate."

    def handle(self, *args, **options):

        self.stdout.write(f"Dumping fixtures : ")

        output = Path("./core/fixtures/products_and_practices.yaml")
        self.stdout.write(f"Products & Practices : Starting")
        self.stdout.write(f"Include : appointment.Service, core.Massage, core.GiftCard, core.Bundle, core.Address, core.Openings, core.Practice")
        with output.open("w", encoding="utf-8", newline="\n") as f:
            call_command(
                "dumpdata",
                "appointment.Service",
                "core.Massage",
                "core.GiftCard",
                "core.Bundle",
                "core.Address",
                "core.Openings",
                "core.Practice",
                format="yaml",
                indent=2,
                stdout=f,
            )
        self.stdout.write(self.style.SUCCESS(f"Products & Practices : Done"))

        output = Path("./core/fixtures/pages_and_configs.yaml")
        self.stdout.write(f"Pages & SiteConfig : Starting")
        with output.open("w", encoding="utf-8", newline="\n") as f:
            call_command(
                "dumpdata",
                "core.Page",
                "core.SiteConfig",
                format="yaml",
                indent=2,
                stdout=f,
            )
        self.stdout.write(self.style.SUCCESS(f"Pages & SiteConfig : Done"))

        output = Path("./core/fixtures/appointment_config.yaml")
        self.stdout.write(f"Appointment:Config : Starting")
        with output.open("w", encoding="utf-8", newline="\n") as f:
            call_command(
                "dumpdata",
                "appointment.Config",
                format="yaml",
                indent=2,
                stdout=f,
            )
        self.stdout.write(self.style.SUCCESS(f"Appointment:Config : Done"))

