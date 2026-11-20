from evolution.genome import Genome, NodeGene, ConnectionGene

import math

class NeuralNetwork:
    def __init__(self, genome: Genome):
        self.genome = genome
        self.input_size = 30

    def forward(self, inputs):
        node_values = self.create_inputs(inputs=inputs)

        pending_hidden_layer_nodes = [node for node in self.genome.nodes.values() if node.node_type == "hidden"]

        while pending_hidden_layer_nodes:

            for node in pending_hidden_layer_nodes[:]:
                if self.node_is_calcuable(node, node_values):
                    node_values[node.id] = self.calculate_node(node, node_values)

                    pending_hidden_layer_nodes.remove(node)

        output_node = [gene_id for gene_id, gene in self.genome.nodes.items() if gene.node_type == "output"][0]
        p = self.calculate_network_output(self.genome.nodes[output_node], node_values)

        return p


    def create_inputs(self, inputs):
        node_values = {}
        
        input_nodes = [gene_id for gene_id, gene in self.genome.nodes.items() if gene.node_type == "input"]

        print(input_nodes)
        print(inputs)

        if len(input_nodes) != len(inputs):
            raise ValueError("Input count does not match input nodes")

        for node, value in zip(input_nodes, inputs):
            node_values[node] = value

        return node_values

    def calculate_node(self, node: NodeGene, node_values: list[ConnectionGene]):
        output = self.calculate_node_weights(node, node_values)

        return max(0, output)

    def node_is_calcuable(self, node: NodeGene, node_values: list[ConnectionGene]):
        incoming = self.genome.get_connections_to_node(node)

        return all(connection.source_id in node_values for connection in incoming if connection.enabled)

    def calculate_network_output(self, output_node: NodeGene, node_values: list[ConnectionGene]):

        output = self.calculate_node_weights(output_node, node_values)

        return 1 / (1 + math.exp(-output))

    def calculate_node_weights(self, node: NodeGene, node_values: list[ConnectionGene]):
        incoming = self.genome.get_connections_to_node(node)

        total = node.bias

        for connection in incoming:
            if not connection.enabled:
                continue

            total += node_values[connection.source_id] * connection.weight

        return total

nodes = {
    0: NodeGene(id=0, node_type="input", bias=0),
    1: NodeGene(id=1, node_type="input", bias=0),
    2: NodeGene(id=2, node_type="input", bias=0),
    3: NodeGene(id=3, node_type="input", bias=0),
    4: NodeGene(id=4, node_type="input", bias=0),
    5: NodeGene(id=5, node_type="input", bias=0),
    6: NodeGene(id=6, node_type="input", bias=0),
    7: NodeGene(id=7, node_type="input", bias=0)
}

connections = []

genome = Genome(nodes=nodes, connections=connections)

network = NeuralNetwork(genome=genome)