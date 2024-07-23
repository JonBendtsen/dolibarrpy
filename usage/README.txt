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


Still somewhat simple usage:

run python3 simple_usage_empty_contact_searchfilter.py and you'll get all your contacts.
At the time of writing this I have 450 contacts spread over 231 Thirdparties.
The file first_94_lines_from_all_contacts.txt only shows the first 94 lines of running
the above. The private data are removed due to GDPR, but they would come from line 95
and onwards.

If you study the file first_94_lines_from_all_contacts.txt you can see it connects 6 times
to my Dolibarr installation, and only in the last, the 6. connection it gets a 404 answer.
This is because there are no more contacts.

In all the other cases it gets 100, 100, 100, 100 and 50. Why? Because Dolibarr's default
limit is 100. This is even though my limit is set to None. Perhaps I should set it to 100
as the default value just like Dolibarr?




Medium usage - let's introduce a filter that only fetches contacts with firstname jon:

run python3 medium_usage_defined_contact_searchfilter.py and I only get 3 contacts, you might
get a different number. The output - except for private data is in this file contacts_firstname_jon.txt

Viewing that file you see it only makes 2 connections, because that is all what is needed to get
all the contacts with a firstname like jon.

if you diff simple_usage_empty_contact_searchfilter.py medium_usage_defined_contact_searchfilter.py
you should easily see the difference in how to use the filter.

How did I get that dataclass information? Well I partly used the information at Dolibarrs API explorer
to know what could be filtered, but it might just be easier to copy the filter definition from
../dolibarrpy/Dolibarrpy.py


If you want to use filters maybe first get the filter working using Dolibarrs API explorer,
and then you can implement the same filter when using dolibarrpy


Debugging example:

If you set debug to False in line 8 of simple_usage_empty_contact_searchfilter.py

    mine = dolibarrpy.Dolibarrpy(url=my_url, token=my_token, timeout=88, debug=False)

then you would only get data output, not all the debug information.
