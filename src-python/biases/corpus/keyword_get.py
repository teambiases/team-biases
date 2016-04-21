"""
This will take the mysql connector and get page data from the database. 
We will be using one seed article, the Cold War category page, and expand
upon the links in a breadth first search. Articles that are classified as 
relevant will be added to some text file somewhere *CHANGE**

REQUIRES: Mysql connector for Python 3.4.3
"""
import mysql.connector as connector
import re

def connect(user="query",
            password="wiki",
            host="thinktank.student.umd.edu",
            database="wikipedia"):
    """
    This returns a connection to the database, it needs to be closed at
    the end of use through the |[connection]|.close function call.
    """
    return connector.connect(user=user,
                            password=password,
                            host=host,
                            database=database)
def threshold(text):
    return True

def clean_link(link):
    """
    The links need to be processed in a number of ways: 
    First: We need to extract the links form the text and iterate over them
    Second: Then, we truncate any link that has a template attached because
    those pages have too much bloat. Redirects are treated as next level
    links, but in future implementations we'll add them to the current
    iteration since that prevents a redirect chain from destroying the depth
    gauge.
    Third, we eliminate the extra markup and replace spaces with underscores.
    """
    link_pattern2 = re.compile('Template:.*|File:.*|w:.*|:*:.*')
    link_replace1 = re.compile('Category:|Wikipedia:')
    link_replace2 = re.compile('#redirect|#REDIRECT')
    link_replace3 = re.compile('(\[\[)|(\]\])')
    if re.search(link_pattern2,link) == None:
        link = re.sub(link_replace3,"",link)
        link = re.sub(link_replace1,"",link)
        link = re.sub(link_replace2,"",link)
        link = re.sub(" ","_",(re.split('[|#]',link)[0]))
        link = re.sub("\"","\\\"",link)
        link = re.sub("\'","\\\'",link)
        return link
    return ""
def gather_corpus(seed,depth):
    """
    This function will take a list of seed articles and return a list of article
    ids that pass the 
    """
    existing = set()
    pagelist = set()
    level = 0
    queue = [[(x,'') for x in seed]]
    c = connect()
    cursor = c.cursor()
    # We first get the text from the seed article
    query_text = ("SELECT page_id, title, text FROM article WHERE title = \"%s\";")
    text_replace1 = re.compile('(\{\{.*\}\})|(<.*>)')
    link_match1 = re.compile('\[\[.*?(?!\[\[])\]\]')
    while (level != depth):
        lst = queue.pop()
        temp = set()
        level += 1
        for item,top in lst:
            print(top,"|||",item)
            cursor.execute(query_text % (item))
            for p_id, title, text in cursor:
                text = re.sub(text_replace1,"",text.decode("utf-8"))
                if threshold(text.split()):
                    pagelist.add((p_id,title.decode("utf-8")))
                    found = re.findall(link_match1,text)
                    if found:
                        for link in found:
                            link = clean_link(link)
                            if not link in existing:
                                temp.add((link,item)) 
                                existing.add(link)
        queue.append(list(temp))
    c.close()
    return list(pagelist)

def export(seed,depth,file):
    with open(file,'w') as f:
        for i,j in gather_corpus(seed,depth):
            f.writelines(str(i)+", "+str(j)+"\n")
