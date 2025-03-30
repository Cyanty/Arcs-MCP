# -*- coding: utf-8 -*-

__author__ = 'cyanty'


def main(host, port):
    from web.app import app
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    main(host="127.0.0.1", port=8000)

