from contextvars import ContextVar

is_blockage_enabled: ContextVar[bool] = ContextVar('is_blockage_enabled', default=True)
