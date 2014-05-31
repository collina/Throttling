import datetime
import numpy

def compile(dataset):
    '''
        dataset: list of NDT M-Lab entries as dicts, typically consisting of keys:
            [
                "connection_spec_server_geolocation_country_code",
                "web100_log_entry_snap_SumRTT",
                "web100_log_entry_snap_DataSegsOut",
                "web100_log_entry_snap_DupAcksOut",
                "web100_log_entry_snap_MinRTT",
                "web100_log_entry_snap_PreCongSumCwnd",
                "web100_log_entry_snap_MaxRTT",
                "web100_log_entry_snap_SndLimTimeSnd",
                "web100_log_entry_snap_CongSignals",
                "web100_log_entry_snap_CountRTT",
                "web100_log_entry_snap_SegsOut",
                "web100_log_entry_snap_MaxPipeSize",
                "web100_log_entry_log_time",
                "web100_log_entry_snap_MaxMSS",
                "web100_log_entry_snap_HCThruOctetsAcked",
                "web100_log_entry_snap_PreCongSumRTT",
                "web100_log_entry_snap_SndLimTimeCwnd",
                "web100_log_entry_connection_spec_remote_ip",
                "web100_log_entry_snap_SegsRetrans",
                "web100_log_entry_snap_Timeouts",
                "web100_log_entry_snap_SndLimTimeSnd",
                "web100_log_entry_snap_ECNsignals",
                "connection_spec_client_geolocation_country_code"
            ]

    '''
    compiled_dataset_to_return = { "download_throughput": {}, "min_rtt": {} }
    
    for row_number, record in enumerate(dataset):

        if record['web100_log_entry_snap_CongSignals'] > 1:
            record_datetime = datetime.datetime.fromtimestamp(int(record['web100_log_entry_log_time']))
            record_key = record_datetime - datetime.timedelta(hours = record_datetime.hour, minutes = record_datetime.minute, seconds = record_datetime.second)
            
            if (not compiled_dataset_to_return["download_throughput"].has_key(record_key)):
                compiled_dataset_to_return["download_throughput"][record_key] = {'raw': [], 'median': None, 'variance': None}
            compiled_dataset_to_return["download_throughput"][record_key]['raw'].append( (record['web100_log_entry_connection_spec_remote_ip'], calculate_download_throughput(record)) )

            if (not compiled_dataset_to_return["min_rtt"].has_key(record_key)):
                compiled_dataset_to_return["min_rtt"][record_key] = {'raw': [], 'median': None}
            compiled_dataset_to_return["min_rtt"][record_key]['raw'].append( (record['web100_log_entry_connection_spec_remote_ip'], calculate_min_rtt(record)) )

    for measurement_type, period_records in compiled_dataset_to_return.iteritems():
        for date_key, date_records in period_records.iteritems():
            if measurement_type == 'download_throughput':
                compiled_dataset_to_return[measurement_type][date_key]['median'] = derive_download_throughput_day(date_records['raw'])
                compiled_dataset_to_return[measurement_type][date_key]['variance'] = derive_download_throughput_day(date_records['raw'], type = 'variance')
            if measurement_type == 'min_rtt':
                compiled_dataset_to_return[measurement_type][date_key]['median'] = derive_download_min_rtt_day(date_records['raw'])
                compiled_dataset_to_return[measurement_type][date_key]['variance'] = derive_download_min_rtt_day(date_records['raw'], type = 'variance')
    return compiled_dataset_to_return


def calculate_download_throughput(record):
    '''
        Download Throughput:
            web100_log_entry_snap_HCThruOctetsAcked / (web100_log_entry_snap_SndLimTimeCwnd + web100_log_entry_snap_SndLimTimeSnd + web100_log_entry_snap_SndLimTimeSnd)
    '''
    return float(record['web100_log_entry_snap_HCThruOctetsAcked']) / (float(record['web100_log_entry_snap_SndLimTimeCwnd']) + float(record['web100_log_entry_snap_SndLimTimeSnd']) + float(record['web100_log_entry_snap_SndLimTimeSnd']))
def calculate_min_rtt(record):
    '''
        Minimum Round Trip Time:
            web100_log_entry_snap_MinRTT
        '''
    return float(record['web100_log_entry_snap_MinRTT'])

def derive_download_throughput_day(date_records, type = 'median'):
    client_measurements = {}
    
    for (address, measurement) in date_records:
        if (not client_measurements.has_key(address)):
            client_measurements[address] = []
        client_measurements[address].append(measurement)

    if type == 'median':
        return numpy.median([numpy.amax(measurements) for measurements in client_measurements.values()])
    elif type == 'variance':
        return numpy.std([numpy.amax(measurements) for measurements in client_measurements.values()])

    return None

def derive_download_min_rtt_day(date_records, type = 'median'):
    client_measurements = {}
    
    for (address, measurement) in date_records:
        if (not client_measurements.has_key(address)):
            client_measurements[address] = []
        client_measurements[address].append(measurement)
    
    if type == 'median':
        return numpy.median([numpy.amax(measurements) for measurements in client_measurements.values()])
    elif type == 'variance':
        return numpy.std([numpy.amax(measurements) for measurements in client_measurements.values()])
    
    return None