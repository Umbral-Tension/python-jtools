"""module to make the running of many shell commands more convenient"""
from . import jconsole as jc
import os, shutil, sys
import os.path as opath
import shlex
from shlex import split as lex
from subprocess import Popen, PIPE, run, STDOUT
import traceback
from datetime import datetime

class Shelldo:
    def __init__(self, logdir):
        """Run sets of shell commands with chain(), logging the results.
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
        self.logdir = logdir
        os.makedirs(self.logdir, exist_ok=True)

        timestamp = str(datetime.now())
        timestamp = timestamp[:timestamp.rfind('.')]
        self.logfile = f'{self.logdir}/shelldo log {timestamp}'
        self.full_transcript = f'{self.logdir}/shelldo full transcript {timestamp}'

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

    def inst_cmd(self, program, uninstall=False):
        """Return platform specific install/uninstall command ."""
        if not uninstall:
            return f'sudo {self.package_manager} -y install {program}'
        if uninstall:
            return f'sudo {self.package_manager} -y remove {program}'

    def set_action(self, description, noprint=False, nocolor=False):
        """Update and print the current action."""
        
        self.curraction = description
        self.actions.append([description])
        if not noprint:
            if nocolor:
                print(f'[starting]:  {self.curraction}')
            else:
                starting = jc.bold(jc.green('starting'))
                print(f'[{starting}]:  {self.curraction}')

    def set_result(self, result, action=None, nocolor=False, noprint=False):
        """record the result of the specified action. Action defaults to self.curraction. 
        
        @param result: may be specified with the strings "ok/fail" or booleans. 
        @param action: value to lookup in self.actions and record a result for.
        curraction is used if no value is given.  
        @param nocolor: do not use color escape sequences
        @param norecord: do not record the result in self.actions
        """
        result = self._parseresult(result)
        if action is None:
            action = self.curraction
        for x in self.actions:
            if x[0].casefold() == action.casefold():
                x.append(result)
        if not noprint:
            self.print_action(result, action, nocolor=nocolor)

    

    def print_action(self, result, action, nocolor=False):
        """"print the specified action/result combo. Does not reference shelldo object's action list. Merely prints the string arguments given.
        """
        if nocolor:
                print(f'[{result}]:  {action}\n')
        else:
            result = jc.green(result) if result == "OK" else jc.red(result)
            print(f'[{jc.bold(result)}]:  {action}\n')

            
    def report(self):
        """Print all actions and their results."""
        print(jc.bold(jc.yellow('\n////// Report /////')))
        for x in self.actions:
            self.print_action(x[1], x[0])
        

    def log(self, result, action):
        """Add a line to the log file like \"[result]:  [action]\"
        
        @param result: may be specified with strings "ok/fail" or booleans. 
        """
        result = self._parseresult(result)
        with open(self.logfile, 'a') as f:
            f.writelines(f"[{result}]:  {action}\n")

    def _parseresult(self, result):
        if isinstance(result, str):
            result = result.casefold()
        return {True:"OK", False:"FAIL", "ok": "OK", "fail": "FAIL"}[result]


    def chain(self, cmds:list, logall=False, ignore_exit_code=False, quiet=False):
        """run a series of commands in the shell, returning False immediately
         if one in the series exits with any non-zero value. Otherwise returns True.
         IO redirection does not work with this method. 

        commands are run using subprocess.Popen(bufsize=1, stdout=PIPE, stderr=PIPE, text=True)

        
        @param cmds: list of strings, each of which is a single shell command,
        such as "mv src dest".  
        @param logall: if True, log each command that is run, not just those, that fail.
        @param ignore_exit_code: don't return if one of cmds returns non-zero.
        @param quiet: don't print stdout content as the subprocess makes it 
        available. 
        """
        with open(self.full_transcript, 'a') as ft:
            ft.writelines(f'ACTION: {self.curraction}\n')
            
            for x in cmds:
                ft.writelines(f'\tCMD: {x}\n')
                try:
                    cmd = shlex.split(x)
                    with Popen(cmd, bufsize=1, stdout=PIPE, stderr=STDOUT, text=True) as p:
                        # print stdout
                        for line in p.stdout:
                            ft.writelines(f'\t\t{line}\n')
                            if not quiet:
                                print(line, end='') 
                        # wait for subprocess to finish
                        p.wait()
                        if p.returncode != 0 and not ignore_exit_code:   
                                return False
                        else:
                            if logall:
                                self.log(True, x)
                except UnicodeDecodeError:
                    pass
                except:
                    estring = traceback.format_exc()
                    print(estring)
                    ft.writelines(['\t\tPYTHON EXCEPTION:\n\t\t\t'] + ['\n\t\t\t'.join(estring.split('\n'))] + ['\t\t\t\n'])
                    self.log(False, f'{x}\n\t{estring}')
                    return False
            
        return True


