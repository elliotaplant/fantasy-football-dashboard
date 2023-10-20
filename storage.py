import json
import redis
from config import REDIS_URL

# Setting up the Redis client
redis_client = redis.Redis.from_url(REDIS_URL)


def get_last_element(team_key):
    last_element_json = redis_client.lindex(team_key, -1)
    return json.loads(last_element_json) if last_element_json else None


def append_to_redis(team_key, data):
    redis_client.rpush(team_key, json.dumps(data))
