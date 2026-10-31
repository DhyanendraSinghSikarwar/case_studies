"""Pipeline health checks: pure Python, no Airflow import, so they are easy to unit test."""
from datetime import datetime, timedelta, timezone


def freshness_problem(last_update, now, max_age):
    """Return None if fresh, else a short reason string."""
    if last_update is None:
        return "no data at all"
    age = now - last_update
    if age > max_age:
        return f"stale: {age} old, limit {max_age}"
    return None


def row_count_problem(rows, min_rows=1):
    return f"only {rows} rows, need at least {min_rows}" if rows < min_rows else None


def notify(context_like):
    """Stand-in for Slack/PagerDuty/SMTP. A real one would post to a webhook."""
    print("ALERT:", context_like)


async def notify_async(context_like):
    """AsyncCallback targets must be async functions (Airflow 3.3.2 refused a plain function at parse time)."""
    notify(context_like)


def on_failure(context):
    """Airflow failure callback: receives the task context dict."""
    ti = context["ti"]
    notify(f"task {ti.dag_id}.{ti.task_id} failed on try {ti.try_number}: {context.get('exception')!r}")


if __name__ == "__main__":
    now = datetime(2026, 10, 26, 12, 0, tzinfo=timezone.utc)
    limit = timedelta(hours=26)  # daily job plus 2h grace
    for label, last in [("fresh", now - timedelta(hours=5)), ("stale", now - timedelta(hours=40)), ("empty", None)]:
        print(f"{label:6} ->", freshness_problem(last, now, limit))
    for n in (0, 3):
        print(f"rows={n} ->", row_count_problem(n))
