"""
Launch San Andreas.. if it gives the 'what screen' popup, accept and then go full screen.
"""

# pip install pywinauto
from pywinauto import application, keyboard

# pip install keyboard (has a way to send keys slower than pywinauto)
import keyboard as kb
from pathlib import Path
import time
import subprocess

# Wife's path
SA_EXE = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\Grand Theft Auto San Andreas\gta-sa.exe"
)
if not SA_EXE.is_file():
    # My path
    SA_EXE = Path(
        r"Y:\Games\Steam\steamapps\common\Grand Theft Auto San Andreas\gta-sa.exe"
    )


def start_game():
    dir = SA_EXE.parent
    name = SA_EXE.name
    # Launch via powershell since for some reason otherwise it doesn't launch the ui
    process = subprocess.Popen(rf"powershell .\{name}", cwd=dir, shell=True)
    time.sleep(3)
    if process.returncode is not None:
        raise RuntimeError("game died")
    return process


def get_game_pid() -> int:
    """
    The game pid doens't match the process.pid since the game's pid is a subprocess of the shell
    """

    for pid, exe, *_ in application.process_get_modules():
        if exe == str(SA_EXE):
            return pid

    raise ValueError("no pid?")


def get_device_selection_window(app: application.Application):
    """
    Find and return the Device Selection window if found
    """
    for w in app.windows():
        if "Device Selection" in str(w):
            return w


def send_alt_enter():
    """Do this slowly.. since it doesn't seem to work otherwise"""
    kb.press("alt")
    kb.press("enter")
    time.sleep(1)
    kb.release("alt")
    kb.release("enter")


def handle_device_selection(window, app: application.Application):
    window.minimize()
    window.restore()

    # close dialog
    keyboard.send_keys("{ENTER}")

    # wait for game to open
    time.sleep(2)

    top_window = app.top_window()
    top_window.minimize()
    top_window.restore()

    # click through loading screens
    for _ in range(3):
        keyboard.send_keys("%{ENTER}")
        time.sleep(1)

    # wait for more loading
    time.sleep(2)

    # go full screen
    top_window.click()
    time.sleep(1)
    send_alt_enter()


if __name__ == "__main__":
    process = start_game()

    app = application.Application()
    app.connect(process=get_game_pid())

    if window := get_device_selection_window(app):
        print("Handling device selection then going full screen.")
        handle_device_selection(window, app)
    else:
        print("Game opened on its own.")
