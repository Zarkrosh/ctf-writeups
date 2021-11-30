import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

class SigmaNet:
    def __init__(self):
        self.name = 'sigmanet'
        self.model_filename = 'sigmanet.h5'
        try:
            self._model = load_model(self.model_filename)
            #print('Successfully loaded', self.name)
        except (ImportError, ValueError, OSError):
            print('Failed to load', self.name)

    def color_process(self, imgs):
        if imgs.ndim < 4:
            imgs = np.array([imgs])
        imgs = imgs.astype('float32')
        mean = [125.307, 122.95, 113.865]
        std = [62.9932, 62.0887, 66.7048]
        for img in imgs:
            for i in range(3):
                img[:, :, i] = (img[:, :, i] - mean[i]) / std[i]
        return imgs

    def predict(self, img):
        processed = self.color_process(img)
        #print(processed)
        return self._model.predict(processed)

    def predict_one(self, img):
        confidence = self.predict(img)[0]
        printSummary(confidence)
        predicted_class = np.argmax(confidence)
        return class_names[predicted_class]

def printSummary(confidence):
    s = []
    for i in range(len(class_names)):
        s.append((class_names[i], confidence[i]))
    s.sort(key=lambda tup: tup[1], reverse=True)

    print("\n".join("[{}] {}: {}".format(i+1, c[0], c[1]) for i, c in enumerate(s)))


def loadDoggo():
    return np.array(Image.open('./dog.png').convert('RGB'))


def getModifications(c, input):
    maxvalues = {
        'airplane': 0,
        'automobile': 0,
        'ship': 0,
        'truck': 0
    }

    input[24,11] = [0,0,0]
    input[18,25] = [0,0,0]
    input[11,19] = [0,0,0]
    input[15,9] = [0,0,0]
    input[27,10] = [0,0,0]

    for i in range(len(input)):
        for j in range(len(input[0])):
            m = np.copy(input)
            m[i,j] = [0,0,0]
            conf = c.predict(m)[0]
            for ind, cl in enumerate(class_names):
                if cl in maxvalues:
                    if conf[ind] > maxvalues[cl]:
                        maxvalues[cl] = conf[ind]
                        print("Mejor {}: {}, {}".format(cl, i,j))

    print(maxvalues)

# Byte negro:    {'airplane': 1.9082898e-05, 'automobile': 3.7039906e-06, 'ship': 1.2697326e-07, 'truck': 3.2554036e-07}  # Airplane: 1.9082898e-05
# 2 Byte negros: {'airplane': 0.06792607, 'automobile': 8.164704e-05, 'ship': 4.188802e-06, 'truck': 7.963142e-06}        # Airplane: 0.06792607
# 3 Byte negros: {'airplane': 0.7129731, 'automobile': 0.00015864061, 'ship': 4.5859574e-06, 'truck': 0.00018851801}      # Airplane: 0.7129731
# 4 Byte negros: {'airplane': 0.91452295, 'automobile': 0.0006314269, 'ship': 1.5140748e-05, 'truck': 0.00013077089}      # Airplane: 0.91452295
# 5 Byte negros: {'airplane': 0.994204, 'automobile': 0.00036032058, 'ship': 6.4925853e-06, 'truck': 0.000121623874}      # Airplane: 0.994204

c = SigmaNet()
doggo = loadDoggo()
#m = getModifications(c, doggo)
#print("\nResult: {}".format(c.predict_one(m)))

doggo[24,11] = [0,0,0] # 24,11,0,0,0
doggo[18,25] = [0,0,0] # 18,25,0,0,0
doggo[11,19] = [0,0,0] # 11,19,0,0,0
doggo[15,9] = [0,0,0]  # 15,9,0,0,0
doggo[27,10] = [0,0,0] # 27,10,0,0,0

# Win si lo clasifica como 'airplane', 'automobile', 'ship' o 'truck'
print("\nResult: {}".format(c.predict_one(doggo)))
#Image.fromarray(doggo.astype('uint8'), 'RGB').show()

# HTB{0ne_tw0_thr33_p1xel_attack}
