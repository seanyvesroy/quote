from bs4 import BeautifulSoup

with open("quotes2.html") as f:
    soup = BeautifulSoup(f,'html.parser')

#def has_class_but_no_id(tag):
#    return tag.has_attr('p') and not tag.has_attr('img')


txt = soup.find_all('div', class_="quoteDetails")

quoteList = []

for a in txt:
    #refine = a.find('em')
    rawtext = a.find('div', class_='quoteText')
    quoteList.append(rawtext.text)
    #print(rawtext.text)
    #print(refine)

finalList = []

for b in quoteList:
    text = b.rsplit('-\n')
    author = b.rsplit(',\n')
    title = b.rsplit('       ')
    data_dict = {'text' : text , 'title': title , 'author' : author}
    finalList.append(data_dict)
    
for c in finalList:
    print(c)