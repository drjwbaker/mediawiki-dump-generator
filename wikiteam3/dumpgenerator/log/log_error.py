import datetime

from wikiteam3.dumpgenerator.config import Config


def do_log_error(config: Config, to_stdout: bool = False, text="") -> None:
    """Log error in errors.log"""
    if text:
        with open(f"{config.path}/errors.log", "a", encoding="utf-8") as outfile:
            output = (
                f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {text}\n'
            )
            outfile.write(output)
    if to_stdout:
        print(text)
