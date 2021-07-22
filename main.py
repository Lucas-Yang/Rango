# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
fastapi 接口启动
"""
import multiprocessing
import uvicorn

from fastapi import FastAPI
from app.bin.controller import video_app
from app.user.controller import user_app

app = FastAPI()
app.include_router(video_app, prefix="/video")
app.include_router(user_app, prefix="/user")


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True, debug=True,
                workers=multiprocessing.cpu_count())
