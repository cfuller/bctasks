from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify

app = Flask(__name__)
app.config.from_object('flaskconfig')

@app.route('/', methods=['GET','POST'])
def index():
  message = None
  if request.method == 'POST':
    message = 'Button clicked'
    from bctasks import dispatch
    files = [
        {'name': 'files/cm3.mp4', 'url': 'http://www.caminandes.com/download/03_caminandes_llamigos_1080p.mp4'},
        {'name': 'files/cm2.mp4', 'url': 'http://www.chrisandweeze.com/02_gran_dillama_1080p.mp4'}
    ]
    dispatch.delay(files)
  return render_template('index.html', message=message)

@app.route('/delete-masters', methods=['GET'])
def deleteMasters():
    return render_template('deleteMasters.html')

@app.route('/longtask', methods=['POST'])
def longtask():
    from bctasks import LotsOfDivisionTask
    iterations = 100
    step = 10
    numerators=range(0, step * iterations * 2, step * 2)
    denominators=range(1, step * iterations, step)

    numbers = []
    numbers.append(numerators)
    numbers.append(denominators)

    task = LotsOfDivisionTask.delay(numbers)
    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}

@app.route('/status/<task_id>')
def taskstatus(task_id):
    from bctasks import LotsOfDivisionTask
    task = LotsOfDivisionTask.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': 'Complete'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        print path.dirname( path.dirname( path.abspath(__file__) ) )
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
    app.run(host='0.0.0.0', debug=True)
