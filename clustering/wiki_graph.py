import collections
from enum import Enum
from tqdm import tqdm
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# =======================================================================================================================

WikiPage = collections.namedtuple('WikiPage', 'id title content topic')

class topics(Enum):
    """Enum to group the topics present in the original dataset"""
    business = 0
    cybersecurity = 1
    technology = 2

# =======================================================================================================================


class WikiNode(object):
    """
    A class used to represent a wikipedia node

    ...

    Attributes
    ----------
    wiki_page : namedtuple WikiPage.
        A named tuple that contains all the information of a wikipage (id, title, content, topic).
        id: int
        title: str
        content: List[str]
        topic: str
    name : str
        The name of the animal.
    wiki_neighbors : dict
        A dictionnary to store the neighbors of a given wikinode.
        key: WikiNode
        value: the number of tokens in common


    Methods
    -------
    add_wiki_neighbor(wiki_neighbor, constraint=None)
        Adds a neighbor to a wiki_node only if there is no contraint on the number of tokens
        in common between the wikipages or if a contraint is established and completed by the nodes.
    """

    def __init__(self, id, title, content, topic):
        self.wiki_page = WikiPage(
            id=id, title=title, content=set(content), topic=topic)
        self.wiki_neighbors = {}

    def __str__(self):
        return str(self.wiki_page.id) + ":" + str(self.wiki_page.title) + "about" + str(self.wiki_page.topic) + "adjacent:" + str([x.get_id() for x in self.wiki_neighbors])

    def add_wiki_neighbor(self, wiki_neighbor, constraint=None):
        tokens_in_common = len(
            self.wiki_page.content.intersection(wiki_neighbor.wiki_page.content))
        if (constraint and tokens_in_common >= constraint) or not constraint:
            self.wiki_neighbors[wiki_neighbor] = tokens_in_common

    def get_id(self):
        return self.wiki_page.id

    def get_topic(self):
        return self.wiki_page.topic

    def get_weight(self, neighbor):
        return self.wiki_neighbors.get(neighbor, None)

    def get_wiki_neighbors(self):
        return self.wiki_neighbors.keys()

# =======================================================================================================================


class WikiGraph(object):
    """
    A class used to represent a wikipedia graph

    ...

    Attributes
    ----------
    wiki_nodes : dict(set)
        A dictionnary to store the overall wiki nodes of the dataset.
        key: int 
        value: wikinode

    num_wiki_nodes : int
        The overall number of wikipedia nodes.

    Methods
    -------
    add_wiki_node(id, wiki_page)
        Adds a wiki_node to the wiki_nodes diactionary.

    add_edge(frm, to, constraint=None)
        Creates an edge from the node with id frm to the node with id to.
    
    build_graph(wiki_pages, constraint=None)
        Builds a graph given a list of wikipedia pages and a given constraint (min nb of tokens in common).

    get_wiki_clusters():
        Returns the clusters in the wiki graph corresponding to the connected components in it. 
    """

    def __init__(self):
        self.wiki_nodes = collections.defaultdict(set)
        self.num_wiki_nodes = 0

    def __iter__(self):
        return iter(self.wiki_nodes.values())

    def __str__(self):
        for wiki_page in self:
            for wiki_neighbor in wiki_page.get_wiki_neighbors():
                wiki_page_id = wiki_page.get_id()
                wiki_neighbor_id = wiki_neighbor.get_id()
                print('( %s , %s, %d)' % (wiki_page_id, wiki_page_id,
                                          wiki_page.get_weight(wiki_neighbor)))

    def add_wiki_node(self, id, wiki_page):
        
        if id in self.wiki_nodes:
            # purge the graph for rebuild
            self.wiki_nodes[id].wiki_neighbors = {}
            return self.wiki_nodes[id]
        
        self.num_wiki_nodes += 1
        new_wiki_node = WikiNode(
            id=id, title=wiki_page["title"], content=wiki_page["content"], topic=wiki_page["topic"])
        self.wiki_nodes[id] = new_wiki_node
        
        return new_wiki_node

    def add_edge(self, frm, to, constraint=None):
        
        if frm not in self.wiki_nodes:
            self.add_wiki_node(frm)
        if to not in self.wiki_nodes:
            self.add_wiki_node(to)

        self.wiki_nodes[frm].add_wiki_neighbor(
            self.wiki_nodes[to], constraint)
        self.wiki_nodes[to].add_wiki_neighbor(
            self.wiki_nodes[frm], constraint)

    def build_graph(self, wiki_pages, constraint=None):

        for i in tqdm(range(len(wiki_pages))):
            self.add_wiki_node(i, wiki_pages[i])

        for i in tqdm(range(self.num_wiki_nodes-1)):
            for j in tqdm(range(i+1, self.num_wiki_nodes)):
                self.add_edge(i, j, constraint)

    def get_wiki_clusters(self):
        
        visited = set()
        components = []
        for wiki_node in tqdm(self):
            if wiki_node.wiki_page.id not in visited:
                visited.add(wiki_node.wiki_page.id)
                stack = [wiki_node]
                wiki_cluster = WikiCluster()
                while stack:
                    node = stack.pop()
                    wiki_cluster.add_wiki_node(node)
                    for nei in node.get_wiki_neighbors():
                        if nei not in visited:
                            visited.add(nei)
                            stack.append(nei)
                wiki_cluster.set_title()
                components.append(wiki_cluster)
        return components

    def get_vertex(self, id):
        return self.wiki_nodes.get(id, None)

    def get_wiki_nodes(self):
        return self.vert_dict.keys()

# =======================================================================================================================


class WikiCluster(object):
    """
    A class used to represent a wikipedia cluster of pages.

    ...

    Attributes
    ----------
    wiki_nodes : []
        A list to store the overall wiki nodes of the cluster.

    title : str
        The title of the cluster defined as the most common topic among the wikipedia pages of the cluster.

    Methods
    -------
    add_wiki_node(id, wiki_page)
        Adds a wiki_node to the wiki_nodes list.
    """

    def __init__(self):
        self.wiki_nodes = []
        self.title = ''
        self.topics_count = {t.name: 0 for t in topics}

    def __iter__(self):
        return iter(self.wiki_nodes)

    def __str__(self):
        return "Cluster " + str(self.title)

    def add_wiki_node(self, wiki_node):
        self.wiki_nodes.append(wiki_node)

    def get_topics_count(self):
        return self.topics_count

    def get_title(self):
        return self.title

    def set_title(self):
        for wiki_node in self.wiki_nodes:
            self.topics_count[wiki_node.get_topic()] += 1
        self.title = max(self.topics_count, key=self.topics_count.get)

# =======================================================================================================================
