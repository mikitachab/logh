from .handlers import get_handler


def dispatch(command, args):
    handler_func = get_handler(command)
    handler_func(args)
