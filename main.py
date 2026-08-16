import asyncio
import httpx

from src.Logger import logger
from src.SecureSharedState import SecureSharedState
from src.TaskValidator import TaskValidator

async def process_task(task: dict, state: SecureSharedState) -> int | None:
    task_id = task["id"]
    instruction = task["instruction"]
    target_domain = task["payload_domain"]

    logger.info(f"Task {task_id}: Started processing.")

    if not TaskValidator.is_safe_content(instruction):
        logger.warning(f"Task {task_id}: REJECTED - Malicious content detected ('{instruction}').")
        return None

    logger.info(f"Task {task_id}: Validating domain '{target_domain}' via external DNS API...")
    is_valid = await TaskValidator.validate_domain_content(target_domain)

    if not is_valid:
        logger.warning(f"Task {task_id}: SKIPPED = Domain '{target_domain}' failed external validation (does not resolve).")
        return None

    logger.info(f"Task {task_id}: APPROVED - Executing instruction...")
    await asyncio.sleep(0.5)

    await state.update_state(task_id, f"Successfully processed instruction for {target_domain}")
    return task_id

async def main():
    GIST_URL = "https://gist.githubusercontent.com/AP-Abhishek/c09f31b37bf3f76c7692850c5a174844/raw/"
    logger.info(f"Fetching mock public feed from Gist: {GIST_URL}")

    async with httpx.AsyncClient() as client:
        response = await client.get(GIST_URL)
        public_feed = response.json()

    shared_state = SecureSharedState()

    logger.info("=== Starting Concurrent Task Processing ===")

    tasks = [process_task(t, shared_state) for t in public_feed]
    results = await asyncio.gather(*tasks)

    approved_task_ids = [res for res in results if res is not None]
    expected_success_count = len(approved_task_ids)

    logger.info("=== Processing Complete ===")
    logger.info(f"Expected Successful Tasks: {expected_success_count}")
    logger.info(f"Actual Count of Successful Tasks: {shared_state.successful_tasks}")

    assert shared_state.successful_tasks == expected_success_count, f"Race Condition detected! Expected{expected_success_count}, got {shared_state.successful_tasks}."
    logger.info("STATE VERIFICATION PASSED: No race conditions detected. No lost updates.")

if __name__ == "__main__":
    asyncio.run(main())
