from celery import Celery
from celery import chord
from celery import chain
import urllib
import subprocess as sp
FFMPEG_BIN = "/usr/bin/ffmpeg"

app = Celery('bctasks')
app.config_from_object('celeryconfig')

@app.task
def download(url, name):
    urllib.urlretrieve(url, name)
    return name

@app.task
def writePaths(pathList):
  f = open('files/filelist.txt', 'w')
  print f
  for path in pathList:
    f.write('file ' + path + "\n")
  return 'files/filelist.txt'

@app.task
def dispatch(files):
   chain(chord(download.s(f['url'], f['name']) for f in files)(writePaths.s()), stitch.s())

@app.task
def stitch(input):
  print input
  command = [FFMPEG_BIN,
             '-f', 'concat',
             '-i', str(input),
             '-c', 'copy',
	     'output', 'files/stitched.mp4']
  sp.call(command)
