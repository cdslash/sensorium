#!/usr/bin/env python3


import sys
from datetime import datetime
from pathlib import Path
from bottle import route, run, request


def mylog(*arg):
	print(datetime.now(), *arg, file=sys.stdout)


def mkdir_today(basedir='./upload'):
	now = datetime.now()
	datapath = Path(basedir) / Path(now.strftime("%Y%m%d"))
	mylog(f"mkdir {datapath}")
	datapath.mkdir(parents=True, exist_ok=True)
	return datapath


@route('/', method='GET')
def home_get():
	mylog("got GET /")
	return ('Nothing interesting here')


@route('/', method='POST')
def do_upload():
	params = request.forms
	for param in params:
		mylog(f"{param=} \t {params.get(param)=}")

	outdir = str(mkdir_today())
	files = request.files

	for one_file in files:
		file_uploaded = files[one_file]
		file_uploaded.save(outdir, overwrite=True)
		mylog("Saved", one_file.split('/')[-1])

	return {"count": len(files), "dir": outdir}


'''
Use lighttpd + flup

lighttpd.conf:
server.modules += ( "mod_fastcgi" )
fastcgi.server = (
	"/sensorium/" =>
	(
		(
			"host" => "127.0.0.1",
			"port" => 8080,
			"check-local" => "disable"
		)
	)
)
'''
run(server="flup", host='127.0.0.1', port=8080)
