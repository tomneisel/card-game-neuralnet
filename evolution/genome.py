class NodeGene:
    def __init__(self, id, node_type, bias):
        self.id = id
        self.node_type = node_type
        self.bias = bias

class ConnectionGene:
    def __init__(self, source_id, target_id, weight, enabled):
        self.source_id = source_id
        self.target_id = target_id
        self.weight = weight
        self.enabled = enabled
        
class Genome:
    def __init__(self, nodes: dict[NodeGene], connections: list[ConnectionGene]):
        self.nodes = nodes
        self.connections = connections

    def get_connections_to_node(self, node: NodeGene):
        return [connection for connection in self.connections if connection.target_id == node.id]