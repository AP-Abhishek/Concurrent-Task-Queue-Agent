import re
import httpx

from src.Logger import logger

class TaskValidator:
    MALICIOUS_TASKS = [
        r"(?i)ignore all previous instructions",
        r"(?i)bypass restrictions",
        r"(?i)import os",
        r"(?i)subprocess\.call",
        r"(?i)rm -rf",
        r"(?i)drop table",
        r"(?i)UNION SELECT"
    ]

    @staticmethod
    def is_safe_content(instructions: str) -> bool:
        for pattern in TaskValidator.MALICIOUS_TASKS:
            if re.search(pattern, instructions):
                return False
        return True

    @staticmethod
    async def validate_domain_content(domain: str) -> str:
        url = "https://cloudflare-dns.com/dns-query"
        headers = {
            "accept": "application/dns-json"
        }
        params = {
            "name": domain,
            "type": "A"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params, timeout=5.0)
                data = response.json()
                return data.get("Status") == 0
        except Exception as e:
            logger.error(f"External API check failed for {domain}: {e}")
            return False
