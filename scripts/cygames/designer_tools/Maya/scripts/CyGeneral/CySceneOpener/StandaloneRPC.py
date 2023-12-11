#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# StandaloneRPC.py
#

from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
except Exception:
    pass

try:
    # Maya 2022-
    from urllib.parse import parse_qs
    from urllib.parse import urlencode
    from urllib.request import urlopen
except Exception:
    from urlparse import parse_qs
    from urllib import urlencode
    from urllib2 import urlopen

import os
import json
import traceback
from wsgiref.simple_server import make_server
import maya.cmds as cmds
import maya.mel as mel
import RenderSettings


class CMD(str):
    def __new__(cls, cmd, *args, **kwargs):
        result = {'command': str(cmd)}
        if args:
            result['args'] = json.dumps(args)
        if kwargs:
            result['kwargs'] = json.dumps(kwargs)
        return urlencode(result)


def send_command(cmd, address='localhost', port=8000):
    url = "http://{address}:{port}/?{cmd}".format(
        address=address, port=port, cmd=cmd)
    q = urlopen(url)
    raw = q.read()
    try:
        results = json.loads(raw)
        return results
    except:
        raise ValueError("Could not parse server responss", raw)


def handle_command(environ, response):
    maya.standalone.initialize()

    project_path = cmds.internalVar(userAppDir=True) + "temp"
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    cmds.workspace(project_path, openWorkspace=True)

    if not environ.get('QUERY_STRING'):
        status = '404 Not Found'
        headers = [('Content-type', 'text/plain')]
        response(status, headers)
        return ["You must supply a command as a query string"]

    query = parse_qs(environ['QUERY_STRING'])
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    response(status, headers)

    cmds_string = query.get('command')
    if not cmds_string:
        return ['No recognized command']

    cmd_name = "-"
    args = "-"
    kwargs = "-"

    try:
        cmd_name = cmds_string[0]
        args = query.get('args') or []
        if args:
            args = json.loads(args[0])

        kwargs = query.get('kwargs') or {}
        if kwargs:
            unicode_kwargs = json.loads(kwargs[0])
            kwargs = dict((str(k), v) for k, v in list(unicode_kwargs.items()))

        cmd_proc = eval(cmd_name)
        if cmd_name == 'shutdown':
            try:
                return ['SERVER SHUTTING DOWN']
            finally:
                cmd_proc()

        result = cmd_proc(*args, **kwargs)
        result_js = {'success': True, 'result': result}
        return [json.dumps(result_js)]

    except:
        result_js = {"success": False,
                     "cmd_name": cmd_name,
                     "args": str(args) or "-",
                     "kwargs": str(kwargs)or "-",
                     "exception": str(sys.exc_info()[0]),
                     "traceback": traceback.format_exc()}
        return [json.dumps(result_js)]


def create_server(port=None):
    port = port or 8000
    address = 'localhost'
    server = make_server(address, port, handle_command)
    return server, address, port


def shutdown():
    print("*" * 80)
    print("shutting down")
    print("*" * 80)
    cmds.quit(force=True)
    server_instance.shutdown()
    raise sys.exit(0)


if __name__ == '__main__':
    import sys
    import maya
    import maya.standalone

    server_instance, address, port = create_server()

    print("=" * 80)
    print(("starting server on %s:%s" % (address, port)).center(80))
    print("=" * 80)
    
    server_instance.serve_forever()
