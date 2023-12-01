import subprocess

# Lista delle librerie da installare
libraries_to_install = ['opencv-python', 'numpy', 'moviepy', 'ttkbootstrap', 'ttkthemes', 'imageio', 'imageio-ffmpeg']

# Installa le librerie usando pip
for library in libraries_to_install:
    subprocess.call(['pip', 'install', library])
