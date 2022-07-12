import plotly.express as px
import plotly.graph_objects as go

main_fig = go.Figure()

line_fig = px.scatter()
line_fig.update_xaxes(autorange='reversed')

hist_fig = px.histogram()
