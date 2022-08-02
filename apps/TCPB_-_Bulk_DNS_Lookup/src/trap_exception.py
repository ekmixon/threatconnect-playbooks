#!/usr/bin/env python
"""Exception Trap Decorator"""

# standard library
import functools
import inspect


def trap(handler='handle_exception', classes=None):
    """Creates a trap handling decorator"""

    if classes is not None and not isinstance(classes, (list, tuple)):
        classes = (classes,)

    def decorator(f):
        """Wrap f"""

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                instance = inspect.unwrap(f)
                if not instance:
                    raise  # pragma: no cover

                if classes and not isinstance(e, classes):
                    raise

                self = args[0] if args else instance
                handle = handler if callable(handler) else getattr(self, handler, None)
                if handle is None:
                    raise  # pragma: no cover
                if not callable(handle):
                    raise  # pragma: no cover
                # N.B. This wont work right on class methods
                return handle(e)

        return wrapper

    return decorator
