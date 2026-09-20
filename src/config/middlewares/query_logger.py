import time

from django.conf import settings
from django.db import connection
from django.utils import timezone
from django.utils.termcolors import colorize


class QueryLoggerMiddleware:
    """
    Logs SQL queries per request in DEBUG mode.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if settings.DEBUG:
            request._query_start_time = time.monotonic()
            request._query_logger_done = False

        try:
            response = self.get_response(request)
        except Exception as exc:
            self.handle_exception(request, exc)
            raise

        return self.handle_response(request, response)

    # ---------------------------------------------------------------------

    def handle_response(self, request, response):
        if not settings.DEBUG:
            return response

        if getattr(request, "_query_logger_done", False):
            return response

        request._query_logger_done = True

        just_count = getattr(settings, "QUERY_LOGGER_JUST_COUNT", False)

        total_time = (
            time.monotonic() - getattr(request, "_query_start_time", time.monotonic())
        ) * 1000

        queries = connection.queries
        query_count = len(queries)
        total_db_time = sum(float(q.get("time", 0)) * 1000 for q in queries)

        # Colors
        def cyan(s):
            return colorize(s, fg="cyan")

        def yellow(s):
            return colorize(s, fg="yellow")

        def green(s):
            return colorize(s, fg="green")

        def magenta(s):
            return colorize(s, fg="magenta")

        def red(s):
            return colorize(s, fg="red")

        print("\n" + "=" * 100)
        print(
            green(
                f"🧩 Query Report for {request.path} [{request.method}] at {timezone.now().strftime('%H:%M:%S')}"
            )
        )
        print(
            yellow(
                f"Total Queries: {query_count} | Total DB Time: {total_db_time:.2f} ms | Total Request Time: {total_time:.2f} ms"
            )
        )
        print("-" * 100)

        if not just_count:
            for idx, query in enumerate(queries, start=1):
                sql = query["sql"]
                time_taken = float(query.get("time", 0)) * 1000
                print(f"{cyan(f'[{idx}]')} {magenta(f'{time_taken:.2f} ms')} → {sql}")
        else:
            print(cyan("🔹 Skipping query details (QUERY_LOGGER_JUST_COUNT=True)"))

        if query_count == 0:
            print(red("⚠️ No database queries were executed in this request."))

        print("=" * 100 + "\n")

        return response

    # ---------------------------------------------------------------------

    def handle_exception(self, request, exception):
        if settings.DEBUG and not getattr(request, "_query_logger_done", False):
            request._query_logger_done = True

            total_time = (
                time.monotonic()
                - getattr(request, "_query_start_time", time.monotonic())
            ) * 1000

            queries = connection.queries
            query_count = len(queries)
            total_db_time = sum(float(q.get("time", 0)) * 1000 for q in queries)

            print("\n" + "=" * 100)
            print(
                f"🧩 Query Report for {request.path} [{request.method}] at {timezone.now().strftime('%H:%M:%S')}"
            )
            print(
                f"Total Queries: {query_count} | Total DB Time: {total_db_time:.2f} ms | Total Request Time: {total_time:.2f} ms"
            )
            print("-" * 100)

            for idx, query in enumerate(queries, start=1):
                sql = query["sql"]
                time_taken = float(query.get("time", 0)) * 1000
                print(f"[{idx}] {time_taken:.2f} ms → {sql}")

            print("=" * 100 + "\n")
