

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class sw_sampler():
    def __init__(self, x_range, y_range, labels=2, homog=True, beta=0.5):
        self.labels = labels
        self.x_range = x_range
        self.y_range = y_range
        self.homog = homog
        self.beta = beta
        self.data = np.random.choice([i for i in range(labels)], size=(x_range, y_range))
        self.edges = np.zeros((x_range, y_range, 2))
        
        for ix, iy in np.ndindex(self.data.shape):
            if iy != y_range - 1:
                self.edges[ix, iy, 0] = self.data[ix, iy] == self.data[ix, iy+1]
            if ix != x_range - 1:
                self.edges[ix, iy, 1] = self.data[ix, iy] == self.data[ix+1, iy]
        
        self.G = None
        self.constructed = False

                    
    
    def construct_graph(self):
        self.G = nx.Graph()
        
        for ix, iy in np.ndindex(self.data.shape):
            # Add nodes with attributes corresponding to their spin value
            self.G.add_node((ix, iy), spin=self.data[ix, iy])
        
        for ix, iy in np.ndindex(s.data.shape):
            current_edges = s.edges[ix, iy]
            if current_edges[0] == 1:
                self.G.add_edge((ix, iy), (ix, iy+1))
            if current_edges[1] == 1:
                self.G.add_edge((ix, iy), (ix+1, iy))
        self.constructed = True
    
    def visualise(self):
        if not self.constructed:
            self.construct_graph()
        
        pos = {(i,j): (j, self.y_range - 1 - i) for i in range(self.x_range) for j in range(self.y_range)}
        node_colors = ['blue' if node[1]['spin'] == 0 else 'red' for node in self.G.nodes(data=True)]
        nx.draw(self.G, pos, node_color=node_colors, with_labels=False)
        plt.title('Colored Connected Nodes (Ising Model)')
        plt.figure(figsize=(20, 20))  # Adjust the width and height as needed
        plt.show()
    
    def sample_next(self):
        if not self.homog:
            # not implemented
            return
        
        
        q = 1 - np.exp(-1*self.beta)
        print(q)
        a = 0
        b = 0
        for ix, iy, e in np.ndindex(self.edges.shape):
            if self.edges[ix,iy,e] == 1:
                a+=1
                self.edges[ix,iy,e] = 1 if np.random.rand() < q else 0
                b = b +1 if self.edges[ix,iy,e] == 0 else b 
        
        self.construct_graph()
        connected_components = list(nx.connected_components(self.G))
        
        num_elements = np.random.randint(1, len(connected_components) + 1)  # Choose between 1 and the length of the array
        
        # Choose random elements from the array
        random_components = np.random.choice(connected_components, size=num_elements, replace=False)
        for random_component in random_components:
            colour = 1 if np.random.rand() < 0.5 else 0
            for node in random_component:
                self.data[node] = colour

        
        for ix, iy in np.ndindex(self.data.shape):
            if iy != self.y_range - 1:
                self.edges[ix, iy, 0] = self.data[ix, iy] == self.data[ix, iy+1]
            if ix != self.x_range - 1:
                self.edges[ix, iy, 1] = self.data[ix, iy] == self.data[ix+1, iy]
        
        self.construct_graph()
        


plt.rcParams['figure.figsize'] = [20,20]

s = sw_sampler(64,64, 2, True, 1)

s.visualise()
for i in range(1000):
    s.sample_next()
    s.visualise()




# Plot the graph with nodes colored based on spin value

