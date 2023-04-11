import uuid
from collections import OrderedDict
from urllib import request

import cv2
from camera_threading.streamer import Capture
from core_utils.json import jsonify

from teachable import model


class TeachableVideo:
    def __init__(self):
        self.tasks = OrderedDict()

    def webhook(self, url, data):
        try:
            req = request.Request(url, data=jsonify(data).encode())
            req.add_header('Content-Type', 'application/json')
            request.urlopen(req)
        except Exception as e:
            print(str(e))

    async def add_task(self, data):
        if 'webhook' not in data:
            raise Exception("No webhook found!")
            
        if 'video_uri' not in data:
            raise Exception("No video found!")

        if 'delay' in data:
            delay = int(data['delay'])

        def on_frame(frame):
            cv2.imshow('Frame', frame)
            predictions = model.predict(frame)
            result = dict(data, **{ 'predictions': predictions })
            self.webhook(data['webhook'], result)

        id = str(uuid.uuid4())
        camera = Capture(data['video_uri'], delay)

        camera.on("frame", on_frame)
        camera.start()

        self.tasks[id] = {
            'data': data,
            'camera': camera
        }

        return id

    async def stop_task(self, task_id):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task['camera'].stop()
            self.tasks.pop(task_id)

        return task_id

teachable_video = TeachableVideo()
