from asyncio import AbstractEventLoop
from asyncio.events import Handle
from contextlib import contextmanager


def patch_handler(handler: Handle) -> None:
    """"Patches the given handle object to enable inspection"""""
    import ipdb; ipdb.set_trace()
    handler._inspector_enabled = True



def patch_event_loop_handler_creator(event_loop: AbstractEventLoop, method_name: str) -> None:
    orig_method = getattr(event_loop, method_name)
    def wrapper(*args, **kwargs):
        handler = orig_method(*args, **kwargs)
        return handler
    setattr(event_loop, method_name, wrapper)
    setattr(event_loop, f'_orig_{method_name}', orig_method)



def unpatch_event_loop_handler_creator(event_loop: AbstractEventLoop, method_name: str) -> None:
    orig_method = getattr(event_loop, f'orig_{method_name}')
    setattr(event_loop, method_name, orig_method)



@contextmanager
def enable_inpection(event_loop: AbstractEventLoop) -> None:
    """Patches the given event loop to enable inspection."""
    patch_event_loop_handler_creator(event_loop, 'call_soon')
    yield
    unpatch_event_loop_handler_creator(event_loop, 'call_soon')