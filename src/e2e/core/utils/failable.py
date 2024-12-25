import re
import typing as t
from functools import wraps

from e2e.core.logger import logger


class failable:
    def __init__(
        self,
        step: str | None = None,
        etype=None,
        pattern: t.Pattern | None = None,
    ):
        self.step = step
        self.etype = etype
        self.pattern = pattern

    def __enter__(self):
        pass

    def __exit__(self, etype, exc, traceback):
        if exc:
            msg = f'Encountered error when running {self.step}: {exc}' if self.step else f'Encountered error: {exc}'

            def as_error():
                logger.error(msg)
                return False

            if self.etype and etype != self.etype:
                return as_error()
            if self.pattern and not re.match(self.pattern, str(exc)):
                return as_error()
            logger.warning(msg)
            return True
        return True

    def __call__(self, *args, **kwargs):
        fn = args[0]

        @wraps(fn)
        def wrapper(*args, **kwargs):
            failable_ = self
            if not self.step:
                # Make `step` more descriptive by cloning this object and modify only `step`
                failable_ = failable(step=fn.__name__, etype=self.etype, pattern=self.pattern)
            with failable_:
                return fn(*args, **kwargs)

        return wrapper
