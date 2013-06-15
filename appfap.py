from gi.repository import GLib, Gdk, Wnck
import sys

def throttle_process(pid):
    if pid:
        with open('/sys/fs/cgroup/cpu/fapped/tasks', 'w') as f:
            f.write(str(pid))


def unthrottle_process(pid):
    if pid:
        with open('/sys/fs/cgroup/cpu/tasks', 'a') as f:
            f.write(str(pid))


def on_active_window_changed(screen, previously_active_window):
    windows_pids = [w.get_pid() for w in screen.get_windows()]

    active_window = screen.get_active_window()
    active_pid = active_window.get_pid() if active_window else 0

    if active_pid in windows_pids:
        windows_pids.remove(active_pid)

    for pid in windows_pids:
        throttle_process(pid)
    unthrottle_process(active_pid)


Gdk.init(sys.argv)
loop = GLib.MainLoop(None)
screen = Wnck.Screen.get_default()

screen.connect('active-window-changed', on_active_window_changed)

loop.run()