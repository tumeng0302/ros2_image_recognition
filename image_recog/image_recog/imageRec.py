import cv2
import torch
import numpy as np
import image_recog.label as label
from torchvision import transforms
from torchvision import models

torch.backends.quantized.engine = 'qnnpack'

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

net = models.quantization.mobilenet_v2(weights="MobileNet_V2_QuantizedWeights.DEFAULT", quantize=True)
net = torch.jit.script(net)
def main(image):
    image = image[:, :, [2, 1, 0]]
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)
    output = net(input_batch)

    top = list(enumerate(output[0].softmax(dim=0)))
    top.sort(key=lambda x: x[1], reverse=True)
    classes=label.label
    idx,val=top[0]
    result=("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nthe result is :%s,the accuracy is %.2f %%"%(classes[idx],val.item()*100))
    return result

if __name__=="__main__":
    pass
