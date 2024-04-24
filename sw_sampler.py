
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx



class sw_sampler():
    '''
    Sampler for the Ising(default) or Potts model using the Swendsen-Wang 
    algorithm and provides visualisation. Non-homogeneous are not supported.
    '''
    def __init__(self, x_range, y_range, labels=2, homog=True, beta=0.5):
        """Initialise a sampler with the parameters of the model to sample

        Args:
            x_range (int): range for lattice sites for a grid on the x axis
            y_range (int): range for lattice sites for a grid on the y axis
            labels (int): the amount of labels each lattice site can take
                defaults to 2 for the ising model
            homog (bool): flag indicating the homogeneuity of the model i.e
                True if  Beta_xy = Beta for all x,y
            beta (int or 2d int array): beta value/values for the model

        """
        
        self.labels = labels
        self.x_range = x_range
        self.y_range = y_range
        self.homog = homog
        self.beta = beta
        ''' 
        ising model typically has spin values of 1, -1 whereas general potts
        models have spin values of 1,2,...,labels    
        '''
        self.label_choice = [i for i in range(labels)] if labels > 2 else [-1,1]
        self.data = np.random.choice(self.label_choice, size=(x_range, y_range))
        self.edges = np.zeros((x_range, y_range, 2))
        
        # form edges 
        for ix, iy in np.ndindex(self.data.shape):
            if iy != y_range - 1:
                self.edges[ix, iy, 0] = self.data[ix, iy] == self.data[ix, iy+1]
            if ix != x_range - 1:
                self.edges[ix, iy, 1] = self.data[ix, iy] == self.data[ix+1, iy]
        
        self.G = None
                    
    
    def construct_graph(self):
        '''constructs a networkx graph based on the current edge configuration'''
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
        '''visualises the current configuration'''
        self.construct_graph()
        colours = np.array(["red", "blue", "green", "yellow", "orange",
        "purple", "cyan", "magenta","pink", "brown", "gray", "black", "white"])
        
        cmap = {}
        for i in range(len(self.label_choice)):
            cmap[self.label_choice[i]] = colours[i]
        
        # pos ensures (0,0) is on the top left and (x_range - 1, y_range - 1) is on the bottom right of plot
        pos = {(i,j): (j, self.y_range - 1 - i) for i in range(self.x_range) for j in range(self.y_range)}
        node_colors = [cmap[node[1]["spin"]] for node in self.G.nodes(data=True)]
        nx.draw(self.G, pos, node_color=node_colors, with_labels=False)
        plt.title('Colored Connected Nodes (Ising Model)')
        plt.figure(figsize=(20, 20))  # Adjust the width and height as needed
        plt.show()
    
    def sample_next(self):
        '''samples the next state of the model given the current one. This is
        done by performing one update step of the SW-algorithm'''
        if not self.homog:
            # not implemented
            return
        
        # turn edges with probability q
        q = 1 - np.exp(-1*self.beta)
        for ix, iy, e in np.ndindex(self.edges.shape):
            if self.edges[ix,iy,e] == 1:
                self.edges[ix,iy,e] = 1 if np.random.rand() < q else 0
        
        # resconstruct graph and get connected components
        self.construct_graph()
        connected_components = list(nx.connected_components(self.G))
        
        # assign a random colour to a random number of connected components
        num_elements = np.random.randint(1, len(connected_components) + 1)
        random_components = np.random.choice(connected_components, size=num_elements, replace=False)
        for random_component in random_components:
            colour = np.random.choice(self.label_choice)
            for node in random_component:
                self.data[node] = colour

        # re-form edges between adjacent nodes sharing the same spin value
        for ix, iy in np.ndindex(self.data.shape):
            if iy != self.y_range - 1:
                self.edges[ix, iy, 0] = self.data[ix, iy] == self.data[ix, iy+1]
            if ix != self.x_range - 1:
                self.edges[ix, iy, 1] = self.data[ix, iy] == self.data[ix+1, iy]
        
        self.construct_graph()
        


plt.rcParams['figure.figsize'] = [20,20]

s = sw_sampler(64,64, 3, True, 1)

s.visualise()
for i in range(1000):
    s.sample_next()
    s.visualise()


