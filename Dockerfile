# Install Images
FROM python:3.6.15-slim

# Set working directory
WORKDIR /home/app

# Install packages
RUN apt-get update -y && apt-get upgrade -y && \
apt-get install ffmpeg libsm6 libxext6 -y && \
apt-get install tk -y && \
apt-get install -y libglib2.0-0 libxrender1 && \
apt-get install -y --no-install-recommends git

# Copy all files into working directory
COPY app.py download_model.py requirements.txt /home/app/

# Copy test images directory
COPY test_images/ /home/app/test_images/

# Download all packages python
RUN git clone https://github.com/nodefluxio/vortex.git && \
	cd vortex/ && git checkout drop-enforce && \
	pip install ./src/runtime[onnxruntime] && cd ../ && \
	pip install -r requirements.txt

# Instal python libraries
RUN pip install -r requirements.txt

# Download Model
RUN python download_model.py

# Run script
ENTRYPOINT ["python", "app.py"]