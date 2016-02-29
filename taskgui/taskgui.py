from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET','POST'])
def index():
  message = None
  if request.method == 'POST':
    #Button was clicked, so kick of workers  
    message = 'Button clicked'
    from bctasks import dispatch
    files = [
              {'name': 'files/cm3.mp4', 'url': 'http://www.caminandes.com/download/03_caminandes_llamigos_1080p.mp4'},
	      {'name': 'files/cm2.mp4', 'url': 'http://www.chrisandweeze.com/02_gran_dillama_1080p.mp4'}
            ]
    dispatch.delay(files)
  return render_template('index.html', message=message)


app.secret_key = 'Dnt8&&/M7?ndikTB122'
if __name__ == '__main__':
    if __package__ is None:
        print 'here'
        import sys
        from os import path
        print path.dirname( path.dirname( path.abspath(__file__) ) )
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    app.run(host='0.0.0.0', debug=True)
