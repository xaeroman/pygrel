#!/usr/bin/python
#
# Copyright (C) 2007 Saket Sathe
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
# $LastChangedBy: xaeroman $
# $LastChangedDate: 2008-12-13 02:02:58 +0100 (Sat, 13 Dec 2008) $
# $LastChangedRevision: 96 $
#
#


from AbstractGraph import *
from sets import Set
from random import randint, choice
from pygel.BaseElements.Edge import *
from pygel.BaseElements.Vertex import *

class NumberedEdgeDirectedGraph(AbstractGraph):

    """ Represents a numbered edge graph. Numbered edges are required to distinguish multiple edges between
        same set of vertices. This class also provides an indexed vertex and edge sets. These indices have certain advantages
        while computing in-degree and out-degree distributions.

        \ingroup Graph        
    """
    
    def __init__(self):
        """ Constructs a numbered edge graph
        """
        ## Dictionary of edges, indexed by edge number
        self.edgeIndex = {}

        ## Dictionary of vertices, indexed by vertex number
        self.vertexIndex = {}

        ## Dictionary of vertices, indexed by parent
        self.parentIndex = {}

        ## Dictionary of vertices and edge numbers, indexed by parent
        self.parentEdgeIndex = {}        
        
        ## Last edge number assigned
        self.__lastEdgeNumber = -1

        ## Dictionary of in-degree counts. Used for efficiently computing in-degree distribution
        self.__inDegreeCount = {}

        ## Dictionary of out-degree counts. Used for efficiently computing out-degree distribution
        self.__outDegreeCount = {}

        ## Dictionary of degree counts. Used for efficiently computing degree distribution
        self.__degreeCount = {}

    def addEdge(self, edge):
        """ Adds an edge to a graph. It also updates the vertex and edge indices. 

            @param edge Edge of type BaseElements::Edge to be added to the graph
        """
        self.__lastEdgeNumber += 1
        self.edgeIndex[self.__lastEdgeNumber] = edge

        startVertex = edge.startVertex
        endVertex = edge.endVertex


        startVertexNumber = startVertex.vertexNumber
        endVertexNumber = endVertex.vertexNumber

        vertexIndex = self.vertexIndex
        parentIndex = self.parentIndex
        parentEdgeIndex = self.parentEdgeIndex

        if startVertexNumber not in vertexIndex:
            vertexIndex[startVertexNumber] = startVertex

        if endVertexNumber not in vertexIndex:
            vertexIndex[endVertexNumber] = endVertex


        if startVertexNumber not in parentIndex:
            parentIndex[startVertexNumber] = [endVertexNumber]
        else:
            parentIndex[startVertexNumber].append(endVertexNumber)

        if startVertexNumber not in parentEdgeIndex:
            parentEdgeIndex[startVertexNumber] = [[endVertexNumber, self.__lastEdgeNumber]]
        else:
            parentEdgeIndex[startVertexNumber].append([endVertexNumber, self.__lastEdgeNumber])

            
        try:
            self.__outDegreeCount[startVertexNumber] += 1
            self.__degreeCount[startVertexNumber] += 1
        except KeyError:
            self.__outDegreeCount[startVertexNumber] = 1
            self.__degreeCount[startVertexNumber] = 1
            
        try:
            self.__inDegreeCount[endVertexNumber] += 1
            self.__degreeCount[endVertexNumber] += 1
        except KeyError:
            self.__inDegreeCount[endVertexNumber] = 1
            self.__degreeCount[endVertexNumber] = 1
            

    def deleteEdge(self, edgeNumber):
        """ Delete an edge

            @param edgeNumber Edge number to be deleted
        """
        
        edge = self.edgeIndex[edgeNumber]
        startVertex = edge.startVertex
        endVertex = edge.endVertex

        startVertexNumber = startVertex.vertexNumber
        endVertexNumber = endVertex.vertexNumber

        vertexIndex = self.vertexIndex
        parentIndex = self.parentIndex
        parentEdgeIndex = self.parentEdgeIndex

        if startVertexNumber in parentIndex:
            # TODO: throws exception
            parentIndex[startVertexNumber].remove(endVertexNumber)

        if startVertexNumber in parentEdgeIndex:
            # TODO: throws exception
            parentEdgeIndex[startVertexNumber].remove([endVertexNumber, edgeNumber])
            
        try:
            self.__outDegreeCount[startVertexNumber] -= 1
            self.__degreeCount[startVertexNumber] -= 1
        except KeyError:
            pass
            
        try:
            self.__inDegreeCount[endVertexNumber] -= 1
            self.__degreeCount[endVertexNumber] -= 1
        except KeyError:
            pass
        
        del self.edgeIndex[edgeNumber]

    def addVertex(self, vertexNumber):
        """ Adds a vertex. Should be used with care

            @param vertexNumber Vertex number of vertex to be added
            @throws PackageExceptions::VertexError
        """
        try:
            self.vertexIndex[vertexNumber]
            raise VertexError(vertexNumber, ErrorMessages.vertexAlreadyExists)
        except KeyError:
            self.vertexIndex[vertexNumber] = Vertex(vertexNumber)
            return 

    def deleteVertex(self, vertexNumber):
        """ Deletes a vertex. Should be used with care

            @param vertexNumber Vertex number to be deleted
        """
        del self.vertexIndex[vertexNumber]

    def getEdges(self):
        """ Get all graph edges

            @return edgeIndex Dictionary of edges, indexed by edge number
        """
        return self.edgeIndex

    def getVertices(self):
        """ Get all graph vertices

            @return vertexIndex Dictionary of vertices, indexed by vertex number
        """
        return self.vertexIndex

    def getLastEdgeNumber(self):
        """ Get the last edge number

            @return __lastEdgeNumber the last edge number assigned to edges. 
        """
        return self.__lastEdgeNumber
    
    def getOutNeighbors(self, vertexNumber):
        """ Get out-neighbors for a vertex

            @param vertexNumber Vertex number for which out-neighbors have to be obtained
            @return outNeighbors List of out-neighbors. Each element of type BaseElements::Vertex
        """
        outNeighbors = []
        edges = self.edgeIndex.values()
        for edge in edges:
            if edge.startVertex.vertexNumber == vertexNumber:
                outNeighbors.append(edge.startVertex)
        return outNeighbors

    def getInNeighbors(self, vertexNumber):
        """ Get in-neighbors for a vertex

            @param vertexNumber Vertex number for which in-neighbors have to be obtained
            @return inNeighbors List of in-neighbors. Each element of type BaseElements::Vertex
        """
        inNeighbors = []
        edges = self.edgeIndex.values()
        for edge in edges:
            if edge.endVertex.vertexNumber == vertexNumber:
                inNeighbors.append(endVertex)
        return inNeighbors

    def getNumberOfOutNeighbors(self, vertexNumber):
        """ Get number of out-neighbors for a vertex

            @param vertexNumber Vertex number for which number of out-neighbors have to be obtained
            @return Number of out-neighbors
        """ 

        return self.__outDegreeCount[vertexNumber]

    def getNumberOfInNeighbors(self, vertexNumber):
        """ Get number of in-neighbors for a vertex

            @param vertexNumber Vertex number for which number of in-neighbors have to be obtained
            @return Number of in-neighbors
        """ 
        return self.__inDegreeCount[vertexNumber]

    def getNumberOfNeighbors(self, vertexNumber):
        """ Get number of neighbors for a vertex

            @param vertexNumber Vertex number for which number of neighbors have to be obtained
            @return Number of neighbors
        """ 
        return self.__degreeCount[vertexNumber]

    def getInDegreeDistribution(self):
        """ Get in-degree distribution

            @return inDegreeDistribution Dictionary indexed on in-degree. Values are the number of nodes for a in-degree
        """
        inDegreeDistribution = {}
        inDegreeCount = self.__inDegreeCount
        getNumberOfInNeighbors = self.getNumberOfInNeighbors
        vertexNumbers = self.vertexIndex.keys()
        for vertexNumber in vertexNumbers:
            try:
                numberOfInNeighbors = inDegreeCount[vertexNumber]
            except KeyError:
                numberOfInNeighbors = 0
                
            try:
                inDegreeDistribution[numberOfInNeighbors] += 1
            except KeyError:
                inDegreeDistribution[numberOfInNeighbors] = 1
        return inDegreeDistribution

    def getOutDegreeDistribution(self):
        """ Get out-degree distribution

            @return outDegreeDistribution Dictionary indexed on in-degree. Values are the number of nodes for a out-degree
        """
        outDegreeDistribution = {}
        outDegreeCount = self.__outDegreeCount
        getNumberOfOutNeighbors = self.getNumberOfOutNeighbors
        vertexNumbers = self.vertexIndex.keys()
        
        for vertexNumber in vertexNumbers:
            try:
                numberOfOutNeighbors = outDegreeCount[vertexNumber]
            except KeyError:
                numberOfOutNeighbors = 0
                
            try:
                outDegreeDistribution[numberOfOutNeighbors] += 1
            except KeyError:
                outDegreeDistribution[numberOfOutNeighbors] = 1
        return outDegreeDistribution

    def getJointDistribution(self):
        """ Get joint-degree distribution

            @return jointDegreeDistribution Dictionary indexed on out-degree and in-degree. Values are the number of nodes for a given combination of out-degree and in-degree
        """
        
        jointDistribution = {}
        outDegreeCount = self.__outDegreeCount
        inDegreeCount = self.__inDegreeCount
        vertexNumbers = self.vertexIndex.keys()

        for vertexNumber in vertexNumbers:
            try:
                numberOfOutNeighbors = outDegreeCount[vertexNumber]
            except KeyError:
                numberOfOutNeighbors = 0

            try:
                numberOfInNeighbors = inDegreeCount[vertexNumber]
            except KeyError:
                numberOfInNeighbors = 0

            try:
                jointDistribution[numberOfOutNeighbors][numberOfInNeighbors] += 1
            except KeyError:
                try:
                    jointDistribution[numberOfOutNeighbors][numberOfInNeighbors] = 1
                except KeyError:
                    jointDistribution[numberOfOutNeighbors] = {numberOfInNeighbors: 1}

        return jointDistribution
    
    def getDegreeDistribution(self):
        """ Get degree distribution

            @return degreeDistribution Dictionary indexed on degree. Values are the number of nodes for a degree
        """
        degreeDistribution = {}
        degreeCount = self.__degreeCount
        vertexNumbers = degreeCount.keys()
        for vertexNumber in vertexNumbers:
            numberOfNeighbors = degreeCount[vertexNumber]
            try:
                degreeDistribution[numberOfNeighbors] += 1
            except KeyError:
                degreeDistribution[numberOfNeighbors] = 1
        return degreeDistribution

    def getVerticesByInDegree(self, degree):
        """ Gets all the vertices with a particular in-degree

            @param degree In-degree to look for
            @return degreeNodes List of vertices. Each element of type BaseElements::Vertex
        """
        degreeNodes = []
        vertexIndex = self.vertexIndex
        inDegreeCount = self.__inDegreeCount
        for vertexNumber in inDegreeCount:
            if inDegreeCount[vertexNumber] == degree:
                degreeNodes.append(vertexIndex[vertexNumber])
        return degreeNodes

    def getVerticesByOutDegree(self, degree):
        """ Gets all the vertices with a particular out-degree

            @param degree Out-degree to look for
            @return degreeNodes List of vertices. Each element of type BaseElements::Vertex
        """
        degreeNodes = []
        vertexIndex = self.vertexIndex
        outDegreeCount = self.__inDegreeCount
        for vertexNumber in outDegreeCount:
            if outDegreeCount[vertexNumber] == degree:
                degreeNodes.append(vertexIndex[vertexNumber])
        return degreeNodes

    def getSCComponents(self, getLargest):
        """ Gets the strongly connected components of a graph. It uses <A HREF="http://en.wikipedia.org/wiki/Tarjan's_strongly_connected_components_algorithm">Tarjan's strongly connected components algorithm.</A>

        
            @param getLargest If greater than 0, only returns the largest connected component
            @return allSCC List of a List of connected components
        """

        def min(a, b):
            if a >= b:
                return b
            elif b >= a:
                return a

        def visit(vertexNumber, visitNumber, lowLinkNumber, vertexTracker):

            vertexTracker[vertexNumber][0] = 1
            visitNumber[vertexNumber] = counter[0]
            lowLinkNumber[vertexNumber] = counter[0]

            counter[0] += 1
            stackAppend(vertexNumber)

            children = []
            try:
                children = parentIndex[vertexNumber]
            except KeyError:
                #print "Vertex %s has no children" % (v.vertexNumber)
                pass
                
            for child in children:
              if vertexTracker[child][1] != 1:
                try:
                    lowLinkNumber[vertexNumber] = min(lowLinkNumber[vertexNumber], visitNumber[child])
                except KeyError:
                    pass 
                        
                    visit(child, visitNumber, lowLinkNumber, vertexTracker)

                    lowLinkNumber[vertexNumber] = min(lowLinkNumber[vertexNumber], lowLinkNumber[child])
                    
            if lowLinkNumber[vertexNumber] == visitNumber[vertexNumber]:
                scc = []
                sccAppend = scc.append
                while stackGetItem(len(stack)-1) != vertexNumber:
                    poppedVertex = stackPop()
                    sccAppend(poppedVertex)
                    vertexTracker[poppedVertex][1] = 1
                poppedVertex = stackPop()
                sccAppend(poppedVertex)
                vertexTracker[poppedVertex][1] = 1
                
                if getLargest > 0:
                    if len(scc) > largestComponentSize[0]:
                        #print "Largest component till now: " , len(scc)
                        largestComponentSize[0] = len(scc)
                        if len(allSCC) == 1: del allSCC[0]
                        allSCC.append(scc) 
                elif getLargest == 0:
                    allSCC.append(scc)
                    #print "Component found and attached. Total number of components: ", len(allSCC)


        
        allSCC = []

        visitNumber = {}
        lowLinkNumber = {}

        vertexTracker = {}  # [vertexVisited, vertexTaken]

        allVertices = self.vertexIndex

        parentIndex = self.parentIndex

        # Initializing the stack and its reference functions
        stack = []
        stackAppend = stack.append
        stackPop = stack.pop
        stackGetItem = stack.__getitem__
        stackLen = len(stack)

        counter = [0]
        largestComponentSize = [0]


        for vertexNumber in allVertices:
            vertexTracker[vertexNumber] = [0,0]
            
        for vertexNumber in allVertices:
                if not vertexTracker[vertexNumber][0]:
                    vertexTracker[vertexNumber][0] = 1
                    visit(vertexNumber, visitNumber, lowLinkNumber, vertexTracker)
                
        return allSCC
        
    def getOutComponent(self, stronglyCC):
        """ Gives the out component for a strongly connected component


            @param stronglyCC Strongly connected component for which th out-component is to be determined
            @return outComponent List of vertices in the out component
        """
        
        parentIndex = self.parentIndex
        collapsedParentIndex = {}
        collapsedParentIndex[-1] = []

        def dfs(v, visitedVertices):
            children = []
            try:
                children = collapsedParentIndex[v]
            except KeyError:
                #print "Vertex %s has no children" % (v)
                pass
            for child in children:
                if child not in visitedVertices:
                    visitedVertices.append(child)
                    dfs(child, visitedVertices)

        stronglyCCLookup = {}
        for each in stronglyCC:
            stronglyCCLookup[each] = ''

        for parent in parentIndex:
            newChildren = []
            oldChildren = parentIndex[parent]
            for child in oldChildren:
                try:
                    if stronglyCCLookup[child] == '':
                        newChildren.append(-1)
                except KeyError:
                    newChildren.append(child)                   

                    
            try:
                if stronglyCCLookup[parent] == '':  
                        collapsedParentIndex[-1].extend(newChildren)

            except KeyError:
                collapsedParentIndex[parent] = newChildren
                
        newChildren = []
        for each in collapsedParentIndex[-1]:
            if each != -1 and each not in newChildren:
                newChildren.append(each)

        collapsedParentIndex[-1] = newChildren
