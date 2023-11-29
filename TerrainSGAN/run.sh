tensorboard --host "0.0.0.0" --logdir="./logs" &
pip install tensorflow h5py pyyaml rasterio pillow
mkdir -p images
python ./TrainSGan.py