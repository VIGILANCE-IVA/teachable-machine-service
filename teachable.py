import os

import cv2 as cv
import numpy as np
from tensorflow.keras.models import load_model

dirname, filename = os.path.split(os.path.abspath(__file__))

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

class TeachableModel:
    def __init__(self, model_path, labels_path):
        self.mode_path = model_path
        self.labels_path = labels_path
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.load_model()

    def set_model(self, model_path, labels_path):
        self.mode_path = model_path
        self.labels_path = labels_path
        # reload model
        self.load_model()

    def load_model(self):
        try: 
            self.model = load_model(self.mode_path)
            self.labels = self.gen_labels(self.labels_path)
        except:
            print("Failed to load model!")

    def gen_labels(self, path):
        labels = {}
        with open(path, "r") as label:
            text = label.read()
            lines = text.split("\n")
            for line in lines[0:-1]:
                hold = line.split(" ", 1)
                labels[hold[0]] = hold[1]
        return labels

    async def predict(self, frame):
        frame = cv.resize(frame, (224, 224))
        image_array = np.asarray(frame)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        self.data[0] = normalized_image_array
        pred = self.model.predict(self.data)

        predictions = []

        for index, key in enumerate(self.labels):
            predictions.append({
                'class': self.labels[key],
                'confidence': pred[0][index]
            })


        return predictions

model = TeachableModel(
    model_path="{}/data/keras_model.h5".format(dirname), 
    labels_path="{}/data/labels.txt".format(dirname)
)
