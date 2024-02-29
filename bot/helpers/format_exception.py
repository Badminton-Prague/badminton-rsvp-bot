import traceback


def format_exception(action: str, exception: Exception) -> str:
    return (
        f"Error occurred while {action}:\n{str(exception)}\n{'n'.join(traceback.format_tb(exception.__traceback__, 5))}",
    )
