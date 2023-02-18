<div align="center">

# Face Detection and Recognition using Neural Network

**✨ Instructions for Raspberry PI boards ✨**

![raspberry-py-logo](https://cdn-icons-png.flaticon.com/32/5969/5969184.png)

</div>

---

## Install OpenCV dependencies

To get started, ensure you update your system by executing the commands below:

```shell
sudo apt update
sudo apt upgrade
```

Next, we will install the  _CMake_  developer tool necessary for building OpenCV. Execute the command below:

```shell
sudo apt install build-essential cmake pkg-config
```

We will also install additional libraries for opening image files on our computer. That includes JPG, JPEG, PNG, et. 
Execute the command below:

```shell
sudo apt install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
```

Other than images, we also need libraries that will enable the use of video files. Install these libraries with the 
commands below:

```shell
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install libxvidcore-dev libx264-dev
```

Now we have both images and videos sorted out. To display images on our computer screens and even develop Graphical User 
Interfaces (GUI) for our projects, we will need a module called  _highgui_. That will require us to install all the 
necessary GTK libraries. Execute the commands below:

```shell
sudo apt install libfontconfig1-dev libcairo2-dev
sudo apt install libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt install libgtk2.0-dev libgtk-3-dev
```

For carrying out matrix operations, we will need to install additional dependencies. Execute the command below.

```shell
sudo apt install libatlas-base-dev gfortran
```
If you wish to install OpenCV via pip, install the additional libraries below necessary for HD5 datasets and the 
development of QT GUIs. There will be no problem even if you install OpenCV via source code. Execute the commands below:

```shell
sudo apt install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt install libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5
```

Lastly, we will need to install Python 3 header files necessary for compiling OpenCV. Execute the commands below:

```shell
sudo apt install python3-dev
```


## Install Numpy and create a Python Virtual environment

Virtual environments are beneficial as they create an isolated environment for running your Python projects. Therefore, 
every project in a virtual environment has its own set of dependencies and libraries regardless of the libraries 
available for other projects.

To get started installing a virtual environment on our Raspberry, we will first need to install pip. Execute the 
commands below to install pip.

```shell
sudo apt-get install python3-pip
```

With pip installed, we can now proceed to install virtualenv and virtualenvwrapper. These are great packages that you 
can use to manage your virtual environments in Python. Execute the commands below.

```shell
sudo pip3 install virtualenv virtualenvwrapper
```

Once the installation completes, we will need to edit the .bashrc file and point to the locations of the virtualenv and 
virtualenvwrapper. Execute the command below to open the .bashrc file with the nano editor.

```shell
nano ~/.bashrc
```

Add the following lines at the bottom of the file.

```shell
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

Save the file (Ctrl + O, then Enter) and Exit (Ctrl + X). You will need to refresh the .bashrc file to apply the 
changes. Execute the command below.

```shell
source ~/.bashrc
```

Before getting started with OpenCV installation, we will need to create a virtual environment for our projects. Let’s 
call it sbb_cv. Execute the command below:

```shell
mkvirtualenv sbb_cv -p python3
```

You can use any name for the virtual environment, not necessarily sbb_cv. Additionally, if you are using a Raspberry Pi 
Camera for your projects, then you will need to install the PiCamera API with the command below:

```shell
pip3 install "picamera[array]"
```

Now we have all the necessary libraries, dependencies, and even a virtual environment set up. Let’s proceed to install 
OpenCV.

## Install OpenCV

As described above, we will look at two ways which you can use to install OpenCV on your Raspberry.

- Method 1 – Install OpenCV with pip.
- Method 2 – Install OpenCV from the source.

Please select one method which you will use for the rest of your installation process. You can’t use both.

### Method 1: Install OpenCV with pip on Raspberry

This method is one of the easiest and fastest ways to install OpenCV on your Raspberry Pi. I would highly recommend this 
for beginners and if you are time conscious since it only takes a couple of minutes. Execute the commands below.

If you had created a virtual environment, execute the command below to activate. If not, skip this step and proceed to 
install OpenCV

```shell
workon sbb_cv
```

You will notice the terminal prompt change and now start with the name of the virtual environment. To exit the virtual 
environment, use the deactivate command.

Once inside the virtual environment, you can now install OpenCV. Execute the command below.

```shell
pip3 install opencv-python
```

From the image above, you can see we have successfully installed OpenCV version 4.5.1.48. That’s it! You are done with 
OpenCV installation. To test OpenCV in your project, skip to the Test section at the bottom of the article.

### Method 2: Install OpenCV from the source

If you need a full installation of OpenCV, which includes patented algorithms, then you should use this method. Unlike 
the pip install method, which only takes a couple of minutes, compiling OpenCV from the source can take around two (2) 
hours. Follow the steps below:

#### Step 1. 
Activate your virtual environment with the workon command below.

```shell
workon sbb_cv
```

#### Step 2. 
Download the source code for both OpenCV and Opencv_contrib from Github. Use the wget commands below.

```shell
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.5.2.zip
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.5.2.zip
```

If you get an error like `wget command not found,` then you will need to install it with the command – `sudo apt install 
wget`

#### Step 3. 
We need to unzip the contents of the two files we downloaded. Use the unzip command as shown below:

```shell
unzip opencv.zip
unzip opencv_contrib.zip
```

#### Step 4. 
After extracting the zip files, we will have two folders – opencv-4.5.2 and opencv_contrib-4.5.1. Let’s rename these two 
to something memorable like opencv and opencv_contrib.

```shell
mv opencv-4.5.2 opencv
mv opencv_contrib-4.5.1 opencv_contrib
```

#### Step 5. 
Compiling OpenCV can be quite heavy on the Raspberry Pi memory. To avoid freezing or hanging, we can increase the SWAP 
space and utilize all four cores of the Pi in the compiling process. To do so, we will edit the dphys-swapfile present 
in the /etc. directory. Execute the command below to open dphys-swapfile with the nano editor.

```shell
sudo nano /etc/dphys-swapfile
```

Find the line – CONF_SWAPSIZE and set its value to 2048. See the image below.

Once done, save the file (Ctrl + O, then Enter) and Exit (Ctrl + X).

To apply the changes, restart the SWAP service with the commands below:

```shell
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
```

#### Step 6. 
Now, we have everything set to start compiling and installing OpenCV. Activate the virtual environment with the workon 
command.

```shell
workon sbb_cv
```

#### Step 7. 
Install Numpy with the pip command.

```shell
pip3 install numpy
```

#### Step 8. 
With NumPy installed, we can now start configuring OpenCV. Navigate to the OpenCV directory to get started.

Note: You need to be in the /opencv/build directory when executing the cmake command. You can use the pwd command to see 
your current working directory.

```shell
cd opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
    -D BUILD_EXAMPLES=OFF ..
```

The cmake command might take a couple of minutes to execute. Please be patient.

#### Step 9. 
We have already configured OpenCV for installation. Now let’s start compiling with all the Four cores of the Pi. Execute 
the command below:

```shell
make -j4
```
This is one of the longest steps. It might take between 1 to 4 hours, depending on the Raspberry Pi board you are using.
As of writing this post, Raspberry Pi 4 is the fastest.

#### Step 10. 
Once the compiling process completes without an ERROR, we can now install OpenCV. Execute the commands below:

```shell
sudo make install
sudo ldconfig
```

#### Step 11. 
Since we are done with installing OpenCV, we can reset the SWAP size to 100MB. Edit the /etc/dphys-swapfile and set the 
value of CONF_SWAPSIZE to 100MB as described in Step 5 above. Remember to Restart the swap service with the commands 
below:

```shell
sudo /etc/init.d/dphys-swapfile stop 
sudo /etc/init.d/dphys-swapfile start
```

#### Step 12. 
To finalize our installation, we will create symbolic links of cv2 to our virtual environment – in this case, sbb_cv.

Note: The Python version and the virtual environment in the commands below might not be similar to yours. Therefore, 
copy-pasting these exact commands might raise an error. I advise you use the tab button to autocomplete the commands for
you.

```shell
cd /usr/local/lib/python3.7/site-packages/cv2/python-3.7/
sudo mv cv2.cpython-37m-arm-linux-gnueabihf.so cv2.so
cd ~/.virtualenvs/sbb_cv/lib/python3.7/site-packages/
ln -s /usr/local/lib/python3.7/site-packages/cv2/python-3.7/cv2.so cv2.so
```

That’s it! We have successfully installed OpenCV on our Raspberry Pi and can now test it in our projects.