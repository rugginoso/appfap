import glob
from collections import defaultdict
import re


class ProcessTable(object):
    REGEXPS = {
        'pid': re.compile(r'^Pid:\s+(\d+)$', re.MULTILINE),
        'ppid': re.compile(r'^PPid:\s+(\d+)$', re.MULTILINE),
    }

    def __init__(self):
        self.table = defaultdict(list)
        for status in glob.glob('/proc/*/status'):
            with open(status) as f:
                data = f.read()
            pid = self._get_process_data('pid', data)
            ppid = self._get_process_data('ppid', data)
            if pid and ppid:
                self.table[int(ppid)].append(int(pid))

    def get_children_pids(self, pid, recursive=True):
        children_pids = []
        try:
            children_pids.extend(self.table[pid])
            if recursive:
                for childpid in self.table[pid]:
                    children_pids.extend(
                        self.get_children_pids(childpid, recursive))
        except KeyError:
            pass
        return children_pids

    def _get_process_data(self, key, data):
        regexp = self.REGEXPS[key]
        m = regexp.search(data)
        if m and len(m.group()) > 0:
            return m.group(1)

if __name__ == '__main__':
    t = ProcessTable()
    print(t.get_children_pids(1))
