import json

import cv2 as cv
import numpy as np
from aiohttp.web import Response, View
from aiohttp_cors import CorsViewMixin
from core_utils.json import jsonify
from teachable import model


class PredictionApi(View, CorsViewMixin):
    async def post(self):
        try:
            body = await self.request.post()
            # decode image
            img = cv.imdecode(np.fromstring(body['image'].file.read(), np.uint8), cv.IMREAD_UNCHANGED)
            predictions = await model.predict(img)

            return Response(
                text=jsonify(predictions),
                content_type="application/json",
                status=200
            )

        except BaseException as e:
            return Response(
                text=json.dumps({'message': str(e)}),
                content_type="application/json",
                status=400
            )
