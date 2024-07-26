from jtools.v2shelldo import Shelldo

shelldo = Shelldo('/home/jeremy/')


shelldo.set_action('doing stuff')

shelldo.run(['touch here', 'ls | wc ', 'touch /home/jeremy/here/newfile'], shell=True, ignore_exit_code=True)
