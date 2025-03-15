from django.core.management.base import BaseCommand

from core.services import CoreService


class Command(BaseCommand):
    help = "抓取店家資料"

    def add_arguments(self, parser):
        parser.add_argument(
            "search_region",
            type=str,
            help="搜尋區域",
        )

    def handle(self, *args, **options):
        search_region = options.get("search_region")

        core_service = CoreService()
        file_name = core_service.main(search_region=search_region)

        self.stdout.write(self.style.SUCCESS(f"[{search_region}] 抓取店家資料完成 -> {file_name}"))

        return None
