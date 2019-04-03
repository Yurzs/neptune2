import asyncio
import os
import aioredis
from gino import Gino

db = Gino()

loop = asyncio.get_event_loop()

redisconnection = None


async def main():
    await db.set_bind('postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        user=os.environ['DB_USER'],
        database=os.environ['DB_NAME'],
        host=os.environ.get('DB_SERVICE', '127.0.0.1'),
        port=os.environ.get('DB_PORT', 5432),
        password=os.environ.get('DB_PASS', 'postgres')
    ),
        loop=loop)
    global redisconnection
    redisconnection = await aioredis.create_redis_pool(
        'redis://redis', db=2, loop=loop, minsize=5, maxsize=10)


loop.run_until_complete(main())
