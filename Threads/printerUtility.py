import serial
import time

class PrinterUtility():

    def maxLenInEachCol(self,df):
        maxInEachCol = [0]*len(df.columns)
        index = 0
        for col in df:
            maxVal = 0
            for element in df[col]:
                elementLength = len(element)
                if (elementLength > maxVal):
                    maxVal = elementLength
            maxInEachCol[index] = maxVal
            index = index + 1
        return maxInEachCol

    # divide pixels among cols
    def findLenOfEachCol(self, maxColumnLenArray, numOfPixels):
        maxPossibleColumnLen = int(numOfPixels / len(maxColumnLenArray))

        numColsLenGreaterThanMaxPossible = 0
        for x in maxColumnLenArray:
            if x <= maxPossibleColumnLen:
                numOfPixels = numOfPixels - x
            else:
                numColsLenGreaterThanMaxPossible = numColsLenGreaterThanMaxPossible + 1

        availableLen = int(numOfPixels / numColsLenGreaterThanMaxPossible)

        for x in range(0, len(maxColumnLenArray)):
            if maxColumnLenArray[x] > maxPossibleColumnLen:
                maxColumnLenArray[x] = availableLen


    def formatDataFrame(self, df):
        columnLen = self.maxLenInEachCol(df)
        self.findLenOfEachCol(columnLen, 22)
        index = 0
        for col in df:
            val = columnLen[index]
            df[col] = [i[:val] for i in df[col]]
            index += 1

    def printTable(self, data):
        try:
            a = serial.Serial('COM4', 9600)
            time.sleep(0.1)
            a.flush()
            settings = [0x1b, 0x21, 0x01]
            a.write(settings)
            a.write(data.encode())
            a.close()
        except Exception as e:
            print(str(e))



