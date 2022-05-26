import asyncio
import aiosqlite as db

import os
from pathlib import Path

def db_file(filename):
    return Path(os.path.dirname(os.path.abspath(__file__))) / filename

# able to create instances of this with the preferred id
class permcache():

    def __init__(self, id : str):
        self.id = id
    
    async def _add(self, val : str = None) -> None:
        if val == None:
            val = 1

        # simple numeric cache program (uniqueid based)
        conn = await db.connect(db_file('cache.db'))
        cur = await conn.cursor()
        await cur.execute("SELECT numeric FROM cache WHERE uniqueid = ?", (self.id,))
        req = await cur.fetchone()

        if req == None:
            await cur.execute("INSERT INTO cache(numeric,uniqueid) VALUES (?,?)", (val, self.id))
            await conn.commit()
            await conn.close()
            return val
        elif req != None:
            req = req[0]
            await cur.execute("UPDATE cache SET numeric = numeric + ? WHERE uniqueid = ?", (val, self.id))
            await conn.commit()
            await conn.close()
            return int(req) + val

