"""Set lib directory for current version of Python"""
import os
import subprocess
import sys

__version__ = '1.0.1'


def main():
    """Main"""
    lib_directory = None

    # All Python Version that will be searched
    lib_major_version = f'lib_{sys.version_info.major}'
    lib_minor_version = f'{lib_major_version}.{sys.version_info.minor}'
    lib_micro_version = f'{lib_minor_version}.{sys.version_info.micro}'

    # Get all "lib" directories
    app_path = os.getcwd()
    contents = os.listdir(app_path)
    lib_directories = [
        c
        for c in contents
        if c.startswith('lib') and os.path.isdir(c) and (os.access(c, os.R_OK))
    ]

    # reverse sort directories
    lib_directories.sort(reverse=True)

    # Find most appropriate FULL version
    lib_directory = None
    if lib_micro_version in lib_directories:
        lib_directory = lib_micro_version
    elif lib_minor_version in lib_directories:
        lib_directory = lib_minor_version
    elif lib_major_version in lib_directories:
        lib_directory = lib_major_version
    else:
        for lv in [lib_micro_version, lib_minor_version, lib_major_version]:
            for ld in lib_directories:
                if lv in ld:
                    lib_directory = ld
                    break
            else:
                continue
            break

    # No reason to continue if no valid lib directory found
    if lib_directory is None:
        print(f'Failed to find lib directory ({lib_directories}).')
        sys.exit(1)

    # Use this if you want to include modules from a subfolder
    # lib_path = os.path.realpath(
    #     os.path.abspath(
    #         os.path.join(
    #             os.path.split(inspect.getfile(inspect.currentframe()))[0], lib_directory)))
    lib_path = os.path.join(app_path, lib_directory)
    if 'PYTHONPATH' in os.environ:
        os.environ['PYTHONPATH'] = f"{lib_path}{os.pathsep}{os.environ['PYTHONPATH']}"
    else:
        os.environ['PYTHONPATH'] = f'{lib_path}'

    # Update system arguments
    sys.argv[0] = sys.executable
    sys.argv[1] = f'{sys.argv[1]}.py'

    # Make sure to exit with the return value from the subprocess call
    ret = subprocess.call(sys.argv)
    sys.exit(ret)


if __name__ == '__main__':
    main()
