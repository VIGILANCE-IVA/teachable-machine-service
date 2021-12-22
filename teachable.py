from os.path import abspath

import cv2 as cv
import numpy as np
from tensorflow.keras.models import load_model

from config import config


class TeachableModel:
    def __init__(self, model_path, labels_path):
        self.mode_path = model_path
        self.labels_path = labels_path
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.loaded = False
        self.load_model()

    def set_config(self, model_path, labels_path):
        self.mode_path = model_path
        self.labels_path = labels_path
        # reload model
        self.load_model()

    def load_model(self):
        try: 
            self.model = load_model(abspath(self.mode_path))
            self.labels = self.gen_labels(abspath(self.labels_path))
            self.loaded = True
        except:
            self.loaded = False
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

    def predict(self, frame):
        if not self.loaded:
            raise Exception('Model not loaded')

        frame = cv.resize(frame, (224, 224))
        image_array = np.asarray(frame)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        self.data[0] = normalized_image_array
        pred = self.model.predict(self.data)
        result = np.argmax(pred[0])
        predictions = []

        for index, key in enumerate(self.labels):
            predictions.append({
                'exact': self.labels[str(result)] == self.labels[key],
                'class': self.labels[key],
                'confidence': pred[0][index]
            })


        return predictions

model = TeachableModel(config.model, config.labels)
