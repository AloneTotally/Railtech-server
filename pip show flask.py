from flask import Flask, Response
import time

app = Flask(__name__)

@app.route('/events')
def events():
    def generate_events():
        while True:
            time.sleep(1)  # Simulate delay
            yield f"data: The current time is {time.ctime()}\n\n"
    
    return Response(generate_events(), mimetype='text/event-stream')



@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <head>
        <title>SSE Example</title>
        <script>
            const evtSource = new EventSource('/events');
            evtSource.onmessage = function(event) {
                const newElement = document.createElement("div");
                newElement.innerHTML = event.data;
                document.body.appendChild(newElement);
            };
        </script>
    </head>
    <body>
        <h1>Server-Sent Events Example</h1>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
