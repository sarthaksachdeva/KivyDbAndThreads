from pymongo import MongoClient
import datetime


class MongoDbHelper:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client.device_users_db
        self.m_userCollection = db.users
        self.m_customerIdCollection = db.customerId
        self.m_customerCollection = db.customers
        self.m_customerMilkDataCollection = db.customersMilkData

        firstUser = {
            "name": "admin",
            "password": "admin",
            "role": "admin"
        }
        # add first user by default
        if (self.m_userCollection.find(firstUser).count() == 0):
            self.m_userCollection.insert_one(firstUser)
        self.m_currentDeviceUser = {
            "name": "",
            "role": "local"
        }

        # make sure user id is unique
        self.m_customerIdCollection.ensure_index(("id"), unique=True)
        # add default customer ID
        defaultCustomerId = 0
        if (self.m_customerIdCollection.find({}).count() == 0):
            self.m_customerIdCollection.insert_one({"id": defaultCustomerId})

    ###################################################################################################################
    # CUSTOMER ID DB
    ###################################################################################################################

    '''
    update customer id in db
    '''

    def updateCustomerId(self):
        entry = self.m_customerIdCollection.find({})
        if (entry.count() == 1):
            entryInDb = entry[0]
            try:
                self.m_customerIdCollection.update_one(
                    {"_id": entryInDb["_id"]},
                    {
                        "$set": {
                            "id": entryInDb["id"] + 1
                        }
                    }
                )
                print("customer ID updated successfully")

            except Exception as e:
                print(str(e))

    '''
    get customer id from db
    '''

    def getCustomerId(self):
        entry = self.m_customerIdCollection.find({})
        if (entry.count() == 1):
            entryInDb = entry[0]
            return entryInDb["id"]

    ###################################################################################################################
    # DEVICE USER  DB
    ###################################################################################################################
    '''
    insert entry in device users db
    '''

    def insertDeviceUserInDb(self, entry):
        retVal = False  # if name  is not admin
        if (self.checkIfDeviceUserSchema(entry)):
            self.m_userCollection.insert_one(entry)
            retVal = True
        return retVal

    '''
    sets current device user
    '''

    def setCurrentDeviceUser(self, user):
        if (self.checkIfDeviceUserSchema(user)):
            self.m_currentDeviceUser["name"] = user["name"]
            self.m_currentDeviceUser["role"] = user["role"]

    '''
    gets current device user
    '''

    def getCurrentDeviceUser(self):
        return self.m_currentDeviceUser

    '''
    get all device user
    '''

    def findAllDeviceUsers(self):
        return self.m_userCollection.find({})

    '''
    check if user exists in db or not given name and password.
    '''

    def findDeviceUser(self, name, password):
        return self.m_userCollection.find({"name": name, "password": password})

    '''
    checks if entry is of type user schema
       {name:,
        password:,
        role:}
    '''

    def checkIfDeviceUserSchema(self, entry):
        retVal = False
        # if a single entry of type dictionary
        if (isinstance(entry, dict)):
            # if correct schema
            if (("name" in entry.keys()) and ("password" in entry.keys()) and ("role" in entry.keys())):
                retVal = True
            else:
                print("not of correct schema")
        else:
            print("not of type a single dictionary object")
        return retVal

    ###################################################################################################################
    # CUSTOMER  DB
    ###################################################################################################################
    '''
    checks if entry is of type new Customer schema
       {id:,
        name:,
        localName:,
        address:,
        telephone}
    '''

    def checkIfNewCustomerSchema(self, entry):
        retVal = False
        # if a single entry of type dictionary
        if (isinstance(entry, dict)):
            # if correct schema
            if (("id" in entry.keys()) and ("name" in entry.keys()) and ("localName" in entry.keys()) and (
                        "address" in entry.keys()) and ("telephone" in entry.keys())):
                retVal = True
            else:
                print("not of correct schema")
        else:
            print("not of type a single dictionary object")
        return retVal

    '''
    add a new customer in customer database
    '''

    def insertNewCustomerInDb(self, entry):
        retVal = False
        # check if schema is correct
        if (self.checkIfNewCustomerSchema(entry)):
            self.m_customerCollection.insert_one(entry)
            retVal = True
        return retVal

    '''
    find a customer with name, address, telephone and local name to check if the user data already exists
    '''

    def findCustomerWithoutId(self, entry):
        return self.m_customerCollection.find(entry)

    '''
    find a customer using CUSTOMER  ID
    '''

    def findCustomerUsingId(self, id):
        entry = self.m_customerCollection.find({"id": id})
        if (entry.count() == 1):
            return entry[0]
        else:
            return None

    '''
    get all customers in the customer database
    '''

    def getAllCustomers(self):
        return self.m_customerCollection.find({})

    '''
    get all customers in the customer database, fields - name, local name, telephone, address, id
    '''

    def getAllCustomersFields(self):
        return self.m_customerCollection.find({}, {"id": 1, "name": 1, "localName": 1, "address": 1, "telephone": 1,
                                                   "_id": 0})

    '''
    find a customer by id and edit it's property and set to the value given
    '''

    def updateCustomerProperty(self, id, property, value):

        entryInDb = self.findCustomerUsingId(id)
        if (entryInDb is not None):
            try:
                self.m_customerCollection.update_one(
                    {"_id": entryInDb["_id"]},  # CONDITION
                    {
                        "$set": {
                            property: value  # PROPERTY
                        }
                    }
                )
                print("customer " + property + " updated successfully")
            except Exception as e:
                print(str(e))



            ###################################################################################################################
            # CUSTOMER MILK DATA DB
            ###################################################################################################################

    def checkCustomerMilkCollectionSchema(self, entry):
        retVal = False
        # if a single entry of type dictionary
        if (isinstance(entry, dict)):
            # if correct schema
            if (("id" in entry.keys()) and ("mode" in entry.keys()) and ("session" in entry.keys()) and (
                        "milktype" in entry.keys()) and ("tariff" in entry.keys()) and ("weight" in entry.keys()) and (
                        "fat" in entry.keys()) and ("amount" in entry.keys()) and ("datetime" in entry.keys())):
                retVal = True
            else:
                print("not of correct schema")
        else:
            print("not of type a single dictionary object")
        return retVal

    def insertEntryInCustomerMilkCollectionDb(self, entry):
        retVal = False
        id = None
        # check if schema is correct
        if (self.checkCustomerMilkCollectionSchema(entry)):
            id = self.m_customerMilkDataCollection.insert_one(entry)
            retVal = True
        return retVal, id

    def getAllCustomersData(self):
        return self.m_customerMilkDataCollection.find({})
