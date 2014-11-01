# from lxml import etree
from lxml.html import parse
shelf_to_read = 'http://www.goodreads.com/review/list/20186983?shelf=to-read&per_page=40'
shelf_computers = 'http://www.goodreads.com/review/list/20186983-anna?shelf=computers&per_page=40'
to_read = parse(shelf_to_read).getroot()
computers = parse(shelf_computers).getroot()


# get number of webpages pages to iterate
def get_num_webpages(root):
    x_num_books = root.xpath('//div[@id="header"]//span[@class="greyText"]')
    num_books = x_num_books[0].text.strip('()')
    num_books = int(num_books)
    if num_books % 40 == 0:
        webpages = num_books / 40
    else:
        webpages = int(num_books / 40) + 1
    return webpages

webpages_toread = get_num_webpages(to_read)
webpages_comp = get_num_webpages(computers)


# for debugging
def printelems(_list):
    for elem in _list:
        print elem
        

# trim whitespace & \n
def append_text(x_list, _list):
    for elem in x_list:
        elem_text = elem.text.strip()
        _list.append(elem_text)
        elem.clear()
        

# from to-read
titles = []
authors = []
links = []

for n in range(1, webpages_toread + 1):
    if n != 1:
        n_shelf_to_read = shelf_to_read + '&page=' + str(n)
        to_read = parse(n_shelf_to_read).getroot()

    x_titles = to_read.xpath('//td[@class="field title"]//a[text()]')
    append_text(x_titles, titles)
    x_auth = to_read.xpath('//td[@class="field author"]//a[text()]')
    append_text(x_auth, authors)
    

# from 'computers'
comp_titles = []

for n in range(1, webpages_comp + 1):
    if n != 1:
        n_shelf_computers = shelf_computers + '&page=' + str(n)
        computers = parse(n_shelf_computers).getroot()

    x_comp_titles = computers.xpath('//td[@class="field title"]//a[text()]')
    append_text(x_comp_titles, comp_titles)
    

# compare to-read and computers
toread_comp_titles = []
for elem in comp_titles:
    for el in titles:
        if elem == el:
            toread_comp_titles.append(elem)
        else:
            pass
        

# mapping keys from list_0 to values from list_1
def add_to_dict(list_0, list_1, dictionary):
    if len(list_0) == len(list_1):
        for n in range(0, len(list_0)):
            dictionary[list_0[n]] = list_1[n]
            

# dictionary for to-read
title_author = dict()
add_to_dict(titles, authors, title_author)


# map keys in 'computer' dictionary to values in 'toread'
def map_toread_comp(comp_dict, toread_dict, toread_comp_keys):
    for n in range(0, len(toread_comp_keys)):
        comp_dict[toread_comp_keys[n]] = toread_dict[toread_comp_keys[n]]
        

# dictionary for computers
comp_title_author = dict()
map_toread_comp(comp_title_author, title_author, toread_comp_titles)


printelems(comp_titles)
