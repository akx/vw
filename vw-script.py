# -- encoding: utf-8 --
from __future__ import with_statement
import argparse
import os
import sys
import virtualenv

ENVS_PATH = os.path.join(os.environ["USERPROFILE"], "envs")

def gen_activation_script(env_path):
    activation_script = []
    activation_script.append("call \"%s\"" % os.path.join(env_path, "Scripts", "activate.bat"))
    workdir_file = os.path.join(env_path, "workdir")
    if os.path.isfile(workdir_file):
        activation_script.append("cd /d \"%s\"" % file(workdir_file, "rb").read())
    return "\n".join(activation_script)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("env")
    ap.add_argument("-w", "--workdir", dest="workdir")
    args = ap.parse_args()
    env_path = os.path.join(ENVS_PATH, args.env)
    if not os.path.isdir(env_path):
        if raw_input("%s (for %s) does not exist. Create new virtualenv? [y/n] " % (env_path, args.env)) == "y":
            virtualenv.logger = virtualenv.Logger([(virtualenv.Logger.NOTIFY, sys.stdout)])
            virtualenv.create_environment(env_path, site_packages=True, unzip_setuptools=True)
        else:
            print "Abort."
            sys.exit(1)

    if args.workdir:
        workdir = os.path.realpath(args.workdir)
        if os.path.isdir(workdir):
            print "Setting environment %s workdir to '%s'." % (args.env, workdir)
            file(os.path.join(env_path, "workdir"), "wb").write(workdir)
    
    activation_script_path = os.environ.get("VW_ACTSCRIPT_PATH")
    if not activation_script_path:
        print "VW_ACTSCRIPT_PATH not set, not creating activation script"
    else:
        with file(activation_script_path, "wb") as actscript:
            actscript.write(gen_activation_script(env_path))

if __name__ == '__main__':
    main()