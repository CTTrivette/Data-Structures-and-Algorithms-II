#Christian Trivette, Student ID: 001307104
import datetime
import hashtable
import truck
import packageClass
import csv

#open the WGUPS Package File CSV and read the CSV file into a 2D array -> Time complexity = O(N^2);
# Space Complexity = O(N^2)
with open('WGUPS Package File CSV.csv', newline='') as packageCSV:
    packageTable = [row for row in csv.reader(packageCSV, delimiter=',')]

#open the Horizontal Headers of the Distance CSV and read them into a list -> Time complexity = O(N);
# space complexity = O(N)
with open('Distance Table Horizontal Headers CSV.csv', newline='') as horizontalCSV:
    horizontalHeaders = []
    reader = csv.reader(horizontalCSV, delimiter=',')
    for entry in reader:
        horizontalHeaders.append(entry)

#open the Vertical Headers of the Distance CSV and read them into a list -> Time complexity = O(N);
# space complexity = O(N)
with open('Distance Table Vertical Headers CSV.csv', newline='') as verticalCSV:
    verticalHeaders = []
    reader = csv.reader(verticalCSV, delimiter=',')
    for entry in reader:
        verticalHeaders.append(entry)

#Create two empty lists. packageDictList will hold dictionary objects that contain a package's information.
#packageObjectList is a list that will hold package objects, whose information is populated from packageDictList ->
# space complexity = O(N)
packageDictList = []
packageObjectList = []

#populate packageDistList with dictionary objects meant to represent packages. Also, populate packageObjectList with
#empty package objects -> time complexity = O(N)
for i in range(len(packageTable)):
    packageInfo = dict(ID=int(packageTable[i][0]), streetAddress=packageTable[i][1], city=packageTable[i][2],
                       state=packageTable[i][3], zip=packageTable[i][4], deadline=packageTable[i][5],
                       weight=packageTable[i][6], notes=packageTable[i][7])
    packageDictList.append(packageInfo)
    packageObjectList.append(packageClass.Package())

#create the HashTable object -> time complexity = O(1); space complexity = O(N^2)
packageHashTable = hashtable.chainingHashTable()

#Iterate through each empty package object in packageObjectList and populate the package's information -> time
#complexity = O(N)
for i in range(len(packageDictList)):
    packageObjectList[i].packageID = packageDictList[i]['ID']
    packageObjectList[i].deliveryStreetAddress = packageDictList[i]['streetAddress'].replace('South', 'S').replace('North', 'N')\
        .replace('West', 'W').replace('East', 'E')
    packageObjectList[i].deliveryCity = packageDictList[i]['city']
    packageObjectList[i].deliveryState = packageDictList[i]['state']
    packageObjectList[i].deliveryZip = packageDictList[i]['zip']
    if packageDictList[i]['deadline'] == 'EOD':
        packageObjectList[i].deliveryDeadline = datetime.datetime.strptime("11:59:59 PM", "%I:%M:%S %p")
    else:
        packageObjectList[i].deliveryDeadline = datetime.datetime.strptime(packageDictList[i]['deadline'], "%I:%M %p")
    packageObjectList[i].packageWeight = packageDictList[i]['weight']
    packageObjectList[i].specialNotes = packageDictList[i]['notes']

    #insert the new package into the packageHashTable -> O(1)
    packageHashTable.insertPackage(packageObjectList[i])

#Create truck objects and assign them their truck number. Truck 2 will leave at 9:05 AM -> time complexity = O(1); space
#complexity = O(N) since each truck constructor creates two separate lists as a truck attribute
truck1 = truck.Truck()
truck1.truckNum = 1
truck2 = truck.Truck()
truck2.truckNum = 2
truck2.departureTime = datetime.datetime.strptime("09:05:00 AM", "%I:%M:%S %p")
truck3 = truck.Truck()
truck3.truckNum = 3

#Manually load the packages onto truck 1 ->  Time Complexity = O(1); Space Complexity = O(N)
truck1.packagesOnTruck = [
    packageHashTable.search(14),
    packageHashTable.search(15),
    packageHashTable.search(16),
    packageHashTable.search(19),
    packageHashTable.search(20),
    packageHashTable.search(13),
    packageHashTable.search(37),
    packageHashTable.search(29),
    packageHashTable.search(30),
    packageHashTable.search(21),
    packageHashTable.search(23),
    packageHashTable.search(40),
    packageHashTable.search(31),
]

#Build truck 1's route and travel to each destination, dropping off its' packages -> overall time-complexity for this
#function call is O(N^2); space complexity = O(N^2)
truck1.buildRouteAndTravel()

