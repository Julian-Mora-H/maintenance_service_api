import time
import functools
import logging
import asyncio
from typing import Callable, Any

# Logger con nivel INFO visible en consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def measure_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorador que mide y registra el tiempo de ejecución de la función.
    Soporta funciones síncronas y asíncronas (async def).
    """
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000.0
                logger.info(f"✓ {func.__name__} executed in {elapsed_ms:.2f} ms")
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000.0
                logger.info(f"✓ {func.__name__} executed in {elapsed_ms:.2f} ms")
        return sync_wrapper