from pytorch_grad_cam import GradCAM
import cv2
from PIL import Image
from pytorch_grad_cam.utils.image import show_cam_on_image, preprocess_image
import numpy as np
import torchvision.transforms as transforms
import os
import matplotlib.pyplot as plt

def explain(model, img, org_img):

    org_img = np.float32(org_img) / 255


    target_layers = [model.features[-1]]

    cam = GradCAM(model=model, target_layers=target_layers, use_cuda=False)  # use_cuda=args.use_cuda
    grayscale_cam = cam(input_tensor=img, targets=None, aug_smooth=True, eigen_smooth=True)[0, :]
    visualization = show_cam_on_image(org_img, grayscale_cam, use_rgb=True, colormap=cv2.COLORMAP_JET)  #
    plt.imshow(visualization[0])
    plt.axis('off')
    fig = plt.gcf()
    plt.close()

    return fig

