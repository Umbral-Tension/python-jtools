from jtools.shelldo import Shelldo
from subprocess import run, Popen, PIPE, STDOUT
import subprocess
import shlex

shelldo = Shelldo('/home/jeremy/')
shelldo.set_action('doing stuff')
shelldo.run(
    ['touch here',
    'touch crab || touch laugh ',
    'touch /home/jeremy/newfile',
    'ls -a | wc'],
     shell=True, ignore_exit_code=False)

shelldo.set_action('OTHERSTUFF')
shelldo.run(
    ['touch here2',
    'touch crab || touch laugh ',
    'touch /home/jeremy/sf/newfile',
    'ls -a | wc'],
     ignore_exit_code=True)




