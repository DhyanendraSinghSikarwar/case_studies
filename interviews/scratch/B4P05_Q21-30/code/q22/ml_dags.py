import pendulum
from airflow.sdk import Asset, dag, task
from airflow.timetables.assets import AssetOrTimeSchedule
from airflow.timetables.trigger import CronTriggerTimetable

features = Asset("s3://ml-bucket/features/daily/")

@dag(schedule="0 2 * * *", start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False, tags=["producer"])
def build_features():
    @task(outlets=[features])
    def write_features():
        print("wrote features/daily/ ; asset event emitted when this task succeeds")
    write_features()

@dag(schedule=[features], start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False, tags=["consumer"])
def train_on_features():
    @task
    def train():
        print("training because the features asset was updated")
    train()

# new data OR a weekly safety net, whichever comes first
@dag(schedule=AssetOrTimeSchedule(timetable=CronTriggerTimetable("0 6 * * 1", timezone="UTC"), assets=[features]),
     start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), catchup=False)
def train_or_weekly():
    @task
    def train():
        print("run")
    train()

build_features(); train_on_features(); train_or_weekly()
