import hmac, time, hashlib
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

# Keys are stored as sha256 hashes (never plain). Demo values only; real keys come from a secret manager.
KEYS = {hashlib.sha256(b"key-alice").hexdigest(): {"name": "alice", "models": {"iris"}},
        hashlib.sha256(b"key-bob").hexdigest(): {"name": "bob", "models": {"fraud"}}}
MAX_BODY = 2_000          # bytes
MAX_FEATURES = 4

class Bucket:
    """Token bucket: `capacity` tokens, refilled at `rate` per second. clock is injectable for tests."""
    def __init__(self, capacity, rate, clock=time.monotonic):
        self.capacity, self.rate, self.clock = capacity, rate, clock; self.tokens, self.last = capacity, clock()
    def allow(self):
        now = self.clock(); self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate); self.last = now
        if self.tokens >= 1: self.tokens -= 1; return True
        return False

def make_app(clock=time.monotonic, capacity=3, rate=1.0):
    app = FastAPI(); buckets = {}

    async def limit_body(request: Request):
        cl = request.headers.get("content-length")
        if cl is not None and int(cl) > MAX_BODY: raise HTTPException(413, "body too large")
        body = b""
        async for chunk in request.stream():          # also covers chunked uploads with no Content-Length
            body += chunk
            if len(body) > MAX_BODY: raise HTTPException(413, "body too large")
        request.state.body = body

    def auth(x_api_key: str = Header(default="")):
        h = hashlib.sha256(x_api_key.encode()).hexdigest()
        for stored, info in KEYS.items():              # compare against every key, constant time per compare
            if hmac.compare_digest(h, stored): return info
        raise HTTPException(401, "invalid api key", headers={"WWW-Authenticate": "ApiKey"})

    def rate_limit(user=Depends(auth)):
        b = buckets.setdefault(user["name"], Bucket(capacity, rate, clock))
        if not b.allow(): raise HTTPException(429, "rate limit", headers={"Retry-After": "1"})
        return user

    class Features(BaseModel): features: list[float] = Field(min_length=MAX_FEATURES, max_length=MAX_FEATURES)

    @app.post("/v1/models/{model}/predict", dependencies=[Depends(limit_body)])
    async def predict(model: str, request: Request, user=Depends(rate_limit)):
        if model not in user["models"]: raise HTTPException(403, "key not allowed for this model")   # per-model authorisation
        try: f = Features.model_validate_json(request.state.body)
        except Exception: raise HTTPException(422, "bad payload")
        return {"model": model, "score": sum(f.features) / 4}      # stand-in for the model
    return app
