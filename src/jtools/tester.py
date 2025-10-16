from jtools.v2shelldo import Shelldo

shelldo = Shelldo('/home/jeremy/')


shelldo.set_action('doing stuff')

# shelldo.run(['touch here', 'ls | wc ', 'touch /home/jeremy/here/newfile', 'ls -a | wc'], shell=True, ignore_exit_code=False)

import shlex
cmd = ["ls", "wc"]

cmd = shlex.join(cmd)
print(cmd)
# s = shlex.split(cmd)
# print(s)
from subprocess import run, Popen, PIPE, STDOUT
import subprocess

with Popen(cmd, bufsize=1, stdout=PIPE, stderr=STDOUT, text=True, shell=True) as p:
    # print stdout
    for line in p.stdout:
        print(line, end='') 
    # wait for subprocess to finish
    p.wait()