"""
    Utilities for making matplotlib less verbose in the backend
    and less ugly in the frontend. Also Plotly interops.
"""
 
import matplotlib.pyplot as plt 
plt.style.use('ggplot')
 
 
#  Remove frame, space out the axis labels.
def remove_frame() :
    ax = plt.subplot(111)   
    for point in ["top", "bottom", "left", "right"] :   
        ax.spines[point].set_visible(False)
    
    ax.get_xaxis().tick_bottom()   
    ax.get_yaxis().tick_left()   
    ax.xaxis.labelpad = 20
    ax.yaxis.labelpad = 20
   
    return ax
   
 
#  Limit the chart where the data is.   
def clip_axes( minX, maxX, minY, maxY ) :
    plt.ylim(minY, maxY)   
    plt.xlim(minX, maxX)   
 
 
 
#  'axis' as in `untick_last_n (2, ax.xaxis)`
def untick_last_n (n, axis):
    ticks = axis.get_major_ticks()
   
    for i in range( 1, n+1 ) :
        ticks[-i].label1.set_visible(False)
 
 
def ticks_off() :
    plt.tick_params(axis="both", which="both", bottom="off", top="off",
                    labelbottom="on", left="off", right="off", labelleft="on")   
  
 
def add_footnotes(x_pos, y_pos, footnotes) :
    if isinstance(footnotes, str):
        footnotes = [footnotes]
    plt.text(x_pos, y_pos, "\n".join(footnotes), fontsize=10)  
 
 
 
#  'axis' as in `hide_half_ticks(ax.yaxis)`
def hide_half_ticks (axis) :
    for tick in axis.get_ticklabels()[::2] :
        tick.set_visible(False)
      
 
# Convert matplotlib plot to offline plotly plot.
def to_interactive(fig, buttonsToRemove) :
    import plotly.offline as ploff
    import plotly.tools as tls
    import webbrowser
    
    plotly_fig = tls.mpl_to_plotly(fig)
    path = ploff.plot(plotly_fig, show_link=False, auto_open=False)
    cleanPath = path[7:]
    hack_js(cleanPath, buttonsToRemove)
    webbrowser.open(cleanPath)
 
 
# Edit the Plotly modebar while Python lacks the API.
# from here: http://stackoverflow.com/a/36610966/5608164
def hack_js (htmlPath, removes):
    with open(htmlPath, 'r') as file :
        temp = file.read()
 
        temp = temp.replace('displaylogo:!0', 'displaylogo:!1')
        temp = temp.replace('modeBarButtonsToRemove:[]', 'modeBarButtonsToRemove: '+ str(removes) )
    with open(htmlPath, 'w') as file:
        file.write(temp)
    del temp
 
 
#%%

#  e.g. World population projection
"""   
import pandas as pd
year = pd.Series([ 1950, 1970 , 1990, 2010 ])
population = pd.Series([ 2.519, 3.692, 5.263, 6.972 ])
df = pd.concat([year, population], axis=1)
df.columns = [ "year", "population" ]
 
fig = plt.figure()   
ax = remove_frame()
ticks_off()
hide_half_ticks(ax.yaxis)
 
 
x = df.year
y = df.population
plt.plot(x.values, y.values, lw=2.5, label="billion people") 
 
# Add a bad prediction line
from sklearn import linear_model
reg = linear_model.LinearRegression(fit_intercept=True)
predictor = df.year.reshape(-1, 1)
reg.fit( predictor, df.population )                                   # Train
x = [ i for i in range(2010, 2110, 10) ]
yhat = [ reg.predict(i) for i in x ]
 
clip_axes( year.min(), max(x), 0, max(yhat)+4 )
ax.yaxis.get_ticklabels()[-3].set_visible(True)
plt.plot(x, yhat, color='blue', linestyle='dashed', label="bad prediction")
plt.show()
 
 
buttonsToRemove = ["sendDataToCloud", "zoom2d", "pan2d", "toggleSpikelines", "autoScale2d" ]
to_interactive( fig, buttonsToRemove )
"""