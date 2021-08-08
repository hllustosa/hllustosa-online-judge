
SECCOMP_CODE = """
import sys
from pyseccomp import *

f = SyscallFilter(defaction=KILL)
f.add_rule(ALLOW, "read", Arg(0, EQ, sys.stdin.fileno()))
f.add_rule(ALLOW, "write", Arg(0, EQ, sys.stdout.fileno()))
f.add_rule(ALLOW, "write", Arg(0, EQ, sys.stderr.fileno()))
f.add_rule(ALLOW, "fstat")
f.add_rule(ALLOW, 'ioctl')
f.add_rule(ALLOW, 'sigaltstack')
f.add_rule(ALLOW, "rt_sigaction")
f.add_rule(ALLOW, "exit_group")
f.add_rule(ALLOW, "rt_sigaction")
f.add_rule(ALLOW, "rt_sigreturn")
f.add_rule(ALLOW, "exit_group")
f.add_rule(ALLOW, "brk")
f.add_rule(ALLOW, "select")
f.add_rule(ALLOW, "rt_sigprocmask")
f.add_rule(ALLOW, "pselect6")
f.load()


"""