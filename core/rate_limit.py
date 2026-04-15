import time
from fastapi import Request, HTTPException

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = {}
    
    def check(self, key: str):
        now = time.time()

        if key not in self.requests:
            self.requests[key] = []
        
        self.requests[key] = [
            t for t in self.requests[key]
            if now - t < self.window_seconds
        ]

        if len(self.requests[key]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later."
            )
        
        self.requests[key].append(now)

# 10 requests per minute for agent routes
agent_limiter = RateLimiter(max_requests=10, window_seconds=60)

# 5 requests per minute for auth routes
auth_limiter = RateLimiter(max_requests=5, window_seconds=60)
