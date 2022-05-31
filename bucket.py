
import copy

import networkx as nx

class Bucket:
    def __init__(self, capacity, level):
        self.capacity = capacity
        self.level = level

    def available_volume(self):
        """The amount available for transfer"""
        return self.level

    def available_capacity(self):
        """The amount of space left in the bucket"""
        return self.capacity - self.level

    def add_volume(self, amount):
        """Adds quantity to the bucket"""
        # TODO raise exception: self.level + amont <= self.capacity
        self.level += amount

    def remove_volume(self, amount):
        # TODO raise exception: test self.level -= amount > 0
        self.level -= amount


class BucketList(list):
    """Class inherits the Python built in list type"""

    def __init__(self, *args):
        """Provide the constructor with a list of Buckets"""
        list.__init__(self, *args)
        self.graph = None

    def __hash__(self):
        """Make this object hashable"""
        #string_ints = [str(int) for int in self.volumes()]
        return hash(""+str(self))

    def __str__(self):
        string_ints = [str(int) for int in self.volumes()]
        return ','.join(string_ints)

    def volumes(self):
        """returns a list of volumes"""
        return list(map(lambda bucket: bucket.level, self))

    def sizes(self):
        """returns a list of bucket sizes"""
        return list(map(lambda bucket: bucket.capacity, self))

    def valid_transfers(self):
        """
            Transfer quantities of water from one bucket to another, without spilling a drop

            :returns: A list of BucketLists, these are the valid transfers from this BucketList 
            :rtype: list of BucketLists
        """
        valid_target_bucketlists = []

        for source_id, source_bucket in enumerate(self):
            for target_id, target_bucket in enumerate(self):
                if source_id != target_id:
                    if source_bucket.available_volume() > 0:
                        if target_bucket.available_capacity() > 0:
                            valid_target = copy.deepcopy(self)
                            #valid_target = list(buckets_volumes).copy()
                            if target_bucket.available_capacity() >= source_bucket.available_volume():
                                transfer_amount = source_bucket.available_volume()
                            else:
                                transfer_amount = target_bucket.available_capacity()

                            valid_target[source_id].remove_volume(transfer_amount)
                            valid_target[target_id].add_volume(transfer_amount)
                            valid_target_bucketlists.append(valid_target)

        return valid_target_bucketlists

    def generate_graph(self):
        """Produce the graph we will query"""
        self.graph = nx.DiGraph()
        self.graph.add_node(str(self), list=self)
        node_list = [str(self)]
        self.build_graph(self,node_list)


    def build_graph(self,bucket_list,node_list):
        """Worker to generate our graph"""
        for target_bucket_list in bucket_list.valid_transfers():
            # for possible buckets lists
            if str(target_bucket_list) not in node_list:
                # if not exist add as a node
                self.graph.add_node(str(target_bucket_list), list=target_bucket_list)
                node_list.append(str(target_bucket_list))
                self.build_graph(target_bucket_list, node_list)
            # add the edge
            self.graph.add_edge(str(bucket_list), str(target_bucket_list))

    def number_of_nodes(self):
        """how many nodes are in our graph"""
        if self.graph is None:
            self.generate_graph()
        return nx.number_of_nodes(self.graph)

    def find_route_to(self,to_bucket_list):
        """Provide the target bucket list as a string"""

        # TODO we could add the total volume up and compare with the volume we have 

        if self.graph is None:
            self.generate_graph()

        return nx.shortest_path(self.graph, source=str(self), target=to_bucket_list) if self.graph.has_node(to_bucket_list) else "Not possible"
