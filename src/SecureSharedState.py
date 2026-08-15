import asyncio

from src.Logger import logger

class SecureSharedState:
    def __init__(self):
        self._lock = asyncio.Lock()
        self.successful_tasks = 0
        self.state_log = []

    async def update_state(self, task_id: int, result: str):
        async with self._lock:
            logger.info(f"Task {task_id}: Acquired lock. Modifying state...")
            current_count = self.successful_tasks

            await asyncio.sleep(0.2)

            self.successful_tasks = current_count + 1
            self.state_log.append(f"Task {task_id}: {result}")
            logger.info(f"Task {task_id}: Released lock. New count: {self.successful_tasks}")
