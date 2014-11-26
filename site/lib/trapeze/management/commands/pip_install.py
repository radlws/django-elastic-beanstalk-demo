
import os
import subprocess
import glob
import datetime
from os.path import expanduser
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

#TODO: move to own module, import
def move_dir(root_src_dir, root_dst_dir):
    #Python - Move and overwrite files and folders
    import os
    import shutil
    #= 'Src Directory\'
    #root_dst_dir = 'Dst Directory\'
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
    shutil.rmtree(root_src_dir)

class Command(BaseCommand):
    args = '[<package1> <package2> <packageN> ...]'
    help = 'Install packages into your project using pip'

    option_list = BaseCommand.option_list + (
         #make_option('--update', action='store', default=None, help='Update/overwrite the specified packages.'),
         #make_option('--update', '-U', action='store_true', default=False, help='Update/overwrite the specified packages.'),
         make_option('--requirement', '-r', action='store', default=None, help='Install from a requirement file'),
         make_option('--path', '-p', action='store', dest='path', type='string', help='Path to install folder'),
    )    # TODO: update would install to tmp directory and then force move & clean up.
    # Install the stuff to tmp installl dependencies
    # For each folder in tmp dir, check if exists in lib dir, if exists, delete and move the new dir, otherwise just move
    # when done remove the tmp dir
    # os.listdir
    #if not os.path.exists(archive_dir):
    #    os.unlink()
    #os.rename(old_file_path, new_file_path)

    def handle(self, *args, **options):
        install_dir = options.get('path') or '../lib'

        pip_packages = args

        if len(pip_packages) < 1:
            raise Exception("A package name is required.")

        now = datetime.datetime.now() #- datetime.timedelta(0)
        tmp_dir = os.path.join(install_dir, 'tmp-{0:04d}-{1:02d}-{2:02d}'.format(now.year, now.month, now.day))
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)

        self.create_distutils_cfg()

        if not os.path.isdir(install_dir): #TODO: Ask to create the dir if does not exist?
            raise Exception("Couldn't find lib directory in project root.")

        for pip_package in pip_packages:
            try:
                #TODO: Test what happens if symlink exists ?
                print("Trying to install {0} using pip install...".format({pip_package}))
                print("WARNING: Updates will be made to installed apps & dependencies will be installed as well.")
                #print("WARNING: Dependencies will not be installed.")
                #status = subprocess.check_output(['pip', 'install',  '--target={0}'.format(install_dir), '--no-deps', pip_package])
                status = subprocess.check_output(['pip', 'install',  '--target={0}'.format(tmp_dir), pip_package])
                print status
                move_dir(tmp_dir, install_dir)
                #os.unlink(tmp_dir)

                status = "Successfully installed {0} to {1}".format(pip_package, install_dir)
                print status
            except subprocess.CalledProcessError:
                #print "WARNING: {0} installation failed, maybe already exists in {1} " \
                #      "or the package was not found.".format(pip_package, install_dir)
                #continue
                #print "An error occurred."
                pass
            finally:
                with open("{0}/install_history.txt".format(install_dir), "a") as f:
                    f.writelines("{0}:\n".format(datetime.datetime.now()))
                    f.writelines("./manage.py pip_install {0}\n".format(" ".join(pip_packages)))
                self.cleanup_info(install_dir)
        #sys.exit(self.return_code)

    def create_distutils_cfg(self):
        #fixes both prefix and home not allowed error
        #https://github.com/Homebrew/homebrew/wiki/Homebrew-and-Python
        home_dir = expanduser("~")
        distutils_file = os.path.join( home_dir, '.pydistutils.cfg')
        if not os.path.exists(distutils_file):
            with open(distutils_file,'w') as f:
                f.write('[install]\n')
                f.write('prefix=')


    def cleanup_info(self, install_dir):
        """ Clean Up of files at end of install """
        print("Removing egg and dist info files...")
        import shutil
        egg_info = glob.glob("{0}/*.egg-info".format(install_dir))
        egg_info += glob.glob("{0}/*.dist-info".format(install_dir))
        #print egg_info
        with open("{0}/install_history.txt".format(install_dir), "a") as f:
            f.write("Removed info files: ")
            for fl in egg_info:
                f.write("{0}".format(fl))
                shutil.rmtree(fl)
            f.write("\n")
        print("Done.")