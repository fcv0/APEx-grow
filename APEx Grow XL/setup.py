import os, subprocess

def install_dependencies():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print('Dependencies successfully installed')
    except subprocess.CalledProcessError as e:
        print(f'Error: failed to install {e}')

if __name__ == '__main__':
    install_dependencies()