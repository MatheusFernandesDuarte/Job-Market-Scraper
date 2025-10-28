import asyncio
import sys

import uvicorn

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(policy=asyncio.WindowsSelectorEventLoopPolicy())
    except Exception as e:
        print(f"WARNING: Could not set WindowsSelectorEventLoopPolicy in run_api.py: {e}")


if __name__ == "__main__":
    uvicorn.run(
        app="backend.src.interface.api.fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )
