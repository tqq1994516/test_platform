# -*- coding: utf-8 -*-
# @Time : 2022/3/18 16:54
# @Author : chenxu.tian
# @Email : chenxu.tian@horizon.ai
# @File : redis_tool.py
# @Project : backend
# @Description : redis operation tool

async def set_value(redis, key, value):
    await redis.execute_command("set", key, value)
    await redis.execute_command("expireat", key, value)


async def get_value(redis, key):
    return await redis.execute_command("get", key)


async def set_json_value(redis, key, value):
    await redis.json().execute_command("set", key, value)
    await redis.json().execute_command("expireat", key, value)


async def get_json_value(redis, key):
    return await redis.json().execute_command("get", key)
