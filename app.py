#!/bin/python3

import os
import threading
import requests
import argparse

"""
The options should be:
    - url to target the bruteforce
    - wordlist to use on bruteforce
"""


def httpRequest(url: str):
    try:
        req = requests.get(url=url)
        if req.status_code in [200, 204, 301, 302, 307, 401, 403, 405]:
            print(f"[{req.status_code}] Valid url: {url}")

    except Exception as e:
        print(f"[REQUEST EXCEPTION] ")


def main(argv):
    url = argv.u
    wordlist_path = argv.w

    # argv.t is number of threads given by user, default being 100
    max_concurrent_threads = 100 if str(
        type(argv.t)) == "<class 'NoneType'>" else int(argv.t)

    # Verify if the the word GAMING is on URL word bruteforce location
    if ("GAMING" not in url):
        return print("The word GAMING was not found on the url")

    # Grab the wordlist
    if not os.path.isfile(wordlist_path):
        return print('Path is not valid.')
    else:
        wordlist = []

        with open(wordlist_path, "r") as file:
            wordlist = file.read().split("\n")[:-1]

        thread_list = []
        print(f"Using {max_concurrent_threads} threads")

        for word in wordlist:
            request_url = url.replace("GAMING", word)

            # Multithread bruteforce
            thread = threading.Thread(
                target=httpRequest, args=(request_url,))

            # If the main thread dies, this thread will be die as well.
            thread.daemon = True

            thread_list.append(thread)

            # When thread list size reaches a limit, execute all threads and wait for finish
            if(len(thread_list) == max_concurrent_threads):
                for t in thread_list:
                    t.start()

                for t in thread_list:
                    t.join()

                thread_list = []


if __name__ == "__main__":
    print("Brute forces url with wordlist. will match by default with status codes 200,204,301,302,307,401,403,405.")
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="URL of target", required=True)
    parser.add_argument("-w", help="Wordlist", required=True)
    parser.add_argument("-t", help="Number of Threads to use (default 100)")
    argv = parser.parse_args()

    main(argv)
