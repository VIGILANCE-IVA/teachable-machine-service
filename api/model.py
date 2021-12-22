import os
import pathlib

from aiohttp.web import Response, View
from aiohttp_cors import CorsViewMixin
from config import config
from teachable import model


class ModelApi(View, CorsViewMixin):
    async def post(self):
        body = await self.request.post()
        files = {}

        for ref in body:
            if hasattr(body[ref], '__class__'):
                item = body[ref]
                file_path = os.path.join('./', 'data', f'{ref}' + f'{pathlib.Path(item.filename).suffix}')
                files[ref] = file_path
                f = open(file_path, "wb")
                f.write(item.file.read())
                f.close()

        if 'model' in files:
            config.model = files['model']
        
        if 'labels' in files:
            config.labels = files['labels']

        if config.model and config.labels:
            model.set_config(config.model, config.labels)
            
        return Response(
            text='ok',
            status=200
        )
