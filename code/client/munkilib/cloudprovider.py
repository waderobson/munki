#!/usr/bin/python

import os
import subprocess
import munkicommon
import fetch

def process_options(options, cloud_provider):
    """recieves options dictionary before gurl gets it.
    Uses the URL key as argment to a user specified executable/script.
    To use this function you need to have except 2 arguments.

    /path/to/cloud_provider [arg1] [arg2]
    arg1: the URL
    arg2: is either 'headers' or 'query_parameters'
    When 'headers' is called:
        The script must return 1 header per line to stdout
    When 'query_parameters' is called:
        The script must return the entire query portion of
        the URL on one line."""
    executable_path = cloud_provider
    if os.path.exists(executable_path):
        if os.access(executable_path, os.X_OK):
            for api_type in ['headers', 'query_parameters']:
                cmd = [executable_path, options['url'], api_type]
                proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                if api_type == 'headers':
                    headers = []
                    while True:
                        line = proc.stdout.readline()
                        if line != '':
                            headers.append(line.rstrip('\n'))
                        else:
                            break
                if api_type == 'query_parameters':
                    query_parameters = proc.stdout.readline()
        else:
            munkicommon.display_warning('%s not executable',
                                        executable_path)
    else:
        munkicommon.display_warning('CloudProvider not at path %s',
                                    executable_path)
    cloud_headers = fetch.header_dict_from_list(headers)
    url_with_query = options['url'] + query_parameters.rstrip('\n')
    options['url'] = url_with_query
    options['additional_headers'].update(cloud_headers)
    return options