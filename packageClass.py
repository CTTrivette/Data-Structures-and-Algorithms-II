#Christian Trivette, Student ID: 001307104
#list detailing the available options for the package's status -> time complexity = O(1); space complexity = O(N)
packageStatuses = ["AT HUB", "EN ROUTE", "DELIVERED"]

class Package:
    # class constructor -> space complexity = O(1)
    def __init__(self):
        self.deliveryStreetAddress = ""  # example: 123 Main Street
        self.deliveryCity = ""
        self.deliveryState = ""
        self.deliveryZip = ""
        self.onTruckNumber = 0  # initial truck - 0 represents the hub
        self.deliveryStatus = packageStatuses[0]  # based off of list for delivery status
        self.isDelayed = False  # checks if package is delayed from the plane, if so, then package will be loaded
        # onto truck 3 when it arrives at the hub and will await until next driver can take truck
        self.incorrectAddress = False  # checks if package has wrong address, if so, won't be loaded and will be
        # loaded onto truck after time that address will be corrected
        self.packageID = 0
        self.deliveryDeadline = None  # zero indicates by end of day. Any other int will represent the actual time
        # that it has to be delivered by in military time
        self.packageWeight = 0
        self.timeDelivered = None  # 0000 is default, will update whenever package is delivered
        self.specialNotes = ""
        self.timeLeftHub = None

    def __hash__(self):
        # magic method that hashes the package's packageID
        return hash(self.packageID)

    def __eq__(self, key):
        # magic method that states that the packages' packageID is equivalent to the variable named key
        return self.packageID == key
