import dolibarrpy
from icecream import install
install()

my_url   = "insert link to your Dolibarr API here"
my_token = "insert your Dolibarr API token here"

mine = dolibarrpy.Dolibarrpy(url=my_url, token=my_token, timeout=88, debug=True)

def recursive_pop_none_and_variable(dirty_data, also_pop = [None]):
    kender_du = type(dirty_data)
    if list == kender_du:
        cleaner_data = []
        for L in dirty_data:
            if L is None:
                continue
            elif L == also_pop:
                continue
            else:
                for KEY in also_pop:
                    if L == KEY:
                        continue
                new_data = recursive_pop_none_and_variable(L,also_pop)
                cleaner_data.append(new_data)
    elif dict == kender_du:
        cleaner_data = {}
        for D in dirty_data.keys():
            V = dirty_data[D]
            if V is None:
                continue
            elif V == []:
                continue
            elif V== "":
                continue
            elif V == also_pop:
                continue
            elif D == also_pop:
                continue
            else:
                for KEY in also_pop:
                    if D == KEY:
                        continue
                    if V == KEY:
                        continue
                    new_V = recursive_pop_none_and_variable(V,also_pop)
                cleaner_data[D] = new_V
    else:
        return dirty_data

    return cleaner_data

result = mine.find_all_contacts()
ic(len(result))
ic(len(recursive_pop_none_and_variable(result)))
ic(recursive_pop_none_and_variable(result))