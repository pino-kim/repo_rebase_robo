#!/usr/bin/python3

import sys
import subprocess
import argparse

is_repo_work = False

def check_repo_work() :
   ret = subprocess.call(['repo'], shell=True ,stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

   if  ret == 1 :
      print("Not ready to run repo command")
      print("Checkc repo install first and Run ""repo init"" frist, terminate")
      sys.exit()
   else :
      print("Ready to run repo command")
      return True

def check_branch_exist(branch_name) :
   if check_repo_work() :
      console_out = subprocess.check_output(['repo branch'], shell=True, stderr=subprocess.STDOUT)

   console_out_tmp = console_out
   console_out_tmp = console_out_tmp.split()
   console_out_tmp = [x.decode('utf-8') for x in console_out_tmp]

   if branch_name in console_out_tmp :
      print('branch exit')
      return True
   else :
      print('branch not exit')
      return False

def check_rebased_branch(rebased_branch_name) :
   branch_name_temp = rebased_branch_name
   if check_branch_exist(branch_name_temp) is True :
      print("Rebased branch is already exit, Remove branch first, terminate")
      # print("If you want Reset branch, use option -f" run command force)
      sys.exit()
   else :
      print("rebased branch is not exit, run next command")
      return True

def check_upstream_branch(upstream_branch_name) :
   branch_name_temp = upstream_branch_name
   if check_branch_exist(branch_name_temp) is True :
      print("upsrem branch is exit")
      return True
   else :
      print("upsteam branch is not exit, terminate")
      sys.exit()

def verify_branch_exit(rebased_branch_name, upstream_branch_name):
    ret = check_rebased_branch(rebased_branch_name)
    ret = check_upstream_branch(upstream_branch_name)
    return ret

def run_rebase_work(rebased_branch_name, upstream_branch_name, run_process=4) :
   ret = verify_branch_exit(rebased_branch_name, upstream_branch_name)

   #repo comd set
   repo_forall = "repo forall "
   repo_forall_option = '-c'
   if run_process > 0 :
      repo_forall_option += "j"+ str(run_process)

   #test run_process
   print(run_process)

   # repo forall cmd should be join git cmd
   repo_cmd_do_forall = repo_forall \
                        + repo_forall_option \
                        + ' '

   # git cmd set
   git_checkout_cmd = 'git checkout '
   git_checkout_option = '-B'
   git_rebase_cmd = 'git rebase '

   # git cmd should be run with repo cmd
   git_cmd_do_checkout = git_checkout_cmd \
                         + git_checkout_option \
                         + ' ' \
                         + rebased_branch_name \
                         + ' ' \
                         + upstream_branch_name
   git_cmd_do_rebase = git_rebase_cmd \
                       + ' '\
                       + upstream_branch_name

   #run cmd set
   run_repo_checkout = repo_cmd_do_forall + git_cmd_do_checkout
   run_repo_rebase = repo_cmd_do_forall + git_cmd_do_rebase

   # checkout all git
   if ret is True :
      subprocess.call([run_repo_checkout], shell=True ,stderr=subprocess.STDOUT)

   # rebase all git
   if ret is True :
      subprocess.call([run_repo_rebase], shell=True, stderr=subprocess.STDOUT)

def main() :
   parser = argparse.ArgumentParser(description='This is repo rebase robo')

   parser.add_argument('rebased_branch', type=str,
                       help="What is the rebased branch name?")
   parser.add_argument('upstream_branch', type=str,
                       help="What is the upstream branch name?")
   parser.add_argument('-j', type=int,
                       help='How many process will you run repo command?')
   #parser.add_argument('-f','--force', default,
                       #help='What operation?')

   # parsing args
   args = parser.parse_args()
   rebased_branch_name = args.rebased_branch
   upstream_branch_name = args.upstream_branch
   run_process =args.j

   #run run_rebase_work
   run_rebase_work(rebased_branch_name, upstream_branch_name, run_process)

if __name__ == "__main__":
   main()
