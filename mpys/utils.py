import json
from mpys import SerialHelper

fmt_clean_root = '''
for f in uos.listdir():
    if f not in %s:
        mpys_del(f)
'''


def clean_root(*exclude):
    s = SerialHelper()
    s.script(fmt_clean_root % json.dumps(exclude))


# clean_root("boot.py", "main.py", "webrepl_cfg.py")
