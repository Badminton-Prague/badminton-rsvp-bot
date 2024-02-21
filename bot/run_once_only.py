import os


def run_once_only(func):
    def wrapper(*args, **kwargs):
        # https://stackoverflow.com/a/67973819
        run_once = os.environ.get("CMDLINERUNNER_RUN_ONCE")
        if run_once is not None:
            return
        os.environ["CMDLINERUNNER_RUN_ONCE"] = "True"

        return func(*args, **kwargs)

    return wrapper
