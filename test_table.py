import pandas as pd
from selenium import webdriver

from operator import itemgetter
from natsort import natsorted


goal_url = 'https://en.wikipedia.org/wiki/List_of_tallest_buildings'
driver = webdriver.Chrome()
driver.get(goal_url)

#function to get the table from wiki page
def get_table():

    html = driver.page_source
    dfs = pd.read_html(html)
    # Select the second table
    df = dfs[2]
    data = []
    for i in range(0, 74):
        #add data from the folowing colums: Rank, Name, City, Country, Height m, Height ft, Floors, Year
        data.append([df.iloc[i][0], df.iloc[i][1], df.iloc[i][3], df.iloc[i][4], df.iloc[i][5], df.iloc[i][6], df.iloc[i][7], df.iloc[i][8]])
    return data
# get the original table from the wiki page for the future use
original_table = get_table()

def test_sorting_by_rank():
    #make two clicks on Rank column, two clicks needed because the first click activates the descending order, which is displayed by default
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/thead/tr[1]/th[1]').click()
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/thead/tr[1]/th[1]').click()
    sorted_table_by_rank = get_table()
    '''
    As the element being sorted is a list of lists ([[40, "23 Marina", "Dubai"], [43, "30 Hudson", "NYC"], etc]) we sort 
    it by the key equal to the second element in every nested list.
    '''
    assert sorted_table_by_rank == sorted(original_table, key=itemgetter(0), reverse=True)
    print("Sorting by rank: pass")


def test_sorting_by_name():
    #only one click needed, as by default the table is sorted by rank
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/thead/tr[1]/th[2]').click()
    sorted_table_by_name = get_table()
    #Using natural sorting in the next assert to avoid problems with elements containing strings and ints.
    assert sorted_table_by_name[0][0] == natsorted(original_table, key=itemgetter(1), reverse=False)[0][0]
    print("Sorting by name: pass")

def test_buildings_max_count():
    countries_list = [element[3] for element in original_table]
    country_max_count = max(countries_list, key=countries_list.count)
    assert country_max_count == "China"
    print(f"Checked if {country_max_count} is the county with maximum number of buildings: pass")

def test_oldest_building():
    #select all the years from the original table
    years_list = [element[7] for element in original_table]
    #select the name of the building with the oldest date
    for element in original_table:
        if element[7] == min(years_list):
            oldest_building = element[1]
    assert oldest_building == "Empire State Building"
    print(f"Checked if {oldest_building} is the oldest building: pass")


#test_sorting_by_rank()
#test_sorting_by_name()
#test_buildings_max_count()
#test_oldest_building()
#driver.close()

'''
The test suite fails if started via 'pytest test_table.py' with the webdriver uncommented at the end. It is working ok 
if you run it as 'python test_table.py' (all the commands at the end must be uncommented). I also tried to make a proper
setup/teardown invoking and closing the webdriver, but for some reason the test_suit fails with them too. The webdriver 
is started and closed as expected, but it seems that the teardown starts before the selenium can click and
get the content. Even with implicit waits. 
I haven't yet found the solution, so could you please give me a hint along with the feedback?
'''





