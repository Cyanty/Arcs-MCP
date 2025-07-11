# -*- coding: utf-8 -*-

__author__ = 'cyanty'


def main():
    from web.app import app
    from config import WEB_SERVER_HOST, WEB_SERVER_PORT
    import uvicorn
    uvicorn.run(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == '__main__':
    main()
