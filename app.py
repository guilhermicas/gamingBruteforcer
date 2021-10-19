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
        print(e)


def main(argv):
    url = argv.u
    wordlist_path = argv.w

    # Verify if the the word GAMING is on URL word bruteforce location
    if ("GAMING" not in url):
        return print("The word GAMING was not found on the url")

    # Grab the wordlist
    if not os.path.isfile(wordlist_path):
        print('Path is not valid.')
    else:
        wordlist = []

        with open(wordlist_path, "r") as file:
            wordlist = file.read().split("\n")[:-1]

        # Multithread bruteforce
        thread_list = []

        for word in wordlist:
            request_url = url.replace("GAMING", word)

            thread = threading.Thread(
                target=httpRequest, args=(request_url,))

            thread_list.append(thread)

            if(len(thread_list) == 100):
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
    argv = parser.parse_args()

    main(argv)
