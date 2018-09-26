import threading
import pandas as pd
from kivyDemos.kivyHomeMenuGit.Threads.printerUtility import PrinterUtility

from kivyDemos.kivyHomeMenuGit.DataBaseUtility.dataBaseType import dataBaseType
from tabulate import tabulate

class PrinterThread(threading.Thread):
    def __init__(self, messageQueue, eventGroup, mongoDbUtility):
        super(PrinterThread, self).__init__()
        self.m_messageQueue = messageQueue
        self.m_event = eventGroup
        self.m_mongoDbUtility = mongoDbUtility

    def printQueueData(self):
        retVal = 0
        dbType = self.m_messageQueue.get()
        params = self.m_messageQueue.get()
        data = self.checkDbAndGetData(dbType, params)
        if(data is not None):
            self.printData(data)
        if (dbType == "done" or params == "done"):
            retVal = 1
        return retVal

    def checkDbAndGetData(self,dbytype, params):
        print("params = ", params)
        data = None
        if(dbytype == dataBaseType["DeviceUserDb"]):
            data = self.m_mongoDbUtility.findAllDeviceUsers()

        if(dbytype == dataBaseType["CustomerDb"]):
            data = self.m_mongoDbUtility.getAllCustomersFields()

        if(dbytype == dataBaseType["CustomerDataDb"]):
            data = self.m_mongoDbUtility.getAllCustomersData()

        return data


    def printData(self, data):
        # df = pd.DataFrame(data,c)
        columnArr = []
        for val in data[0]:
            columnArr.append(str(val))

        df = pd.DataFrame(list(data), columns=columnArr)
        printerUtility = PrinterUtility()
        printerUtility.formatDataFrame(df)
        printerUtility.printTable(tabulate(df, showindex=False, headers=df.columns))
        print(tabulate(df, showindex=False, headers=df.columns))

    def run(self):
        print("Printer Thread started")
        while (1):
            # returns true when wait is over except in case of timeout, by default timeout = None
            self.m_event.wait()
            self.m_event.clear()
            print("**********************************************************************")
            ret = self.printQueueData()
            if (ret):
                break

        print("Thread 1 done")
