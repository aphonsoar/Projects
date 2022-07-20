## Sankey Diagram in Python (examples)
# https://plotly.com/python/sankey-diagram/
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

fig = go.Figure(data=[go.Sankey(node = dict(pad = 15,
                                            thickness = 20,
                                            line = dict(color = "black", width = 0.5),
                                            label = ["A1", "A2", "B1", "B2"],
                                            color = "red"),

                                link = dict(source = [0, 1, 0, 2, 2, 2], # indices correspond to labels, eg A1, A2, A1, B1, ...
                                            target = [2, 3, 3, 3, 3, 3],
                                            value = [8, 3, 2, 4, 2, 2]))])

fig.update_layout(title_text="Basic Sankey Diagram",
                  font_size=10,
                  width=1500, height=700)
fig.show()



#%%
import plotly.graph_objects as go
import urllib, json

url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
response = urllib.request.urlopen(url)
data = json.loads(response.read())

# override gray link colors with 'source' colors
opacity = 0.4
# change 'magenta' to its 'rgba' value to add opacity
data['data'][0]['node']['color'] = ['rgba(255,0,255, 0.8)' if color == "magenta" else color for color in data['data'][0]['node']['color']]
data['data'][0]['link']['color'] = [data['data'][0]['node']['color'][src].replace("0.8", str(opacity))
                                    for src in data['data'][0]['link']['source']]

fig = go.Figure(data=[go.Sankey(
    valueformat = ".0f",
    valuesuffix = "TWh",
    # Define nodes
    node = dict(
      pad = 15,
      thickness = 15,
      line = dict(color = "black", width = 0.5),
      label =  data['data'][0]['node']['label'],
      color =  data['data'][0]['node']['color']
    ),
    # Add links
    link = dict(
      source =  data['data'][0]['link']['source'],
      target =  data['data'][0]['link']['target'],
      value =  data['data'][0]['link']['value'],
      label =  data['data'][0]['link']['label'],
      color =  data['data'][0]['link']['color']
))])

fig.update_layout(title_text="Energy forecast for 2050<br>Source: Department of Energy & Climate Change, Tom Counsell via <a href='https://bost.ocks.org/mike/sankey/'>Mike Bostock</a>",
                  font_size=10)
fig.show()