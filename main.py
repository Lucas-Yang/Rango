# /usr/bin/env python
# -*- coding: utf-8 -*-
"""
fastapi 接口启动
"""
import argparse
import multiprocessing
import uvicorn

from fastapi import FastAPI
from app.bin.controller import video_app
from app.user.controller import user_app
from app.common.joker import buddha

app = FastAPI()
app.include_router(video_app, prefix="/video")
app.include_router(user_app, prefix="/user")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('-rl', '--reload', type=str, default=None, help="reload code")
    args = parser.parse_args()
    if args.reload:
        reload = False
    else:
        reload = True
    buddha()
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=reload, debug=reload,
                workers=multiprocessing.cpu_count())
