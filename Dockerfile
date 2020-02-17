from debian:stable

run apt-get update
run apt-get install -y \
        python3 \
        python3-dev \
        python3-distutils \
        build-essential \
        gcc \
        liblapack-dev \
        libblas-dev \
        gfortran
add https://bootstrap.pypa.io/get-pip.py get-pip.py
run python3 get-pip.py
run pip3 install numpy
run pip3 install \
        ipython \
        scipy \
        pymc \
        matplotlib \
        requests \
        scikit-learn \
        gpy \
        gpyopt
run pip3 install ipython[all]
run apt-get install -y git
run git clone https://github.com/saffsd/langid.py /src/langid.py
run pip3 install /src/langid.py
run git clone  https://github.com/myleott/ark-twokenize-py /src/ark-twokenize-py
run pip3 install geopy
run pip3 install unidecode

workdir /src/meetup
run cp /src/ark-twokenize-py/twokenize.py /src/meetup/twokenize.py
run useradd -m ipython
expose 8888
run chown ipython .

volume /src/meetup/data

user ipython

cmd ["ipython", "notebook", "--ip", "0.0.0.0", "--no-browser"]
