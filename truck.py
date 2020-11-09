# Christian Trivette, Student ID: 001307104
import packageClass
import csv
import graph
import datetime


class Truck:
    # Truck object constructor -> space complexity = O(N); time complexity = O(1)
    def __init__(self):
        self.truckNum = 0
        self.max_packages = 16
        self.avg_speed = 18  # this is in mph
        self.packagesOnTruck = []  # this lists all the packages on the truck
        self.milesTraveled = 0  # initial distance traveled is 0 since it starts at the hub
        self.locationsVisited = []  # this helps determine where the truck has been
        self.departed = False  # truck starts at hub
        self.pathGraph = graph.Graph()  # graph that depicts where the truck is going to go
        self.departureTime = datetime.datetime.strptime("08:00 AM", "%I:%M %p")
        self.truckTime = self.departureTime
        self.timeLeftHub = self.departureTime

    # This routing algorithm works by reading in 3 separate CSV files - a file with just the distances and 2 files
    # with header information. The algorithm then standardizes the header information by replacing "North" with "N",
    # "South" with "S", "West" with "W" and "East" with "E". Replacing "West" threw off the header labelled "Western
    # Governors" so threw in a special case. Also standardized "Sta" by replacing it with "Station" unless it was
    # "State" was in the header. The algorithm then removes the zip codes from the header labels and gets only the
    # street address from both header files. This allows for standardized information so comparisons between headers
    # can be made more easily. Line 90 helps standardize the headers further by replacing "HUB", as seen in the CSV
    # file, with the street address, which makes for an easier comparison. The algorithm then creates a Graph object and
    # adds bidirectional weighted edges based on the vertical headers, horizontal headers, and distance information.
    # The algorithm then compares the addresses of the packages on the truck to the vertices in the graph object and
    # fills another graph object called pathGraph, which is a graph data structure that holds all the vertices
    # (package destinations) and will hold weighted edges between all the package destinations later in the program.
    # Next, the algorithm sets HUB to the WGUPS address and sets the truck's current location as the hub. The algorithm
    # then adds all the hub's adjacent destinations and all the other vertices' adjacent destinations. The variable
    # closestDistToHub is set to 999.9 in order to assist finding the closest neighbor to the hub. The algorithm will
    # then look for the nearest neighbor to the hub by iterating through all the edge weights and neighbors to the hub.
    # The closest neighbor is set as the variable travelRoute, which is a tuple where travelRoute[0] is the current
    # location and travelRoute[1] is the next destination. Next, the truck will "leave" the hub, which causes all the
    # packages on the truck to have their deliveryStatus set to "EN ROUTE" and timeLeftHub to the time the truck leaves
    # the hub. The truck then "travels" to the closest neighbor, determines how long it will take to get to the
    # destination, add the time difference to truckTime, adds the miles traveled to milesTraveled, and puts the
    # destination into the truck's locationsVisited list. This list exists to ensure the truck does not visit the
    # location again. The truck then iterates through all it's packages, comparing the packages' deliveryStreetAddress
    # variable to the currentLocation. If the packages' deliveryStreetAddress is the same as the currentLocation, the
    # truck updates the packages' status and delivery time and "drops" the package off. The algorithm then removes
    # the path taken. The algorithm repeats this process until all the packages are off the truck. Once all the packages
    # are off the truck, the algorithm then finds the shortest path back to the hub from it's current location,
    # calculates the time to travel back to the hub, travels to the hub, and adds the mileage traveled to milesTraveled.

    def buildRouteAndTravel(self):
        # open the WGUPS Distance Table CSV and read the CSV file into a 2D array -> time and space complexity = O(N^2)
        with open('WGUPS Distance Table CSV.csv', newline='') as distanceCSV:
            distanceTable = [row for row in csv.reader(distanceCSV, delimiter=',')]

        # open the Distance Table Horizontal Headers CSV and read the CSV file into a list -> time and space
        # complexity = O(N)
        with open('Distance Table Horizontal Headers CSV.csv', newline='') as horizontalCSV:
            horizontalHeaders = []
            reader = csv.reader(horizontalCSV, delimiter=',')
            for entry in reader:
                horizontalHeaders.append(entry)

        # open the Distance Table Vertical Headers CSV and read the CSV file into a list -> time and space
        # complexity = O(N)
        with open('Distance Table Vertical Headers CSV.csv', newline='') as verticalCSV:
            verticalHeaders = []
            reader = csv.reader(verticalCSV, delimiter=',')
            for entry in reader:
                verticalHeaders.append(entry)

        # standardize the horizontalHeaders list -> time complexity = O(N^2)
        for i in range(len(horizontalHeaders)):
            for j in range(len(horizontalHeaders[i])):
                horizontalHeaders[i][j] = horizontalHeaders[i][j].replace('South', 'S')
                horizontalHeaders[i][j] = horizontalHeaders[i][j].replace('North', 'N')
                horizontalHeaders[i][j] = horizontalHeaders[i][j].replace('East', 'E')
                if ("Western Governors" in str(horizontalHeaders[i][j])):
                    continue
                if ("Sta" in str(horizontalHeaders[i][j])) and ("State" not in str(horizontalHeaders[i][j])):
                    horizontalHeaders[i][j] = horizontalHeaders[i][j].replace("Sta", "Station")
                horizontalHeaders[i][j] = horizontalHeaders[i][j].replace('West', 'W')

        # standardize the verticalHeaders list -> time complexity = O(N^2)
        for i in range(len(verticalHeaders)):
            for j in range(len(verticalHeaders[i])):
                verticalHeaders[i][j] = verticalHeaders[i][j].replace('South', 'S')
                verticalHeaders[i][j] = verticalHeaders[i][j].replace('North', 'N')
                verticalHeaders[i][j] = verticalHeaders[i][j].replace('East', 'E')
                if ("Western Governors" in str(verticalHeaders[i][j])):
                    continue
                if ("Sta" in str(verticalHeaders[i][j])) and ("State" not in str(verticalHeaders[i][j])):
                    verticalHeaders[i][j] = verticalHeaders[i][j].replace("Sta", "Station"). \
                        replace('Stationtion', 'Station')
                verticalHeaders[i][j] = verticalHeaders[i][j].replace('West', 'W')

        # remove zip codes from vertical headers -> time complexity = O(N)
        for i in range(len(verticalHeaders)):
            verticalHeaders[i][1] = verticalHeaders[i][1].lstrip(' ')
            if i == 0:
                continue
            size = len(verticalHeaders[i][1])
            verticalHeaders[i][1] = verticalHeaders[i][1][:size - 8]

        # get just the street address from horizontal headers -> time complexity = O(N)
        for i in range(len(horizontalHeaders[0])):
            if i == 0:
                splitString = horizontalHeaders[0][i].splitlines()
                horizontalHeaders[0][i] = splitString[1]
                size = len(horizontalHeaders[0][i])
                horizontalHeaders[0][i] = horizontalHeaders[0][i][:size - 2]
            else:
                splitString = horizontalHeaders[0][i].splitlines()
                horizontalHeaders[0][i] = splitString[1]
                horizontalHeaders[0][i] = horizontalHeaders[0][i].lstrip(' ')

        # replace the "HUB" in the vertical headers with the WGUPS street address for standardization -> time
        # complexity = O(1)
        verticalHeaders[0][1] = horizontalHeaders[0][0]

        # graph object for all packages and edges -> time complexity = O(1); space complexity = O(N^2) since the graph
        # object contains a method that will populate a list of lists
        g = graph.Graph()

        # add bidirectional weighted edges to the graph object for all packages -> time complexity = O(N^2)
        for row in range(len(distanceTable)):
            for column in range(len(distanceTable[row])):
                if (distanceTable[row][column]) == '':
                    break
                if verticalHeaders[row][1] == horizontalHeaders[0][column]:
                    break
                g.add_undirected_edge(verticalHeaders[row][1], horizontalHeaders[0][column],
                                      float(distanceTable[row][column]))

        # add vertices to the truck's path graph if the package's street address matches the vertices' label ->
        # time complexity = O(N^2)
        for package in self.packagesOnTruck:
            for vertex in g.adjacencyList.keys():
                if package.deliveryStreetAddress in vertex:
                    self.pathGraph.add_vertex(vertex)

        # set the hub's location -> time complexity = O(1)
        hub = g.getVertex(verticalHeaders[0][1])

        # set the truck's location as the hub -> time complexity = O(1)
        self.currentLocation = hub
        self.locationsVisited.append(hub)

        # add the hub's adjacency list and edge weights to the truck's path -> time complexity = O(N)
        for vertex in list(self.pathGraph.adjacencyList):
            self.pathGraph.add_undirected_edge(vertex, hub, g.edgeWeights.get((vertex, hub)))

        # add all the adjacency lists and edge weights for all the stops to the truck's path -> time complexity = O(N^2)
        for vertexA in list(self.pathGraph.adjacencyList):
            for vertexB in list(self.pathGraph.adjacencyList):
                if vertexA == vertexB:
                    continue
                self.pathGraph.add_undirected_edge(vertexA, vertexB, g.edgeWeights.get((vertexA, vertexB)))

        #arbitrarily high number variable to help determine the nearest neighbor -> time complexity = O(1); space
        #complexity = O(1)
        closestDistToHub = 999.9

        # find nearest neighbor to hub -> time complexity = O(N); space complexity = O(1) since pathGraph is already
        # created and the only new variable being created is travelRoute
        for edge in self.pathGraph.edgeWeights:
            if self.pathGraph.edgeWeights[edge] < closestDistToHub and self.pathGraph.edgeWeights[edge] != 0.0 and (
                    self.currentLocation in list(edge)[0]):
                closestDistToHub = self.pathGraph.edgeWeights[edge]
                travelRoute = edge

        # leave the hub and update the truck's packages' status and time it left the hub -> time complexity = O(N)
        self.departed = True
        self.truckTime = self.departureTime
        for package in self.packagesOnTruck:
            package.deliveryStatus = packageClass.packageStatuses[1]
            package.timeLeftHub = self.departureTime

        # travel to the location identified, calculate the travel time, add the travel time to the truck's time,
        # add the miles traveled to the truck's milesTraveled variable, and add new stop to the locations
        # visited -> time complexity = O(1); space complexity = O(1) since the only new variable being created is
        # travelTimeInMinutes
        travelTimeInMinutes = (closestDistToHub / self.avg_speed) * 60
        self.truckTime += datetime.timedelta(minutes=travelTimeInMinutes)
        self.currentLocation = list(travelRoute)[1]
        self.milesTraveled += closestDistToHub
        self.locationsVisited.append(travelRoute[1])

        # iterate through the truck's packages and deliver any packages whose deliveryStreetAddress matches the
        # truck's current location -> time complexity = O(N)
        for package in self.packagesOnTruck:
            if package.deliveryStreetAddress == self.currentLocation:
                package.deliveryStatus = packageClass.packageStatuses[2]
                package.timeDelivered = self.truckTime
                self.packagesOnTruck.remove(package)

        # remove the path traveled from the truck's pathGraph edges -> time complexity = O(1)
        self.pathGraph.edgeWeights.pop(travelRoute)

        # keep finding and traveling to the nearest neighbor and dropping off any packages until there are no packages
        # left on the truck. -> the while loop is O(N), the 2 for loops are O(2n), overall time complexity is O(2n^2),
        # or, simplified, is O(N^2); space complexity = O(1)
        while len(self.packagesOnTruck) > 0:
            closestDist = 999.9
            # find nearest neighbor -> time complexity = O(N); space complexity = O(1)
            for edge in self.pathGraph.edgeWeights:
                if self.pathGraph.edgeWeights[edge] < closestDist and self.pathGraph.edgeWeights[edge] != 0.0 and \
                        (self.currentLocation in list(edge)[0]) and list(edge)[1] not in self.locationsVisited:
                    closestDist = self.pathGraph.edgeWeights[edge]
                    travelRoute = edge

            # travel to the location identified, calculate the travel time, add the travel time to the truck's time,
            # add the miles traveled to the truck's milesTraveled variable, and add new stop to the locations
            # visited -> time and space complexity = O(1)
            travelTimeInMinutes = (closestDistToHub / self.avg_speed) * 60
            self.truckTime += datetime.timedelta(minutes=travelTimeInMinutes)
            self.currentLocation = list(travelRoute)[1]
            self.milesTraveled += closestDistToHub
            self.locationsVisited.append(travelRoute[1])

            # iterate through the truck's packages and deliver any packages whose deliveryStreetAddress matches the
            # truck's current location -> time complexity = O(N)
            for package in reversed(self.packagesOnTruck):
                if package.deliveryStreetAddress == self.currentLocation:
                    package.deliveryStatus = packageClass.packageStatuses[2]
                    package.timeDelivered = self.truckTime
                    self.packagesOnTruck.remove(package)

            # remove the path traveled from the truck's pathGraph edges -> time complexity = O(1)
            self.pathGraph.edgeWeights.pop(travelRoute)

        # find the closest path back to the hub -> time complexity = O(N)
        if self.currentLocation != hub:
            closestDistToHub = 999.9
            for edge in self.pathGraph.edgeWeights:
                if self.pathGraph.edgeWeights[edge] < closestDistToHub and self.pathGraph.edgeWeights[edge] != 0.0 and \
                        self.currentLocation in list(edge)[0] and list(edge)[1] == hub:
                    closestDistToHub = self.pathGraph.edgeWeights[edge]
                    travelRoute = edge

        # travel to the location identified, calculate the travel time, add the travel time to the truck's time,
        # add the miles traveled to the truck's milesTraveled variable, and add new stop to the locations
        # visited -> time complexity = O(1)
        travelTimeInMinutes = (closestDistToHub / self.avg_speed) * 60
        self.truckTime += datetime.timedelta(minutes=travelTimeInMinutes)
        self.currentLocation = list(travelRoute)[1]
        self.milesTraveled += closestDistToHub
