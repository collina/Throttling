import matplotlib.pyplot
import matplotlib.ticker, matplotlib.dates
import datetime

def graph(trends, outfile = None, aggregation_type = 'median', graph_type = 'plot', start = None, end = None, events = None):

    colors = {
                'median-line': '#785D89',
                'median-below': '#C6A8DB',
                'throttled-below': '#FFDE8C',
             }
    x_values = sorted(trends.keys())
    y_values = [trends[date_key][aggregation_type] for date_key in x_values]
    
    x_size = len(x_values) * .1
    
    matplotlib.pyplot.clf()
    matplotlib.pyplot.figure(figsize=(x_size, 4), dpi=80)
    
    matplotlib.pyplot.title("Throughput between %s and %s" % (x_values[0].strftime('%Y-%m-%d'), x_values[-1].strftime('%Y-%m-%d')))

    if graph_type == 'plot':
        matplotlib.pyplot.plot(x_values, y_values, color = colors['median-line'], label = aggregation_type) #, label = 'media %s' % state, linewidth = 3)
        matplotlib.pyplot.fill_between(x_values, y_values, 0, color=colors['median-below'])
        
    elif graph_type == 'scatter':
        all_values = [(date_key, measurement[1]) for date_key in x_values for measurement in trends[date_key][aggregation_type] ]
        print all_values
        matplotlib.pyplot.scatter([value[0] for value in all_values], [value[1] for value in all_values]) #, color = colors['median-line']) #, label = 'media %s' % state, linewidth = 3)

    if events is not None:
        for (before_event, after_event) in events:
            x_values_throttled = sorted([date_key for date_key in trends.keys() if date_key > before_event and date_key < after_event])
            y_values_throttled = [trends[date_key][aggregation_type] for date_key in x_values_throttled]
            matplotlib.pyplot.fill_between(x_values_throttled, y_values_throttled, 0, color=colors['throttled-below'])

    axis = matplotlib.pyplot.gca()
    axis.set_xlim([x_values[0], x_values[-1]])
#    axis.set_ylim([0, .12])
    axis.xaxis.set_major_locator(matplotlib.dates.MonthLocator(bymonth = range(1,13), bymonthday = 1, interval = 1))
    axis.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%B %Y"))
    
    axis.xaxis.set_minor_locator(matplotlib.dates.WeekdayLocator(byweekday=matplotlib.dates.SA))
    
    matplotlib.pyplot.minorticks_on()
    matplotlib.pyplot.legend()
    
    matplotlib.pyplot.savefig(outfile, bbox_inches='tight')
    matplotlib.pyplot.close('all')
