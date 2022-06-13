import plotly.express as px

from data import data

fig = px.imshow(data['1'][[x for x in data['1'].keys()][0]][0])
line_fig = px.scatter()
