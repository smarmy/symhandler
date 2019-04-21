#!/usr/bin/env python3

import os
import os.path
import sys
import json

def usage_and_exit():
    print("Usage: symhandler.py <install|uninstall> FILE")
    sys.exit(1)


def yesno(what):
    response = ''
    valid = ['yes', 'no', 'y', 'n']
    while response.lower() not in valid:
        response = input(what + ' [y/N] ')
        if not response:
            response = 'n'
    return response.lower() == 'yes' or response.lower() == 'y'


def install(rc):
    '''
    Install symlinks pointed to by `rc`.
    The files to link to should be stated with relative path to where this
    script is run, so with a folder structure like:
    
      folder
      |-- rc.json
      |-- symlinks
          |-- foo
          |-- bar
    
    Then the rc file should look like:
    
      {
        "symlinks/foo": "target/directory/1",
        "symlinks/bar": "target/directory/2
      }

    The script will resolve the absolute paths of `foo` and `bar`.
    '''
    for path, sympath in rc.items():
        path = os.path.expandvars(path)
        sympath = os.path.expandvars(sympath)

        if not os.access(path, os.R_OK):
            print("No file '%s' found." % path)
            continue

        path = os.path.abspath(path)

        if os.access(sympath, os.R_OK):
            if yesno("'%s' exists, overwrite?" % sympath):
                os.unlink(sympath)
            else:
                continue

        try:
            os.symlink(path, sympath)
            print("Symlink created: '%s' => '%s'" % (path, sympath))
        except:
            print("Failed to create symlink: '%s' => '%s'" % (path, sympath))


def uninstall(rc):
    '''
    Uninstall symlinks. Will ask for every file.
    '''
    for _, sympath in rc.items():
        sympath = os.path.expandvars(sympath)

        if os.access(sympath, os.R_OK):
            if not os.path.islink(sympath):
                if yesno("'%s' is not symlink, really delete?" % sympath):
                    os.unlink(sympath)
            elif yesno("Really delete '%s'?" % sympath):
                os.unlink(sympath)
        else:
            print("No file '%s' found." % sympath)


def main():
    if len(sys.argv) != 3:
        usage_and_exit()

    action = sys.argv[1]
    with open(sys.argv[2], 'r') as f:
        rc = json.loads(f.read())

    if action == 'install':
        install(rc)
    elif action == 'uninstall':
        uninstall(rc)
    else:
        usage_and_exit()


if __name__ == '__main__':
    main()
