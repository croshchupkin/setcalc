This is a mini-project for calculating set members' interrelations.
For general CLI help, call ./setcalc.sh --help
For the grammar describing the syntax of the command, see grammar.txt.

-------------------------------------------------------------------------------
                                   WARNING!
-------------------------------------------------------------------------------
At the moment, setcalc.sh can only be run directly from the project root.
Otherwise, the relative paths will break.

Also, bin/setup.sh and bin/run.sh expect python3.7+, related pip executable and
the python3 venv package to be already install and visible on PATH.
On contemporary Ubuntu, these can usually be installed from these packages:
- python3 (should be already installed from the start)
- python3-pip (or possibly a manual global install for the correct interpreter
  version)
- python3-venv

Also, to simplify the parsing of file paths by lark, these may either be
double quotes-delimited strings or strings containing no whitespace and
starting with "/", ".", "~" or anything that matches the \w regex character
class, followed by any symbol except for whitespace.

-------------------------------------------------------------------------------
                             RUNNING THE COMMAND
-------------------------------------------------------------------------------
Just run ./setcalc.sh from the project root.
`./setcalc.sh --help` will display a brief CLI help message
`./setcalc.sh COMMAND` will run the command
`./setcalc.sh --grammar-file FILE COMMAND` will point to a non-default grammar
definition and run the command.

General COMMAND syntax:
`[ EQ|GR|LE NUMBER OPERAND+ ]`

Available operations:
EQ - return the unique (sorted) integers which exist in exactly NUMBER OPERANDs
LE - same, but existing in less than NUMBER OPERANDs
GR - same, but existing in more than NUMBER OPERANDs

OPERAND can be a path to a file or a nested COMMAND.

files are expected to contain only a single integer on each new line.

In this case, COMMAND means the full command, e.g.:
`./setcalc.sh [ GR 1 test/c.txt [ EQ 3 test/a.txt test/a.txt test/b.txt ] ]`

Running the command for the first time will check if a vitualenv exists in the
current directory and set it up with bin/setup.sh if it doesn't.

After that, each invocation of setcalc.sh will just activate the virtualenv,
execute the `setcalc` package with `python -m` (passing through all of the
CLI arguments), and deactivate the virtualenv.
-------------------------------------------------------------------------------
                             TROUBLESHOOTING
-------------------------------------------------------------------------------
If you encountered the following error:
ModuleNotFoundError: No module named 'lark'
the virtual environment has most likely been set up with errors. Re-running
bin/setup.sh from the project root should fix the issue

-------------------------------------------------------------------------------
                            INVOCATION EXAMPLES
-------------------------------------------------------------------------------
First invocation:
```
$ ./setcalc.sh [ GR 1 test/c.txt [ EQ 3 test/a.txt test/a.txt test/b.txt ] ]
(re)Creating virtual environment...
Done.
Installing dependencies...
Collecting lark==0.11.1
  Using cached lark-0.11.1-py2.py3-none-any.whl (93 kB)
Installing collected packages: lark
Successfully installed lark-0.11.1

2
3
```

Regular invocation:
```
$ ./setcalc.sh [ GR 1 test/c.txt [ EQ 3 "test/a.txt" ~/projects/setcalc/test/a.txt "./test/b.txt" ] ]
2
3
```
```
$ ./setcalc.sh [ EQ 1 test/a.txt test/a.txt test/b.txt [ LE 2 test/b.txt test/c.txt ] ]
4
5
```
Invocation without recusive commands:
```
$ ./setcalc.sh [ LE 2 test/b.txt test/c.txt ]
1
5
```

Specifying the grammar file explicitly:
```
$ ./setcalc.sh --grammar-file ./grammar.txt [ LE 2 test/a.txt [ GR 1 test/b.txt test/c.txt ] ]
1
4
```

Empty result:
```
$ ./setcalc.sh [ LE 1 test/a.txt test/a.txt ]
$
```
