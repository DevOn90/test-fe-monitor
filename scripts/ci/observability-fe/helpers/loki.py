import time
from typing import Any

import requests

class LokiClient:

    """Client for querying Loki logs."""

    def __init__(
            self,
            url: str = "http://localhost:3100",
            timeout: int = 10,
    ):
        self.url = url.rstrip("/")
        self.timeout = timeout

    def query(
            self,
            logql_query: str,
            limit: int = 100,            
    ) -> list[dict[str, Any]]:

        """
        Execute a LogQL query and return matching log streams.
        """
        endpoint = f"{self.url}/loki/api/v1/query_range"

        params = {
            "query": logql_query,
            "limit": limit,
            "since": "5m",
            "direction": "backward"
        }

        response = requests.get(
            endpoint,
            params=params,
            timeout=self.timeout
        )

        response.raise_for_status()

        result = response.json()

        if result.get("status") != "success":
            raise RuntimeError(f"Loki query failed: {result}")

        return result.get("data", {}).get("result", [])

    def query_logs(
            self,
            logql_query: str,
            limit: int = 100,
    ) -> list[str]:

        """
        Execute a LogQL query and return only the log lines.
        """

        streams = self.query(logql_query, limit=limit)

        return [
            value[1]
            for stream in streams
            for value in stream.get("values", [])
        ]

    def wait_for_log(
                self,
                logql_query: str,
                expected_text: str,
                timeout: int = 30,
                interval: float = 2,
        ) -> str:
    
                """
                Wait until a matching log line appears in Loki.
    
                Returns the matching log line.
                Raises AssertionError if no matching log appears.
                """
    
                start_time = time.time()
    
                while time.time() - start_time < timeout:
                    logs = self.query_logs(logql_query)
    
                
                    for log in logs:
                       if expected_text in log:
                          return log
    
                    time.sleep(interval)
    
                raise AssertionError(
                    f"Log containing '{expected_text}' "
                    f"was not found in Loki within {timeout} seconds."
                )

    def wait_for_logs(
            self,
            logql_query: str,
            expected_text: str,
            expected_count: int = 2,
            timeout: int = 30,
            interval: float = 2,
    ) -> list[str]:

            """
            Wait until a matching log line appears in Loki.

            Returns the matching log line.
            Raises AssertionError if no matching log appears.
            """

            start_time = time.time()

            while time.time() - start_time < timeout:
                logs = self.query_logs(logql_query)

                if len(logs) >= expected_count:
                    return logs

                time.sleep(interval)

            raise AssertionError(
                f"Log containing '{expected_text}' "
                f"was not found in Loki within {timeout} seconds."
            )