#Manually load the packages onto truck 2 ->  Time Complexity = O(1); Space Complexity = O(N)
truck2.packagesOnTruck = [
    packageHashTable.search(1),
    packageHashTable.search(3),
    packageHashTable.search(6),
    packageHashTable.search(18),
    packageHashTable.search(25),
    packageHashTable.search(28),
    packageHashTable.search(32),
    packageHashTable.search(34),
    packageHashTable.search(35),
    packageHashTable.search(36),
    packageHashTable.search(38),
    packageHashTable.search(39),
]

#Build truck 2's route and travel to each destination, dropping off its' packages -> overall time-complexity for this
#function call is O(N^2); space complexity = O(N^2)
truck2.buildRouteAndTravel()

#Manually load the packages onto truck 3 -> Time Complexity = O(1); Space Complexity = O(N)
truck3.packagesOnTruck = [
    packageHashTable.search(26),
    packageHashTable.search(24),
    packageHashTable.search(22),
    packageHashTable.search(2),
    packageHashTable.search(4),
    packageHashTable.search(5),
    packageHashTable.search(7),
    packageHashTable.search(8),
    packageHashTable.search(9),
    packageHashTable.search(10),
    packageHashTable.search(11),
    packageHashTable.search(12),
    packageHashTable.search(17),
    packageHashTable.search(27),
    packageHashTable.search(33),
]

#Truck 3 cannot leave until truck 1's driver is back, so have to ensure that truck 1 is at the hub. Also,
#build truck 3's route and travel to each destination, dropping off its' packages -> overall time-complexity for this
#is O(N^2); space-complexity = O(N^2)
if truck1.currentLocation == "4001 S 700 E":
    truck3.departureTime = truck1.truckTime
    truck3.truckTime = truck1.truckTime
    truck3.buildRouteAndTravel()

#Run the program
run = True
while run == True:
    print("Welcome to the WGUPS Delivery Tracker")
    menuChoice = input("Enter 1 to check status of one package. Enter 2 to check status of all packages. "
                       "Enter 3 to check the distance all the delivery trucks traveled. Enter 4 to quit. \n>>")
    if menuChoice == str(1):
        packageQuery = input("Enter the packageID of the package you are searching for: ")
        packageTimeQuery = datetime.datetime.strptime(input("Enter the time formatted as HH:MM AM/PM: "), '%I:%M %p')
        print('-----------------------------------------------')
        wantedPackage = packageHashTable.search(int(packageQuery))
        print("Package ID Number:", wantedPackage.packageID)
        print("Package Weight (in Kg):", wantedPackage.packageWeight)
        print("Package Delivery Street Address:", wantedPackage.deliveryStreetAddress)
        print("Package Delivery City:", wantedPackage.deliveryCity)
        print("Package Delivery State:", wantedPackage.deliveryState)
        print("Package Delivery Zip Code:", wantedPackage.deliveryZip)
        print("Package Delivery Deadline:", wantedPackage.deliveryDeadline.time().strftime('%I:%M %p'))
        if packageTimeQuery <= wantedPackage.timeLeftHub:
            print("Package Delivery Status:", packageClass.packageStatuses[0])
        elif wantedPackage.timeLeftHub < packageTimeQuery < wantedPackage.timeDelivered:
            print("Package Delivery Status:", packageClass.packageStatuses[1])
        else:
            print("Package Delivery Status:", packageClass.packageStatuses[2])
            print("Package Delivery Time:", wantedPackage.timeDelivered.time().strftime('%I:%M %p'))
        print('-----------------------------------------------')

    elif menuChoice == str(2):
        userTime = datetime.datetime.strptime(input("Enter the time formatted as HH:MM AM/PM: "), '%I:%M %p')
        print('-----------------------------------------------')
        for package in packageObjectList:
            if (userTime <= packageHashTable.search(package).timeLeftHub):
                print("Package ID:", package.packageID, "Package Status:", packageClass.packageStatuses[0])
            elif (userTime > package.timeLeftHub and userTime < package.timeDelivered):
                print("Package ID:", package.packageID, "Package Status:", packageClass.packageStatuses[1])
            else:
                print("Package ID:", package.packageID, "Package Status:", packageClass.packageStatuses[2], end=' ')
                print("Delivery Time:", package.timeDelivered.time().strftime('%I:%M %p'))
        print('-----------------------------------------------')

    elif menuChoice == str(3):
        print("Truck 1 travelled:", str(round(truck1.milesTraveled, 2)), "miles.")
        print("Truck 2 travelled:", str(round(truck2.milesTraveled, 2)), "miles.")
        print("Truck 3 travelled:", str(round(truck3.milesTraveled, 2)), "miles.")
        print("Total distance traveled:", str(round(truck1.milesTraveled + truck2.milesTraveled + \
                                                    truck3.milesTraveled, 2)),
              "miles.")
    elif menuChoice == str(4):
        run = False
    else:
        print("Incorrect selection, please try again.")



