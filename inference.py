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

class Inference:
	def __init__(self, aws_access_key_id, aws_secret_access_key):
		self.aws_access_key_id = aws_access_key_id
		self.aws_secret_access_key = aws_secret_access_key
		self.filename = "model.pth"
		self.classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
		self.MODEL_UPDATE_INTERVAL = 10 ## in seconds

		if (os.path.exists(self.filename) == False):
			s3 = boto3.client('s3',aws_access_key_id = self.aws_access_key_id, aws_secret_access_key = self.aws_secret_access_key)
			print("Downloading model...\n")
			s3.download_file('hummingbird-293', 'model', self.filename)
			print("Download complete!\n")
		self.model = self.load_model(self.filename)
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

		transform = transforms.Compose([
			transforms.Resize(256),
			transforms.CenterCrop(224),
			transforms.ToTensor(),
			transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
		])

		#input_image = Image.open(imgfilename)
		input_tensor = transform(img)
		input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

		with torch.no_grad():
			outputs = self.model(input_batch)
		_, predicted = torch.max(outputs, 1)
		print('Predicted: ', ' '.join('%5s' % self.classes[predicted[j]] for j in range(1)))
		return self.classes[predicted[0]]

	def update_model(self, sc):
		## To DO
		
		while True:
			time.sleep(self.MODEL_UPDATE_INTERVAL)
			print("Updating model...\n")
		
		return