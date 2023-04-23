"""module to make the running of many shell commands more convenient"""
from . import jconsole as jc
import os, shutil, sys
import os.path as opath
import shlex
from shlex import split as lex
from subprocess import Popen, PIPE, run
import traceback
from datetime import datetime

class Shelldo:
    def __init__(self, logdir=None):
        """Run sets of shell commands with chain() loging the results.
        Allows to build a human readable list of actions and results that can 
        be printed as they're happening or as a full report all at once. 

        The class is intended to be used something like:\n
            Shelldo.set_action('making a directory and a file')\n
            outcome = Shelldo.chain(['mkdir x', 'touch y'])\n
            Shelldo.set_result(outcome)\n
            ...more...\n
            Shelldo.report()\n
        
        @param logdir: path where logs should be stored, defaults to cwd. 
        """ 
        
        self.logdir = os.getcwd() if logdir is None else logdir
        os.makedirs(self.logdir, exist_ok=True)

        timestamp = str(datetime.now())
        timestamp = timestamp[:timestamp.rfind('.')]
        self.logfile = f'{self.logdir}/shelldo log {timestamp}'
        try:
            latestlog = f'{self.logdir}/@LATEST-SHELLDO-LOG.txt'
            os.remove(latestlog)
        except FileNotFoundError:
            pass
        os.symlink(self.logfile, latestlog)
        
        # determine platform info 
        if os.name is None:
            self.package_manager = None
        else:    
            try:
                run(['apt'], capture_output=True)
                self.package_manager = 'apt'
            except FileNotFoundError:
                try:
                    run(['dnf'], capture_output=True)
                    self.package_manager = 'dnf'
                except FileNotFoundError:
                    print('shelldo: No supported package manager found (apt, dnf)')
            
        self.actions = [] # format is [ [action, result], [action, result] ]
        self.curraction = ''

    def inst_cmd(self, program):
        """Return f'sudo {self.package_manager} -y install {program}'."""
        return f'sudo {self.package_manager} -y install {program}'

    def set_action(self, description, noprint=False, nocolor=False):
        """Update and print the current action."""
        
        self.curraction = description
        self.actions.append([description])
        if not noprint:
            if nocolor:
                print(f'---->  {self.curraction}')
            else:
                print(jc.bold(jc.yellow('---->  ')+f'{self.curraction}'))

    def set_result(self, result, action:str=None, nocolor=False, norecord=False, noprint=False):
        """record and/or print the specified result of the specified action.
        Action defaults to self.curraction. 
        
        @param result: may be specified with the strings "ok/fail" or booleans. 
        @param action: value to lookup in self.actions and record a result for.
        curraction is used if no value is given.  
        @param nocolor: do not use color escape sequences
        @param norecord: do not record the result in self.actions
        """
        result = self._parseresult(result)
        if action is None:
            action = self.curraction
        if not norecord:
            for x in self.actions:
                if x[0].casefold() == action.casefold():
                    x.append(result)
        if not noprint:
            if nocolor:
                print(f'[{result}]:  {action}')
            else:
                result = jc.green(result) if result == "OK" else jc.red(result)
                print(f'[{jc.bold(result)}]:  {action}')
    

    def report(self):
        """Print all actions and their results."""
        print(jc.bold(jc.yellow('\n////// Report /////')))
        for x in self.actions:
            self.set_result(x[1], x[0], norecord=True)
        

    def log(self, result, action):
        """Add a line to the log file like \"[result]:  [action]\"
        
        @param result: may be specified with strings "ok/fail" or booleans. 
        """
        result = self._parseresult(result)
        with open(self.logfile, 'a') as f:
            line = f"[{result}]:  {action}\n"
            f.writelines(line)

    def _parseresult(self, result):
        if isinstance(result, str):
            result = result.casefold()
        return {True:"OK", False:"FAIL", "ok": "OK", "fail": "FAIL"}[result]


    def chain(self, cmds, logall=False, ignore_exit_code=False, quiet=False):
        """run a series of commands in the shell, returning False immediately
         if one in the series exits with any non-zero value. Otherwise returns True.

        commands are run usingsubprocess.Popen(bufsize=1, stdout=PIPE, stderr=PIPE, text=True)

        
        @param cmds: list of strings, each of which is a single shell command,
        such as "mv src dest".  
        @param logall: if True, log each command that is run, not just those, that fail.
        @param ignore_exit_code: don't return if one of cmds returns non-zero.
        @param quiet: don't print stdout content as the subprocess makes it 
        available. 
        """
        
        for x in cmds:
            try:
                cmd = shlex.split(x)
                with Popen(cmd, bufsize=1, stdout=PIPE, stderr=PIPE, text=True) as p:
                    # print stdout
                    if not quiet:
                        for line in p.stdout:
                            print(line, end='') 
                    # wait for subprocess to finish
                    p.wait()
                    if p.returncode != 0:
                        print(f'chain: failed (exit code {p.returncode}): {x}')

                        errstr = ''.join([x for x in p.stderr])
                        self.log(False,
                                f'failed (exit code {p.returncode}): {x}\n\tstderr:\n\t\t{errstr}')        
                        if not ignore_exit_code:
                            return False
                    else:
                        if logall:
                            self.log(True, x)
            except:
                estring = traceback.format_exc()
                print(estring)
                self.log(False, f'{x}\n\t{estring}')
                return False
            
        return True


s = Shelldo()