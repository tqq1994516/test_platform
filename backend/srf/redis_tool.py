# -*- coding: utf-8 -*-
# @Time : 2022/3/18 16:54
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : redis_tool.py
# @Project : backend
# @Description : redis operation tool
from functools import wraps

from settings import REDIS_TTL


def ttl(sec):
    def out_wrapper(func):
        @wraps(func)
        async def wrapper(redis, key, value):
            await func(redis, key, value)
            return await redis.expire(key, sec)
        return wrapper
    return out_wrapper


@ttl(REDIS_TTL)
async def set_json_value(redis, key, value):
    if await redis.exists(key) == 1:
        await del_json_key(redis, key)
    await redis.json().set(key, value)


async def get_json_value(redis, key):
    return await redis.json().get(key)


async def del_json_key(redis, key):
    return await redis.json().delete(key)


@ttl(REDIS_TTL)
async def set_value(redis, key, value):
    if await redis.exists(key) == 1:
        await del_key(redis, key)
    await redis.set(key, value)


async def get_value(redis, key):
    return await redis.get(key)


async def del_key(redis, key):
    return await redis.delete(key)