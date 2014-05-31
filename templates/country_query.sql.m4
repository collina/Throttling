SELECT
        web100_log_entry.log_time,
        web100_log_entry.connection_spec.remote_ip,
        web100_log_entry.snap.HCThruOctetsAcked,
        web100_log_entry.snap.SndLimTimeRwin,
        web100_log_entry.snap.SndLimTimeCwnd,
        web100_log_entry.snap.SndLimTimeSnd,
        web100_log_entry.snap.MinRTT,
        web100_log_entry.snap.MaxRTT,
        web100_log_entry.snap.SumRTT,
        web100_log_entry.snap.CountRTT,
        web100_log_entry.snap.MaxMSS,
        web100_log_entry.snap.MaxPipeSize,
        web100_log_entry.snap.SegsRetrans,
        web100_log_entry.snap.SegsOut,
        web100_log_entry.snap.DataSegsOut,
        web100_log_entry.snap.CongSignals,
        web100_log_entry.snap.Timeouts,
        web100_log_entry.snap.DupAcksOut,
        web100_log_entry.snap.ECNsignals,
        web100_log_entry.snap.PreCongSumCwnd,
        web100_log_entry.snap.PreCongSumRTT,
        connection_spec.client_geolocation.country_code,
        connection_spec.server_geolocation.country_code
    FROM 
        DATETABLES
    WHERE
        IS_EXPLICITLY_DEFINED(project)
        AND project = 0
        AND IS_EXPLICITLY_DEFINED(connection_spec.data_direction)
        AND connection_spec.data_direction = 1
        AND IS_EXPLICITLY_DEFINED(web100_log_entry.is_last_entry)
        AND web100_log_entry.is_last_entry = True
        AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.HCThruOctetsAcked)
        AND web100_log_entry.snap.HCThruOctetsAcked >= 8192
        AND web100_log_entry.snap.HCThruOctetsAcked < 1000000000
        AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeRwin)
        AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeCwnd)
        AND IS_EXPLICITLY_DEFINED(web100_log_entry.snap.SndLimTimeSnd)
        AND (web100_log_entry.snap.SndLimTimeRwin +
        web100_log_entry.snap.SndLimTimeCwnd +
        web100_log_entry.snap.SndLimTimeSnd) >= 9000000
        AND (web100_log_entry.snap.SndLimTimeRwin +
        web100_log_entry.snap.SndLimTimeCwnd +
        web100_log_entry.snap.SndLimTimeSnd) < 3600000000
        AND IS_EXPLICITLY_DEFINED(web100_log_entry.log_time)
        AND IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.remote_ip)
        AND IS_EXPLICITLY_DEFINED(web100_log_entry.connection_spec.local_ip)
        AND connection_spec.client_geolocation.country_code = 'TARGET_COUNTRY';
