from .handlers import get_handler


def dispatch(args):
    command = get_command(args)
    handler_func = get_handler(command)
    handler_func(args)


def get_command(args):
    return [arg for arg, value in vars(args).items() if value][0]
