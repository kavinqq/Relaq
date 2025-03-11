from pprint import pprint
from django.core.management.base import BaseCommand

from core.services import Relaq


class Command(BaseCommand):
    help = "抓取店家資料"

    def add_arguments(self, parser):
        parser.add_argument(
            "--search_query",
            type=str,
            help="搜尋關鍵字",
        )

    def handle(self, *args, **options):
        search_query = options.get("search_query")

        relaq = Relaq()
        file_name = relaq.get_ai_result(search_query=search_query)

        self.stdout.write(self.style.SUCCESS(f"[{search_query}] 抓取店家資料完成 -> {file_name}"))

        return None
