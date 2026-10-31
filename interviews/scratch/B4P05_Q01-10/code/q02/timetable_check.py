# Which run would a scheduler create first, and when may it start? Pure pendulum maths.
import pendulum
start = pendulum.datetime(2026, 1, 1, tz="UTC")
interval_start, interval_end = start, start.add(days=1)
print("first @daily data interval :", interval_start, "->", interval_end)
print("run is created at or after :", interval_end, "(end of interval)")
# DST: 2026-03-08 is a US spring-forward date
ny = pendulum.datetime(2026, 3, 8, tz="America/New_York")
print("NY day length (hours)      :", ny.add(days=1).diff(ny).in_hours())
print("UTC day length (hours)     :", pendulum.datetime(2026,3,8).add(days=1).diff(pendulum.datetime(2026,3,8)).in_hours())
