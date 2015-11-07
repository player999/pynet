import numpy as np
from images import *
import imread
import skimage.io
import skimage.color

#CONFIGURATION
from pynet_config import *

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224

import sys
sys.path.insert(0,CAFFE_ROOT + '/python')

import caffe

#Create labels map
if 'LABEL_FILE' in locals():
	labels = open(LABEL_FILE, 'r').readlines()
	labels_text = list(map(lambda x: x.split(' ')[0],labels))

caffe.set_mode_cpu()
net = caffe.Classifier(MODEL_FILE, PRETRAINED,
                       mean=np.load(MEAN_FILE).mean(1).mean(1),
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(IMAGE_WIDTH, IMAGE_HEIGHT))

def feedforward_file(image_fname):
	btes = open(image_fname, 'r').read()
	class_result = feedforward_bytes(btes)
	return class_result

def feedforward_bytes(image_bytes):
	src_float = skimage.img_as_float(imread.imread_from_blob(image_bytes)).astype(np.float32)
	if src_float.ndim == 1:
		src_float = skimage.color.gray2rgb(src_float)
	prediction = net.predict([src_float]) 
	return prediction

def classify_bytes(image_bytes):
	vector = feedforward_bytes(image_bytes)
	idx = np.argmax(vector)
	val = np.amax(vector)
	return val, idx

def classify_file(image_fname):
	return classify_bytes(open(image_fname, 'r').read())

def classify_file_label(image_fname):
	val, idx = classify_bytes(open(image_fname, 'r').read())
	lab_string = labels_text[idx]
	return val, lab_string

def classify_bytes_label(image_bytes):
	val, idx = classify_bytes(image_bytes)
	lab_string = labels_text[idx]
	return val, lab_string

