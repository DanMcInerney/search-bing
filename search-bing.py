#!/usr/bin/env python

#This must be one of the first imports or else we get threading error on completion
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent import joinall

import urllib
import urllib2
import argparse
import sys
import json

def parse_args():
   ''' Create the arguments '''
   parser = argparse.ArgumentParser()
   parser.add_argument("-s", "--search", help="Search terms")
   parser.add_argument("-l", "--limit", default="10", help="Limit number of results")
   return parser.parse_args()

def bing_search(query, limit, **kwargs):
    ''' Make the search '''
    username = ''
    key = 'YOUR KEY HERE'
    baseURL = 'https://api.datamarket.azure.com/Bing/SearchWeb/'
    limit = str(limit)
    query = urllib.quote(query)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = (':%s' % key).encode('base64')[:-1]
    auth = 'Basic %s' % credentials
    url = baseURL+'Web?Query=%27'+query+'%27&$top='+limit+'&$format=json'
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, username, key)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    readURL = urllib2.urlopen(url).read()
    return readURL

def action(result):
    ''' Perform this action on each result '''
    print result['Title'].ljust(60), result['Url']

def result_concurrency(results):
    ''' Do some current actions to the results '''
    in_parallel = 1000
    pool = Pool(in_parallel)
    jobs = [pool.spawn(action, result) for result in results]
    joinall(jobs)

def main():
    args = parse_args()
    if not args.search:
        sys.exit('[!] Specify a search term, eg, ./search-bing.py -s "search for this"')
    query = args.search
    limit = int(args.limit)
    response = bing_search(query, limit)
    results = json.loads(response)['d']['results']
    result_concurrency(results)
    #Raw print json.loads(response)['d']['results']
    #print 'Title and URL:'
    #for i in results:
    #    # Do something with each result
    #    print i['Title'], '--', i['Url']

if __name__ == "__main__":
    main()
