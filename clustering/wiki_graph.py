import collections

WikiPage = collections.namedtuple('WikiPage', 'title content topic')

class WikiNode(object):
    def __init__(self, title, content, topic):
        self.wiki_page = WikiPage(
            title=title, content=content, topic=topic)
        self.wiki_neighbors = []
    
    def add_wiki_neighbors(self, wiki_node):
        self.wiki_neighbors.append(wiki_node)

class WikiGraph(object):
    def __init__(self, n_tokens=100):
        self.wiki_nodes = []
        self.n_tokens = n_tokens
    
    def add_wiki_node(self, wiki_node):
        self.wiki_nodes.append(wiki_node)
