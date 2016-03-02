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
def stitch(pathList):
  f = open('files/filelist.txt', 'w')
  for path in pathList:
    path = path.replace('files/', '')
    f.write('file ' + path + "\n")
 
  command = [FFMPEG_BIN,
             '-f', 'concat',
             '-i', 'files/filelist.txt',
             '-c', 'copy',
	     'files/stitched.mp4']
  try:
    out = sp.check_output(command, shell=True, stderr=sp.STDOUT)
    print out
    return out.output
  except sp.CalledProcessError as er:
    print er.output
    return er.output

@app.task
def dispatch(files):
   chord(download.s(f['url'], f['name']) for f in files)(stitch.s())
