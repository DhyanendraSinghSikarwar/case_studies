import pendulum
from airflow.timetables.interval import CronDataIntervalTimetable
from airflow.timetables.trigger import CronTriggerTimetable
from airflow.timetables.base import TimeRestriction
from airflow.sdk import DAG

# What does a plain string become in this install?
for s in ["@daily", "0 2 * * *"]:
    d = DAG(f"d{len(s)}", schedule=s, start_date=pendulum.datetime(2026, 1, 1, tz="UTC"))
    print(repr(s), "->", type(d.timetable).__name__)

start = pendulum.datetime(2026, 1, 1, tz="UTC")
restr = TimeRestriction(earliest=start, latest=None, catchup=True)

tt = CronDataIntervalTimetable("@daily", timezone="UTC")
info = tt.next_dagrun_info(last_automated_data_interval=None, restriction=restr)
print("CronDataIntervalTimetable first run: interval", info.data_interval.start, "->", info.data_interval.end, "| run_after", info.run_after)

tt2 = CronTriggerTimetable("0 0 * * *", timezone="UTC")
info2 = tt2.next_dagrun_info(last_automated_data_interval=None, restriction=restr)
print("CronTriggerTimetable first run    : interval", info2.data_interval.start, "->", info2.data_interval.end, "| run_after", info2.run_after)
