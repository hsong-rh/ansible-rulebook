import asyncio
import glob
import json
import logging
import os
from typing import Any, Dict

logger = logging.getLogger("replay")


async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    delay = args.get("delay", 0)
    directory = args.get("directory", None)
    if not directory:
        logger.error("No replay directory")
        return

    for replay_file in sorted(glob.glob(os.path.join(directory, "*.json"))):
        with open(replay_file) as f:
            await queue.put(json.loads(f.read()))
            await asyncio.sleep(delay)


if __name__ == "__main__":

    class MockQueue:
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), dict(directory="replays")))
