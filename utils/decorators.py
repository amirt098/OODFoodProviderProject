import logging
import functools

logger = logging.getLogger(__name__)


def class_method_logging_decorator(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        class_name = self.__class__.__name__
        method_name = fn.__name__

        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info(f"Calling {class_name}.{method_name}({signature})")

        try:
            # Call the original function
            result = fn(self, *args, **kwargs)

            # Log output
            logger.info(f"{class_name}.{method_name} returned {result!r}")
            return result
        except Exception as e:
            # Log exception
            logger.exception(f"Exception raised in {class_name}.{method_name}. Exception: {str(e)}")
            raise

    return wrapper
