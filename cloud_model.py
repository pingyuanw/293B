import torch
import torchvision
from torchvision import transforms, models

from PIL import Image

import matplotlib.pyplot as plt
import numpy as np

import torch.nn as nn
import torch.nn.functional as F

import torch.optim as optim

import boto3

class MyDataset(torch.utils.data.Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform
        
    def __getitem__(self, index):
        # image_path = self.image_paths[index]
        image_path = './img/dog.jpg'
        x = Image.open(image_path)
        if self.transform is not None:
            x = self.transform(x)
        return x, 0
    
    def __len__(self):
        return len(self.image_paths)

def download_model(filename):
    return torch.load('./'+filename)
    # s3 = boto3.client('s3')
    # s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')

def upload_model(filename):
    torch.save(model.state_dict(), './'+filename)
    # s3 = boto3.client('s3')
    # s3.upload_file(file_name, bucket, object_name)

def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

def test_model(model, testset):
    
    testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                             shuffle=False, num_workers=2)

    classes = ('plane', 'car', 'bird', 'cat',
               'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

    dataiter = iter(testloader)
    images, labels = dataiter.next()
    imshow(torchvision.utils.make_grid(images))
    print('GroundTruth: ', ' '.join('%5s' % classes[labels[j]] for j in range(4)))
    outputs = model(images)
    _, predicted = torch.max(outputs, 1)

    print('Predicted: ', ' '.join('%5s' % classes[predicted[j]]
                                  for j in range(4)))

transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
def create_model(PATH):
    # load dataset: use CIFAR10
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                            download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                              shuffle=True, num_workers=2)

    # trained model: use resnet18
    model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet18', pretrained=True)

    # set model
    for param in model.parameters():
        param.requires_grad = False

    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 10)

    criterion = nn.CrossEntropyLoss()

    # Observe that all parameters are being optimized
    optimizer = optim.SGD(model.fc.parameters(), lr=0.001, momentum=0.9)

    # train
    # Iterate over data.
    i = 0
    for data in trainloader:
        # get the inputs
        inputs, labels = data

        # wrap them in Variable
        # inputs, labels = Variable(inputs), Variable(labels)

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward
        outputs = model(inputs)
        _, preds = torch.max(outputs.data, 1)
        loss = criterion(outputs, labels)

        # backward + optimize only if in training phase
        loss.backward()
        optimizer.step()

        i += 1
        # only for test
        if i == 100:    
            break

    testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
    test_model(model, testset)

    upload_model(model, 'test.pth')
  
def update_model(filename, PATH):
    # 1. load model
    model = models.resnet18(pretrained=True)
    for param in model.parameters():
        param.requires_grad = False

    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 10)

    model.load_state_dict(download_model(filename))

    # 2. load dataset
    trainset = MyDataset(image_paths=PATH, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=4, shuffle=True, num_workers=2)
    

    # self training


    dataiter = iter(trainloader)
    images, labels = dataiter.next()
    test_model(model, trainset)

    # upload_model(model, 'test2.pth')

def predict(model, filename):
    # sample execution (requires torchvision)
    input_image = Image.open(filename)
    input_tensor = transform(input_image)
    input_batch = input_tensor.unsqueeze(0) # create a mini-batch as expected by the model

    with torch.no_grad():
        output = model(input_batch)
    print(output[0])


# create_model('test.pth')
update_model('./test.pth', './img')
