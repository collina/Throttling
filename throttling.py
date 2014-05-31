import argparse
import datetime
import csv

import throttling

def built_dataset_from_csv(csv_file):
    '''
        Processing outside of main function in order to provide room to do modifications if needed.
    '''
    list_of_dicts_to_return = []
    
    for dataset_dict in csv.DictReader(csv_file):
        list_of_dicts_to_return.append(dataset_dict)
    
    return list_of_dicts_to_return

def main(args):

    if args.infiles:
        dataset = []
        
        for infile in args.infiles:
            dataset += built_dataset_from_csv(infile)

    if len(dataset) > 0:
        performance_trends = throttling.compile(dataset)
        
        throttling_events = [(datetime.datetime.strptime('2013-05-21', '%Y-%m-%d'), datetime.datetime.strptime('2013-06-14', '%Y-%m-%d'))]
        throttling.graph(performance_trends['download_throughput'], '/tmp/trends.png', aggregation_type = 'median', graph_type = 'plot', events = throttling_events)
#        throttling.graph(performance_trends['min_rtt'], '/tmp/trends.png', aggregation_type = 'median', graph_type = 'plot')
#        throttling.graph(performance_trends['download_throughput'], '/tmp/trends.png', aggregation_type = 'raw', graph_type = 'scatter')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Select RIPE Atlas probes.")
    parser.add_argument('infiles', nargs="+", type=argparse.FileType('r'), default=None)
    
    args = parser.parse_args()
    
    exit(main(args))
