from datetime import date
from flask import Flask
from flask import render_template
import metrics


app = Flask(__name__)

@app.route('/')
def index():
    project_type = 'tc-approved-release'

    d1 = date.today()
    d2 = date(2016,2,29)
    weeks = abs(d2-d1).days / 7

    rank,  projects = metrics.load_project_data(metrics.release, metrics.company, project_type)
    return  render_template('show_data.html', company=metrics.company, project_type=project_type, rank=rank, projects=projects,
                            weeks=weeks, release=metrics.release)

if __name__ == '__main__':
     app.run(port=5001, debug=True)
