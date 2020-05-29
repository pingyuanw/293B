import torch
import torchvision
from torchvision import transforms, models

from PIL import Image

import numpy as np

import torch.nn as nn
import torch.nn.functional as F

import torch.optim as optim

import boto3
import os

import sched
import time
import threading

import resnet
from collections import OrderedDict

class Inference:
	def __init__(self, aws_access_key_id, aws_secret_access_key):
		self.aws_access_key_id = aws_access_key_id
		self.aws_secret_access_key = aws_secret_access_key
		self.filename = "model.pth"
		self.classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
		self.MODEL_UPDATE_INTERVAL = 10 ## in seconds

		device = 'cuda' if torch.cuda.is_available() else 'cpu'
		print("device is : {}".format(device))
		self.net = resnet.ResNet50()
		self.net = self.net.to(device)

		if device == 'cuda':
			self.net = torch.nn.DataParallel(net)
			cudnn.benchmark = True

		if (os.path.exists(self.filename) == False):
			s3 = boto3.client('s3',aws_access_key_id = self.aws_access_key_id, aws_secret_access_key = self.aws_secret_access_key)
			print("Downloading model...\n")
			s3.download_file('hummingbird-293', 'Models/resnet50_ckpt.pth', self.filename)
			print("Download complete!\n")
		#self.model = self.load_model(self.filename)
		self.model = torch.load(self.filename,map_location=device)
		state = self.model['net']
		if device != 'cuda':
			new_state_dict = OrderedDict()
			for k,v in state.items():
				name = k[7:] # remove 'module.'
				new_state_dict[name] = v # load params
			self.net.load_state_dict(new_state_dict)
		else:
			#net.load_state_dict(state,map_location = 'cpu')
			self.net.load_state_dict(state)

		self.net.eval()
		#self.transformation = transforms.Compose([transforms.Resize((32,32)), transforms.ToTensor(),transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010),)])

		update_thread = threading.Thread(target=self.update_model, args=(1,))
		update_thread.start()

	def load_model(self, filename):
		
		model = models.resnet18(pretrained=True)
		for param in model.parameters():
			param.requires_grad = False

		num_ftrs = model.fc.in_features
		model.fc = nn.Linear(num_ftrs, 10)

		model.load_state_dict(torch.load('./'+filename))

		return model

	def predict(self, img):

#		transform = transforms.Compose([
#			transforms.Resize(256),
#			transforms.CenterCrop(224),
#			transforms.ToTensor(),
#			transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
#		])

		#input_image = Image.open(imgfilename)
		img = img.convert('RGB')
		transformation = transforms.Compose([transforms.Resize((32,32)), transforms.ToTensor(),transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010),)])
		img = transformation(img)
		input_batch = img.unsqueeze(0) # create a mini-batch as expected by the model
		pix = np.array(input_batch)
		image = torch.from_numpy(pix)

		with torch.no_grad():
			outputs = self.net(image)
		_, predicted = torch.max(outputs, 1)
		print('Predicted: ', ' '.join('%5s' % self.classes[predicted[j]] for j in range(1)))
		return self.classes[predicted[0]]

	def update_model(self, sc):
		## To DO
		
		while True:
			time.sleep(self.MODEL_UPDATE_INTERVAL)
			print("Updating model...\n")
		
		return