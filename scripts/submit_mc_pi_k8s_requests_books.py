#!/usr/bin/env python3

"""
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from multiprocessing import Pool
import requests
import time
import json
import argparse
from functools import reduce
from tqdm import tqdm
import sys

url = 'http://<external_ip>:8983/solr/employee/select?q=*'

def getUrl(url):
    try:
        url = 'http://<external_ip>:8983/solr/employee/select?q=*'
        return requests.get(url,timeout=30)
    except Exception as e:
        pass
        #print("Ouch, I'm getting timeouts !!!! ")

def runParallelRequests(processes=10, queued_requests_per_process=10,url="",iterations=10000000):
    the_url = url + "/?iterations=" + str(iterations)
    queue_of_urls = [ the_url for x in range(processes * queued_requests_per_process) ]
    print("Total processes: {}\nLen of queue_of_urls: {}\ncontent of queue_of_urls: {}".format(
        processes,
        len(queue_of_urls), 
        queue_of_urls[0]))
    pool = Pool(processes)
    try:
        results = []
        for res in tqdm(pool.imap_unordered(getUrl, queue_of_urls), total=len(queue_of_urls)):
            print(res.content)
            results.append(res)
    finally:
        pool.close()
        pool.join()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--processes',dest='processes',type=int,default=10, help="Number of parallel processes to use as clients")
    parser.add_argument('-r','--requests',dest='req',type=int,default=10, help="Number of requests each client process will run")
    parser.add_argument('-u','--url',dest='url',type=str, default=url, help="URL that will be used to do the GET request")
    parser.add_argument('-i','--iterations', dest='iterations', default=10000000, help="Number of Search Query")
    args = parser.parse_args()
   
    runParallelRequests(
        processes=args.processes,
        queued_requests_per_process=args.req,
        url=args.url,
        iterations=args.iterations
    )


if __name__ == "__main__":
    main()

