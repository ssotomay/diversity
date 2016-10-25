# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField
#from wtforms.validators import Required, Length
import random, json
import pandas as pd
import plotly
import plotly.graph_objs as go
#import Enrollment_Diveristy as ed

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap(app)


# The CS counts are real (counted them for each year), the others are randomly
# generated.



with open('diversity.json', 'r') as f:
     loaded_diversity = json.load(f)

# One can create more than one plot and store them in a list, which will be
# turned into JSON to be passed to the client.

def createData(dL,department,cl):
    a = []
    b = []
    l = []
    w =[]
    for d in dL:
        if d["Department"] == department and d["Course Level"] == cl:
            a.append(d["Vectors"][1])
            b.append(d["Vectors"][2])
            l.append(d["Vectors"][3])
            w.append(d["Vectors"][7])
    return a, b, l, w

def make_line_chart(choice,cl):
    test1 = list(createData(loaded_diversity,choice,cl))
    year = ["Fall 2011", "Spring 2012","Fall 2012", "Spring 2013","Fall 2013", "Spring 2014","Fall 2014", "Spring 2015"]
    # Create traces
    trace0 = go.Scatter(
        x = year,
        y = test1[0],
        mode = 'lines+markers',
        name = 'Asian'
    )
    trace1 = go.Scatter(
        x = year,
        y = test1[1],
        mode = 'lines+markers',
        name = 'Black'
    )
    trace2 = go.Scatter(
        x = year,
        y = test1[2],
        mode = 'lines+markers',
        name = 'Latina'
    )
    trace3 = go.Scatter(
        x = year,
        y = test1[3],
        mode = 'lines+markers',
        name = 'White'
    )
    data = [trace0, trace1, trace2, trace3]
    graphs = [dict(data=data)]
              # Convert the figures to JSON
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    print(graphJSON)
    return graphJSON


class ChoiceForm(Form):
    #name = StringField('What is your name?', validators=[Required(), Length(1, 16)])
    
    choice = SelectField(u'Departments', choices=[("blank", "Make a choice"), ('Africana Studies (AFR)', 'Africana Studies (AFR)'),
                                                 ('American Studies (AMST)', 'American Studies (AMST)'),
                                                 ('Anthropology (ANTH)', 'Anthropology (ANTH)'),
                                                 ('Art (ART)', 'Art (ART)'),
                                                 ('Astronomy (ASTR)', 'Astronomy (ASTR)'),
                                                 ('Biochemistry (BIOC)', 'Biochemistry (BIOC)'),
                                                 ('Biological Sciences (BISC)', 'Biological Sciences (BISC)'),
                                                 ('Chemistry (CHEM)', 'Chemistry (CHEM)'),
                                                 ('Cinema and Media Studies (CAMS)', 'Cinema and Media Studies (CAMS)'),
                                                 ('Classical Studies (CLST)', 'Classical Studies (CLST)'),
                                                 ('Cognitive and Linguistic Sci (CLSC)',
                                                  'Cognitive and Linguistic Sci (CLSC)'),
                                                 ('Comparative Literature (CPLT)', 'Comparative Literature (CPLT)'),
                                                 ('Computer Science (CS)', 'Computer Science (CS)'),
                                                 ('East Asian Languages and Cult (EALC)',
                                                  'East Asian Languages and Cult (EALC)'),
                                                 ('Economics (ECON)', 'Economics (ECON)'),
                                                 ('Education (EDUC)', 'Education (EDUC)'),
                                                 ('English (ENG)', 'English (ENG)'),
                                                 ('Environmental Sciences (ES)', 'Environmental Sciences (ES)'),
                                                 ('French (FREN)', 'French (FREN)'),
                                                 ('Geosciences (GEOS)', 'Geosciences (GEOS)'),
                                                 ('German (GER)', 'German (GER)'),
                                                 ('History (HIST)', 'History (HIST)'),
                                                 ('Humanities (HUM)', 'Humanities (HUM)'),
                                                 ('Italian Studies (ITST)', 'Italian Studies (ITST)'),
                                                 ('Jewish Studies (JWST)', 'Jewish Studies (JWST)'),
                                                 ('Mathematics (MATH)', 'Mathematics (MATH)'),
                                                 ('Medieval Renaissance Studies (ME/R)',
                                                  'Medieval Renaissance Studies (ME/R)'),
                                                 ('Middle Eastern Studies (MES)', 'Middle Eastern Studies (MES)'),
                                                 ('Music (MUS)', 'Music (MUS)'),
                                                 ('Neuroscience (NEUR)', 'Neuroscience (NEUR)'),
                                                 ('Peace and Justice Studies (PEAC)', 'Peace and Justice Studies (PEAC)'),
                                                 ('Philosophy (PHIL)', 'Philosophy (PHIL)'),
                                                 ('Physical Education (PE)', 'Physical Education (PE)'),
                                                 ('Physics (PHYS)', 'Physics (PHYS)'),
                                                 ('Political Science (POLS)', 'Political Science (POLS)'),
                                                 ('Psychology (PSYC)', 'Psychology (PSYC)'),
                                                 ('Quantitative Reasoning (QR)', 'Quantitative Reasoning (QR)'),
                                                 ('Religion (REL)', 'Religion (REL)'),
                                                 ('Russian (RUSS)', 'Russian (RUSS)'),
                                                 ('Russian Area Studies (RAST)', 'Russian Area Studies (RAST)'),
                                                 ('Sociology (SOC)', 'Sociology (SOC)'),
                                                 ('South Asia Studies (SAS)', 'South Asia Studies (SAS)'),
                                                 ('Spanish (SPAN)', 'Spanish (SPAN)'),
                                                 ('Sustainability (SUST)', 'Sustainability (SUST)'),
                                                 ('Theatre Studies (THST)', 'Theatre Studies (THST)'),
                                                 ("Women's and Gender Studies (WGST)", "Women's and Gender Studies (WGST)"),
                                                 ('Writing (WRIT)', 'Writing (WRIT)')])

    cl = SelectField(u'Course Level', choices=[("blank", "Make a choice"), ('100 Level', '100 Level'),
                                                 ('200 Level', '200 Level'),
                                                 ('300 Level', '300 Level')])

    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    
    choice = None
    cl = None
    ids = []
    graphJSON = []
    #ruhlman_data = pd.read_excel('test.xlsx')
    form = ChoiceForm()
    if form.validate_on_submit():
        choice = form.choice.data
        cl = form.cl.data
        if choice != "blank" and cl != "blank":
            graphJSON = make_line_chart(choice,cl)
            ids = ["Line Chart for {}".format(choice)]
        form.choice.data = ''
    return render_template('index.html', form=form, choice=choice,
                           graphJSON=graphJSON,
                           ids=ids) #data = ruhlman_data.to_html())


if __name__ == '__main__':
    #app.run(debug=True, port = 7000)
    app.run(host='0.0.0.0', port = 1561, debug=True)