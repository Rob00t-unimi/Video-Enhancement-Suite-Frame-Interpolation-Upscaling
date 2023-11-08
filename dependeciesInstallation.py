import subprocess

# Lista delle librerie da installare
libraries_to_install = ['opencv-python', 'numpy', 'matplotlib', 'ttkbootstrap', 'ttkthemes']

# Installa le librerie usando pip
for library in libraries_to_install:
    subprocess.call(['pip', 'install', library])
