from kivyDemos.kivyHomeMenuGit.DataBaseUtility.AuthenticationUtility import Authentication
import datetime


class CustomerDataUtility(Authentication):
    def __init__(self, dbHelper):
        super(CustomerDataUtility, self).__init__(dbHelper)
        self.m_dbHelper = dbHelper

    def basicNonEmptyCheckForNewCustomer(self, id, name, localName, address, telephone, calleeWidget):
        text = ""
        retVal = True

        if (len(id) <= 0):
            text = text + "id is empty,"
            retVal = False
        if (len(name) <= 0):
            text = text + "name is empty,"
            retVal = False
        if (len(localName) <= 0):
            text = text + "localName is empty,"
            retVal = False
        if (len(address) <= 0):
            text = text + "address is empty,"
            retVal = False
        if (len(telephone) <= 0):
            text = text + "telephone is empty,"
            retVal = False

        if (retVal == False):
            print(text)
            self.createPopUp(text, calleeWidget)
        return retVal

    def getNumberOfCustomers(self):
        return self.m_dbHelper.getCustomerId()


    def addNewCustomer(self, idWidget, nameWidget, localNameWidget, addressWidget, telephoneWidget, calleeWidget):
        retVal = False
        #ensure all entries are filled
        if (
        self.basicNonEmptyCheckForNewCustomer(idWidget.text, nameWidget.text, localNameWidget.text, addressWidget.text,
                                              telephoneWidget.text, calleeWidget)):
            entry = {
                "name": nameWidget.text,
                "localName": localNameWidget.text,
                "address": addressWidget.text,
                "telephone": telephoneWidget.text,
            }
            #ensure same customer doesnt exist with the given details
            foundCustomers = self.m_dbHelper.findCustomerWithoutId(entry)
            if(foundCustomers.count() == 0):
                entry["id"] = idWidget.text
                #if insertion is successful
                if(self.m_dbHelper.insertNewCustomerInDb(entry)):
                    self.m_dbHelper.updateCustomerId()
                    text = "new user add successfully"
                    print(text)
                    self.createPopUp(text, calleeWidget)
                    #clear widgets
                    self.clearAddCustomerData(nameWidget, localNameWidget, addressWidget, telephoneWidget)
                    retVal = True

            else:
                text = "customer already exists"
                print(text)
                self.createPopUp(text, calleeWidget)

        return retVal


    def clearAddCustomerData(self, nameWidget, localNameWidget, addressWidget, telephoneWidget):
        nameWidget.text = ""
        localNameWidget.text = ""
        addressWidget.text = ""
        telephoneWidget.text = ""
        return True

    def getAllCustomers(self):
        return self.m_dbHelper.getAllCustomers()

    def getCustomerAndCustomerNameById(self, id):
        customer = self.m_dbHelper.findCustomerUsingId(id)
        if (customer is not None):
            return customer,customer["name"]
        else:
            return None,""

    def updateCustomerDbProperty(self, id, property, value):
        self.m_dbHelper.updateCustomerProperty(id, property, value)

    def basicNonEmptyCheckForCustomerMilkCollectionData(self, id, name, mode, session, milkType, tariff, weight, fat,
                                                        amount, calleeWidget):
        text = ""
        retVal = True
        if (len(name) <= 0):
            text = "enter a valid ID"
            retVal = False
            print(text)
            self.createPopUp(text, calleeWidget)
        else:
            if (len(id) <= 0):
                text = text + "id is empty,"
                retVal = False
            if (len(mode) <= 0):
                text = text + "mode is empty,"
                retVal = False
            if (len(mode) <= 0):
                text = text + "localName is empty,"
                retVal = False
            if (len(session) <= 0):
                text = text + "session is empty,"
                retVal = False
            if (len(milkType) <= 0):
                text = text + "milkType is empty,"
                retVal = False
            if (len(tariff) <= 0):
                text = text + "tariff is empty,"
                retVal = False
            if (len(weight) <= 0):
                text = text + "weight is empty,"
                retVal = False
            if (len(fat) <= 0):
                text = text + "fat is empty,"
                retVal = False
            if (len(amount) <= 0):
                text = text + "amount is empty,"
                retVal = False

            if (retVal == False):
                print(text)
                self.createPopUp(text, calleeWidget)
        return retVal

    # TODO add date time, although why is date time needed from outside while taking data
    def addCustomerMilkCollectionData(self, id, name, mode, session, milkType, tariff, weight, fat,
                                      amount, calleeWidget):
        retVal = False
        dateTime = datetime.datetime.now()
        if (
                self.basicNonEmptyCheckForCustomerMilkCollectionData(id.text, name.text, mode.text, session.text,
                                                                     milkType.text,
                                                                     tariff.text,
                                                                     weight.text, fat.text, amount.text,
                                                                     calleeWidget)):

            entry = {
                "id": id.text,
                "mode": mode.text,
                "session": session.text,
                "milktype": milkType.text,
                "tariff": tariff.text,
                "weight": weight.text,
                "fat": fat.text,
                "amount": amount.text,
                "datetime": dateTime
            }
            ret, milkCollDataId = self.m_dbHelper.insertEntryInCustomerMilkCollectionDb(entry)
            print(milkCollDataId.inserted_id)
            if(ret and (milkCollDataId is not None)):
                customer,_ = self.getCustomerAndCustomerNameById(id.text)
                if (customer is not None and "milkCollDataArray" in customer):
                    customer["milkCollDataArray"].append(milkCollDataId.inserted_id)
                elif("milkCollDataArray" not in customer):
                    customer["milkCollDataArray"] = [milkCollDataId.inserted_id]
                print(customer)
                self.updateCustomerDbProperty(id.text, "milkCollDataArray", customer["milkCollDataArray"])
                self.clearCustomerMilkCollectionData(id, name, milkType, weight, fat, amount)
                retVal = True
                return retVal

    def clearCustomerMilkCollectionData(self, id, name, milkType, weight, fat, amount):

        id.text = ""
        name.text = ""
        milkType.text = ""
        weight.text = ""
        fat.text = ""
        amount.text = ""
        return True



