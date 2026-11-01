from train_flow import train

if __name__ == "__main__":
    # one deployment, one cron schedule, default parameters; the process stays alive and polls for runs
    train.serve(name="nightly", cron="0 2 * * *", parameters={"rows": 10}, tags=["ml"])
