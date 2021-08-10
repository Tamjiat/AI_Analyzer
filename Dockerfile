FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-runtime

COPY . /root
WORKDIR /root

RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

RUN conda install pip

RUN pip install pip -U
RUN pip install -r requirements.txt