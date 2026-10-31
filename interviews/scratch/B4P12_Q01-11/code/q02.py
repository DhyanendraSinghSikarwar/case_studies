users=8_000_000; loads=6; items=2_000_000
daily=users*loads
avg=daily/86400
print("daily feed requests",daily)
print("avg feed rps",round(avg,1))
print("catalogue items",items)
# invented: 70% of daily requests in 4 busy hours
busy=daily*0.7/(4*3600)
print("busy-hour rps (70% in 4h, invented)",round(busy,1))
assert daily==48_000_000
