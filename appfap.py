from gi.repository import GLib, Gdk, Wnck
import sys
from processes import ProcessTable


def throttle_process(pid):
    if pid:
        with open('/sys/fs/cgroup/cpu/fapped/tasks', 'w') as f:
            f.write(str(pid))


def unthrottle_process(pid):
    if pid:
        with open('/sys/fs/cgroup/cpu/tasks', 'a') as f:
            f.write(str(pid))


def on_active_window_changed(screen, previously_active_window):
    process_table = ProcessTable()

    windows_pids = [w.get_pid() for w in screen.get_windows()]

    active_window = screen.get_active_window()
    active_pid = active_window.get_pid() if active_window else 0

    if active_pid in windows_pids:
        windows_pids.remove(active_pid)

    to_throttle = windows_pids
    for pid in windows_pids:
        to_throttle.extend(process_table.get_children_pids(int(pid)))

    to_unthrottle = [active_pid] + \
        process_table.get_children_pids(int(active_pid))

    for pid in to_throttle:
        throttle_process(pid)

    for pid in to_unthrottle:
        unthrottle_process(pid)


Gdk.init(sys.argv)
loop = GLib.MainLoop(None)
screen = Wnck.Screen.get_default()

screen.connect('active-window-changed', on_active_window_changed)

loop.run()