#        print collapsedParentIndex
        outComponent = []
        dfs(-1, outComponent)

        return outComponent

    def writeCC(self, fileName, allSCC):
        """ Write the connected components to a file

        
            @param fileName File name to store the connected components
            @param allSCC List of list of connected components
        """
        f = open(fileName,'w')
        for compNumber in range(0,len(allSCC)):
            f.write("Component number %s: " % (compNumber))
            f.write("%s\n" % (str(allSCC[compNumber])))
        f.close()

    def writeEdges(self, fileName, format):
        """ Write edges to file

            @param fileName File name to store edges in
            @param format Format of output file. Can take values: <br>
                          'simple' = simple format <br>
                          'dot' = format compatible with 'dot' command
                          
        """
        edges = self.edgeIndex.values()
        if format == 'simple':
            f = open(fileName,'w')
            for edge in edges:
                f.write("%s -> %s\n" % (edge.startVertex.vertexNumber, edge.endVertex.vertexNumber))
            f.close()
        elif format == 'dot':
            f = open(fileName,'w')
            f.write("digraph G { \n")
            for edge in edges:
                f.write("%s -> %s;\n" % (edge.startVertex.vertexNumber, edge.endVertex.vertexNumber))
            f.write("} \n")
            f.close()

    def readEdges(self, fileName, format):
        """ Read edges from file

            @param fileName File name to read edges from
            @param format Format of input file. Can take values: <br>
                          'simple' = simple format
        """
        f = open(fileName)
        if format == 'simple':
            edgesRaw = f.read().split("\n")

            if edgesRaw[-1] == '': edgesRaw = edgesRaw[:-1]

            for edge in edgesRaw:
                [startVertex, endVertex] = edge.split("->")
                newEdge = Edge(Vertex(int(startVertex)), Vertex(int(endVertex)))
                self.addEdge(newEdge)

    def findEdge(self, edgeNumber):
        """ Find edge with a given edge number

            @param edgeNumber Edge number to look for
            @throws PackageExceptions::EdgeError
            @return Matched edge of type BaseElements::Edge
            
        """
        try:
            return self.edgeIndex[edgeNumber]
        except KeyError:
            raise EdgeError(edgeNumber, ErrorMessages.edgeNotFound)
    
    def findVertex(self, vertexNumber):
        """ Find vertex with a given vertex number

            @param vertexNumber Vertex number to look for
            @throws PackageExceptions::VertexError
            @return Matched vertex of type BaseElements::Vertex
        """
        try:
            return self.vertexIndex[vertexNumber]
        except KeyError:
            raise VertexError(vertexNumber, ErrorMessages.vertexNotFound)

    def hasVertex(self, vertexNumber):
        """ Checks if vertex is present

            @param vertexNumber Vertex number of the vertex to check
            @return 0 if found. 1 if not found
        """
        try:
            rs = self.findVertex(vertexNumber)
            return 0
        except VertexError, e:
            return 1

