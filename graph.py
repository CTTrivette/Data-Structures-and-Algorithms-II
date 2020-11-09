#Christian Trivette, Student ID: 001307104

class Graph:
    def __init__(self):
        #constructor -> space complexity = O(N)
        self.adjacencyList = {}
        self.edgeWeights = {}
        self.vertexList = []

    def add_vertex(self, new_vertex):
        # method to create a new vertex, add it to the graph's adjacency list, and add it to the graph's
        # vertex list -> time complexity = O(1); space complexity = O(N^2)
        newV = Vertex(new_vertex)
        self.adjacencyList[new_vertex] = []
        self.vertexList.append(newV)

    def add_directed_edge(self, fromVertex, toVertex, weight):
        # method to add a unidirectional weighted edge between 2 vertices -> time complexity = O(1)
        self.edgeWeights[(fromVertex),(toVertex)] = weight
        self.adjacencyList[fromVertex].append(toVertex)

    def add_undirected_edge(self, vertexA, vertexB, weight):
        # method to add a bidirectional weighted edge between 2 vertices -> time complexity = O(1)
        if vertexA not in self.adjacencyList:
            newVertex = self.add_vertex(vertexA)
        if vertexB not in self.adjacencyList:
            newVertex = self.add_vertex(vertexB)
        self.add_directed_edge(vertexA, vertexB, weight)
        self.add_directed_edge(vertexB, vertexA, weight)

    def getVertex(self, n):
        # method to return a vertex if n is equivalent to the vertex's label -> time complexity = O(N)
        for vertex in self.vertexList:
            if n == vertex.label:
                return vertex.label

    def getDistance(self, u, v):
        # method to return the distance between two vertices -> time complexity = O(1)
        return self.edgeWeights[u][v]

class Vertex:
    def __init__(self, label):
        #constructor -> space complexity = O(1)
        self.label = label