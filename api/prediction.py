import json

import cv2 as cv
import numpy as np
from aiohttp.web import Response, View
from aiohttp_cors import CorsViewMixin
from core_utils.json import jsonify
from teachable import model
from teachable_video import teachable_video


class PredictionApi(View, CorsViewMixin):
    async def post(self):
        body = await self.request.post()
        # decode image
        img = cv.imdecode(np.fromstring(body['image'].file.read(), np.uint8), cv.IMREAD_UNCHANGED)
        predictions = model.predict(img)

        return Response(
            text=jsonify(predictions),
            content_type="application/json",
            status=200
        )

class VideoPredictionApi(View, CorsViewMixin):
    async def post(self):
        body = await self.request.json()
        task_id = await teachable_video.add_task(body)

        return Response(
            text=jsonify({'task_id': task_id }),
            content_type="application/json",
            status=200
        )

    async def put(self):
        body = await self.request.json()
        await teachable_video.stop_task(body['task_id'])

        return Response(
            text=jsonify({'task_id': body['task_id'] }),
            content_type="application/json",
            status=200
        )
