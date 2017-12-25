import csv
from os import listdir

dataCRAN = '/home/minh/PycharmProjects/Ensemble/PythonESN/data_backup/cran_10_12'
dataEDGAR = '/home/minh/PycharmProjects/Ensemble/PythonESN/data_backup/edgar_10_12'
dataKyoto = '/home/minh/PycharmProjects/Ensemble/PythonESN/data_backup/kyoto_10_12'

realCRAN = '/home/minh/PycharmProjects/Ensemble/processed/cran_10_12'
realEDGAR = '/home/minh/PycharmProjects/Ensemble/processed/edgar_10_12'
realKyoto = '/home/minh/PycharmProjects/Ensemble/processed/kyoto_10_12'

outCRAN = '/home/minh/PycharmProjects/Ensemble/final_results/cran_10_12.csv'
outEDGAR = '/home/minh/PycharmProjects/Ensemble/final_results/edgar_10_12.csv'
outKyoto = '/home/minh/PycharmProjects/Ensemble/final_results/kyoto_10_12.csv'

esnCRAN = '/home/minh/PycharmProjects/Ensemble/PythonESN/predictions_backup/cran_10_12_enet_identity_mae/predictions_cran_historical_10_12_enet_identity_'
esnEDGAR = '/home/minh/PycharmProjects/Ensemble/PythonESN/predictions_backup/edgar_10_12_enet_identity_mae/predictions_edgar_historical_10_12_enet_identity_'
esnKyoto = '/home/minh/PycharmProjects/Ensemble/PythonESN/predictions_backup/kyoto_10_12_enet_identity_mae/predictions_kyoto_historical_10_12_enet_identity_'

ensembleCRAN = '/home/minh/PycharmProjects/Ensemble/ensemble_algorithms/results/cran_10_12/'
ensembleEDGAR = '/home/minh/PycharmProjects/Ensemble/ensemble_algorithms/results/edgar_10_12/'
ensembleKyoto = '/home/minh/PycharmProjects/Ensemble/ensemble_algorithms/results/kyoto_10_12/'

ensembleNames = ['Average','CrossValidation','GBM','GA',
                 'NaiveBaggingRegression','ArBaggingRegression','ArmaBaggingRegression','ArimaBaggingRegression','EtsBaggingRegression']
dataList = [dataCRAN,dataEDGAR,dataKyoto]
realList = [realCRAN,realEDGAR,realKyoto]
esnList = [esnCRAN,esnEDGAR,esnKyoto]
ensembleList = [ensembleCRAN,ensembleEDGAR,ensembleKyoto]
outList = [outCRAN,outEDGAR,outKyoto]

testingSize = 240
repeatSize = 5

def readData(dataFile,column,ignores):
    dataList = []
    count = 0
    with open(dataFile,'r') as f:
        for line in f:
            count+=1
            if count>ignores:
                lineParts = line.split(',')
                if lineParts[column][-1:]=='\n':
                    dataList.append(int(float(lineParts[column][:-1])))
                else:
                    dataList.append(int(float(lineParts[column])))
    dataList = dataList[-240:]
    for i in range(len(dataList)):
        dataList[i] = str(dataList[i])
    return dataList

def readReal(dataFile,column,ignores):
    results = readData(dataFile,column,ignores)
    results.insert(0,'real')
    return results

def readComponents(dataFile,ignores):
    naive = readData(dataFile,0,ignores)
    naive.insert(0,'naive')
    ar = readData(dataFile,1,ignores)
    ar.insert(0,'ar')
    arma = readData(dataFile,2,ignores)
    arma.insert(0,'arma')
    arima = readData(dataFile,3,ignores)
    arima.insert(0,'arima')
    ets = readData(dataFile,4,ignores)
    ets.insert(0,'ets')
    return (naive,ar,arma,arima,ets)

def readESN(dataPath):
    results = []
    for i in range(testingSize):
        results.append(0)
    for i in range(1,repeatSize+1):
        dataFile = dataPath + str(i)
        with open(dataFile,'r') as f:
            count=0
            for line in f:
                results[count]+=float(line)
                count+=1
    for i in range(len(results)):
        if results[i]<0:
            print('problem with negative value in ESN')
        results[i]=int(round(results[i]/repeatSize))
    for i in range(len(results)):
        results[i]=str(results[i])
    results.insert(0,'esn')
    return results

def readEnsemble(dataPath):
    results = []
    for name in ensembleNames:
        fileList = []
        for fileName in listdir(dataPath):
            nameParts = fileName.split('_')
            if nameParts[1]==name:
                fileList.append(dataPath+fileName)
        fileList=sorted(fileList)
        results.append(doEnsemble(fileList))
    for i in range(len(results)):
        results[i].insert(0,ensembleNames[i])
    return results

def doEnsemble(fileList):
    resultList = [0]*testingSize
    for fileName in fileList:
        with open(fileName,'r') as f:
            reader = csv.reader(f)
            count = 0
            for line in reader:
                count+=1
                if count>1:
                    resultList[count-2]+=float(line[1])
    for i in range(len(resultList)):
        resultList[i]/=len(fileList)
    for i in range(len(resultList)):
        resultList[i] = int(round(resultList[i]))
        resultList[i]=str(resultList[i])
    return resultList

def main():
    for i in range(len(dataList)):
        real = readReal(dataList[i],-1,1)
        naive,ar,arma,arima,ets = readComponents(dataList[i],1)
        esn = readESN(esnList[i])
        results = readEnsemble(ensembleList[i])

        average = results[0]
        crossval = results[1]
        gbm = results[2]
        ga = results[3]
        naivebag = results[4]
        arbag = results[5]
        armabag = results[6]
        arimabag = results[7]
        etsbag = results[8]

        with open(outList[i],'w') as f:
            for j in range(len(real)):
                #f.write(real[j] + ',' + naive[j] + ',' + ar[j] + ',' + arma[j] + ',' + arima[j] + ',' + ets[j] + ',' + esn[j])
                f.write(real[j] + ',' + average[j] + ',' + crossval[j] + ',' + gbm[j] + ',' + ga[j] + ',' +
                        naivebag[j] + ',' + arbag[j] + ',' + armabag[j] + ',' + arimabag[j] + ',' + etsbag[j] + ',' + esn[j])
                f.write('\n')

if __name__ == "__main__":
    main()