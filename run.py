#! /usr/bin/env python3
"""
Runs counterpartyd or the counterpartyd test suite via the python interpreter in its virtualenv on both Linux and Windows
"""
import os
import sys
import subprocess

assert os.name in ("nt", "posix")

#under *nix, script must NOT be run as root
if os.name == "posix" and os.geteuid() == 0:
    print("Please run this script as a non-root user.")
    sys.exit(1)

run_tests = False
run_counterblockd = False
run_armory_utxsvr = False
args = sys.argv[1:]
if len(sys.argv) >= 2 and sys.argv[1] == 'tests':
    run_tests = True
    args = sys.argv[2:]
elif len(sys.argv) >= 2 and sys.argv[1] == 'csfrblockd':
    run_counterblockd = True
    args = sys.argv[2:]
elif len(sys.argv) >= 2 and sys.argv[1] == 'armory_utxsvr':
    run_armory_utxsvr = True
    args = sys.argv[2:]
    
base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
env_path = os.path.join(base_path, "env")
dist_path = os.path.join(base_path, "dist")
python_path = os.path.join(env_path, "Scripts" if os.name == "nt" else "bin", "python.exe" if os.name == "nt" else "python")

if run_tests:
    pytest_path = os.path.join(env_path, "Scripts" if os.name == "nt" else "bin", "py.test.exe" if os.name == "nt" else "py.test")
    counterpartyd_tests_path = os.path.join(dist_path, "csfrd", "test", "test_.py")
    command = "%s %s %s" % (pytest_path, counterpartyd_tests_path, ' '.join(args))
elif run_counterblockd:
    counterblockd_env_path = os.path.join(base_path, "env.csfrblockd")
    counterblockd_python_path = os.path.join(counterblockd_env_path, "Scripts" if os.name == "nt" else "bin", "python.exe" if os.name == "nt" else "python")
    counterblockd_path = os.path.join(dist_path, "csfrblockd", "csfrblockd.py")
    command = "%s %s %s" % (counterblockd_python_path, counterblockd_path, ' '.join(args))
elif run_armory_utxsvr:
    armory_utxsvr_env_path = os.path.join(base_path, "env.csfrblockd") #use the csfrblock venv
    armory_utxsvr_python_path = os.path.join(armory_utxsvr_env_path, "Scripts" if os.name == "nt" else "bin", "python.exe" if os.name == "nt" else "python")
    armory_utxsvr_path = os.path.join(dist_path, "csfrblockd", "armory_utxsvr.py")
    command = "DISPLAY=localhost:1.0 xvfb-run --auto-servernum %s %s %s" % (armory_utxsvr_python_path, armory_utxsvr_path, ' '.join(args))
else: #run csfrd
    counterpartyd_path = os.path.join(dist_path, "csfrd", "csfrd.py")
    command = "%s %s %s" % (python_path, counterpartyd_path, ' '.join(args))

status = subprocess.call(command, shell=True)
sys.exit(status)
