import time

from fastapi import Request, HTTPException

from app.redis.connection import get_redis


redis_client = get_redis()


MAX_REQUESTS = 10
WINDOW_SECONDS = 60


def check_rate_limit(request: Request):

    client_ip = request.client.host

    key = f"rate_limit:{client_ip}"

    current_count = redis_client.get(key)

    if current_count is None:

        redis_client.set(
            key,
            1,
            ex=WINDOW_SECONDS
        )

        return

    current_count = int(current_count)

    if current_count >= MAX_REQUESTS:

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )

    redis_client.incr(key)