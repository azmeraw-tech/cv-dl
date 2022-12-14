import tensorflow as tf
import data_utils
import check
import os
import cv2
import numpy as np
import pathlib
import argparse
from PIL import Image
import numpy
from tensorflow.python.client import device_lib

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #gets rid of avx/fma warning


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # bools
    parser.add_argument('--train', help='Train the model', action="store_true")
    parser.add_argument('--test', help='Run PSNR test on an image', action="store_true")
    parser.add_argument('--downsample_type', type=str, default='desubpixel')
    parser.add_argument('--conv_type', type=str, default='default')
    parser.add_argument('--upscale', help='Upscale an image with desired scale', action="store_true")
    parser.add_argument('--export', help='Export the model as .pb', action="store_true")
    parser.add_argument('--fromscratch', help='Load previous model for training',action="store_false")

    # numbers
    parser.add_argument('--quant', type=int, help='Quantize to shrink .pb file size. 1=round_weights. 2=quantize_weights. 3=round_weights&quantize.', default=0)
    parser.add_argument('--B', type=int, help='Number of resBlocks', default=32)
    parser.add_argument('--F', type=int, help='Number of filters', default=16)
    parser.add_argument('--scale', type=int, help='Scaling factor of the model', default=2)
    parser.add_argument('--batch', type=int, help='Batch size of the training', default=16)
    parser.add_argument('--epochs', type=int, help='Number of epochs during training', default=20)
    parser.add_argument('--lr', type=float, help='Learning_rate', default=0.0001)

    # paths
    parser.add_argument('--image', help='Specify test image', default="./images/original.png")
    parser.add_argument('--traindir', help='Path to train images')
    parser.add_argument('--validdir', help='Path to train images')
    args = parser.parse_args()

    # INIT
    scale = args.scale
    meanbgr = [110.3456, 112.3421, 115.6739]

    # Set checkpoint paths for different scales and models
    ckpt_path = ""
    if scale == 2:
        ckpt_path = "./checkPoint/x2/"
    elif scale == 3:
        ckpt_path = "./checkPoint/x3/"
    elif scale == 4:
        ckpt_path = "./checkPoint/x4/"
    else:
        print("No checkpoint directory. Choose scale 2, 3 or 4. Or add checkpoint directory for this scale.")
        exit()

    # Set gpu
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    # Create run instance
    run = run.run(config, ckpt_path, scale, args.batch, args.epochs, args.B, args.F, args.lr, args.fromscratch, meanbgr)

    if args.train:
        run.train(args.traindir,args.validdir)

    if args.test:
        run.testFromPb(args.image)

    if args.upscale:
        run.upscaleFromPb(args.image)


    if args.export:
        run.export(args.quant)

    print("oh! success.")