sudo apt update
sudo apt upgrade
sudo apt install build-essential cmake pkg-config
sudo apt install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install libxvidcore-dev libx264-dev
sudo apt install libfontconfig1-dev libcairo2-dev
sudo apt install libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt install libgtk2.0-dev libgtk-3-dev
sudo apt install libatlas-base-dev gfortran
sudo apt install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt install libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5
sudo apt install python3-dev
sudo apt-get install python3-pip
sudo pip3 install virtualenv virtualenvwrapper
touch ~/.bashrc
"# virtualenv and virtualenvwrapper" >> ~/.bashrc
"export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
"export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
"source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
mkvirtualenv sbb_cv -p python3
pip3 install "picamera[array]"
workon sbb_cv
pip3 install opencv-python
