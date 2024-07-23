Here is how you get started using Dolibarrpy.

1. pip3 install dolibarrpy
2. pip3 install icecream
3. edit simple_usage_get_status.py and insert:
    a. the URL to your Dolibarr API
    b. the TOKEN for your Dolibarr API user
4. python3 simple_usage_get_status.py

You should now get a successful response to STDOUT and see which version of Dolibarr you run.


Once you have done a pip3 install dolibarrpy it is super easy to use dolibarrpy:

10. import dolibarrpy
11. define my_url
12. define my_token
13. Do something like:
    mine=dolibarrpy.Dolibarrpy(url=my_url, token=my_token, timeout=88, debug=True)
14. Call API endpoints by using the functions inside Dolibarrpy:
    result = mine.get_status()

