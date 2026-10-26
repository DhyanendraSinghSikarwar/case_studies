# the Q15 app plus a /stall route that blocks the event loop (simulates a GC pause or a slow batch). Demo only.
import time
from serve_app import app
@app.get("/stall")
async def stall(secs: float = 0.5):
    time.sleep(secs)             # blocking on purpose
    return {"stalled": secs}
