from celery import Celery
from celery import chord
from celery import chain
import urllib
import subprocess as sp
from time import sleep
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

@app.task(bind=True)
def LotsOfDivisionTask(self,numbers):
    numerators = numbers[0]
    denominators = numbers[1]

    results = []
    divisions_to_do = len(numerators)
    # Only actually update the progress in the backend every 10 operations
    update_frequency = 10
    for count, divisors in enumerate(zip(numerators, denominators)):
        numerator, denominator = divisors
        results.append(numerator / denominator)
        # Let's let everyone know how we're doing
        self.update_state(state='PROGRESS',
                      meta={'current': count, 'total': divisions_to_do,
                            'status': 'In progress'})
        # Let's pretend that we're using the computers that landed us on the moon
        sleep(0.1)

    return results