import time
from fileorganizer import FileOrganizer

import os
from bplustree import BPlusTree,StrSerializer

from catalog import Catalog

import sys

path_to_json=os.path.abspath(os.getcwd())

fileOrg=FileOrganizer()
catalogg=Catalog()

fileOrg.checkIndexStorage()
fileOrg.fillThePrimaryKeys()
inputFile=sys.argv[1]



file=open(inputFile)
lines=file.readlines()

logFile=open("horadrimLog.csv",'a')
outputFile=open("output.text",'a')

for row in lines:
    operation=row.strip()
    operation=operation.strip('\n')
    operationList=operation.split(" ")
    print("ANAN", operationList)
    if operationList[1]=="type":
        #HORADRIM 
        if operationList[0]=="create":
            returnValue=fileOrg.createType(operationList)
            if returnValue=="SUCCESS":
                logFile.write(str(int(time.time()))+","+operation+",success\n")
            elif returnValue=="FAILURE":
                logFile.write(str(int(time.time()))+","+operation+",failure\n")

        elif operationList[0]=="list":
            allTypes=fileOrg.listAllTypes()
            if len(allTypes)==0:
                logFile.write(str(int(time.time()))+","+operation+",failure\n")
                
            else:
                logFile.write(str(int(time.time()))+","+operation+",success\n")
                newAllTypes=allTypes[::2]
                sortedNewAllTypes=sorted(newAllTypes)
                for xtype in sortedNewAllTypes:
                    outputFile.write(str(xtype)+"\n")


        elif operationList[0]=="delete":
            returnValue=fileOrg.deleteType(operationList[2])
            if returnValue=="SUCCESS":
                logFile.write(str(int(time.time()))+","+operation+",success\n")
            elif returnValue=="FAILURE":
                logFile.write(str(int(time.time()))+","+operation+",failure\n")

    elif operationList[1]=="record":
        #HORADRIM MANIPULATION
        if operationList[0]=="create":
            returnValue=fileOrg.insertRecord(operationList)
            if returnValue=="SUCCESS":
                logFile.write(str(int(time.time()))+","+operation+",success\n")

            elif returnValue=="FAILURE":
                logFile.write(str(int(time.time()))+","+operation+",failure\n")

        elif operationList[0]=="delete":

            xtype=operationList[2]
            primaryKey=operationList[3]
            allTypes=catalogg.takeAllTypes()
            if xtype in allTypes:
                bplustree=BPlusTree(filename=os.path.join(path_to_json,"{}.db".format(xtype)),key_size=20, serializer=StrSerializer())
                fullbplustree=BPlusTree(filename=os.path.join(path_to_json,"full{}.db".format(xtype)),order=50, page_size=15000,key_size=20, value_size=300, cache_size=600,serializer=StrSerializer())

                if primaryKey in fileOrg.primaryKeys[xtype]:
                    strRID=(bplustree.get(primaryKey)).decode()
                    recordID=strRID.split(",")
                    node=bplustree._search_in_tree(primaryKey,bplustree._root_node)
                    node.remove_entry(primaryKey)

                    fullstrRID=(fullbplustree.get(primaryKey)).decode()
                    fullrecordID=fullstrRID.split(",")
                    fullnode=fullbplustree._search_in_tree(primaryKey,fullbplustree._root_node)
                    fullnode.remove_entry(primaryKey)





                    fileOrg.deleteRecord(xtype,recordID)
                    logFile.write(str(int(time.time()))+","+operation+",success\n")
                else:
                    logFile.write(str(int(time.time()))+","+operation+",failure\n")


                bplustree.close()
            else:
                logFile.write(str(int(time.time()))+","+operation+",failure\n")



        elif operationList[0]=="update":

            xtype=operationList[2]
            primaryKey=operationList[3]
            allTypes=catalogg.takeAllTypes()
            if xtype in allTypes:
                bplustree=BPlusTree(filename=os.path.join(path_to_json,"{}.db".format(xtype)),key_size=20, serializer=StrSerializer())
                fullbplustree=BPlusTree(filename=os.path.join(path_to_json,"full{}.db".format(xtype)),order=50, page_size=15000,key_size=20, value_size=300, cache_size=600,serializer=StrSerializer())

                if primaryKey in fileOrg.primaryKeys[xtype]:
                    newFields=[]
                    for i in range(4,len(operationList)):
                        newFields.append(operationList[i])

                    strRID=(bplustree.get(primaryKey)).decode()
                    recordID=strRID.split(",")

                    ###UPDATE FULLBPLUSTREE
                    strNewFields=','.join(newFields)

                    fullbplustree.__setitem__(primaryKey,strNewFields.encode())
                    strRecord=(fullbplustree.get(primaryKey)).decode()
                    
                    ###


                    fileOrg.updateRecord(xtype,recordID,newFields)
                    bplustree.close()
                    fullbplustree.close()
                    logFile.write(str(int(time.time()))+","+operation+",success\n")
                else:
                    logFile.write(str(int(time.time()))+","+operation+",failure\n")
            else:
                logFile.write(str(int(time.time()))+","+operation+",failure\n")



        elif operationList[0]=="search":
            xtype=operationList[2]
            primaryKey=operationList[3]
            allTypes=catalogg.takeAllTypes()

            if xtype in allTypes:
                fullbplustree=BPlusTree(filename=os.path.join(path_to_json,"full{}.db".format(xtype)),order=50, page_size=15000,key_size=20, value_size=300, cache_size=600,serializer=StrSerializer())
                
                if primaryKey in fileOrg.primaryKeys[xtype]:
                    strRecord=(fullbplustree.get(primaryKey)).decode()
                    recordData=strRecord.split(",")
                    fieldList=' '.join(recordData)
                    fullbplustree.close()
        
                    outputFile.write(fieldList+"\n")
                    logFile.write(str(int(time.time()))+","+operation+",success\n")
                else:
                    logFile.write(str(int(time.time()))+","+operation+",failure\n")
            else:
                logFile.write(str(int(time.time()))+","+operation+",failure\n")

            

        elif operationList[0]=="list":

            xtype=operationList[2]
           
            allTypes=catalogg.takeAllTypes()
            pKeyType=catalogg.takeFromAttributes(xtype,True)
            pKeyNo=int(catalogg.takeFromPrimaryKeys(xtype))
            pKeyIndex=pKeyNo-1

            recList=""
            if xtype in allTypes:
                fullbplustree=BPlusTree(filename=os.path.join(path_to_json,"full{}.db".format(xtype)),order=50, page_size=15000,key_size=20, value_size=300, cache_size=600,serializer=StrSerializer())
                outputs=[]
                check=False
                for key,record in fullbplustree.items():
                    if key in fileOrg.primaryKeys[xtype]:
                        check=True
                        strRecord=record.decode()
                        if(strRecord==""):
                            logFile.write(str(int(time.time()))+" "+operation+",failure\n")
                            continue
                        recordData=strRecord.split(",")
                        if pKeyType=="int":
                            recordData[pKeyIndex]=int(recordData[pKeyIndex])

                        outputs.append(recordData)
                    
                
                

                fullbplustree.close()
                if check:
                    sortedOutputs=sorted(outputs,key=lambda l:l[pKeyIndex])
                    for output in sortedOutputs:
                        strOutput=[str(i) for i in output]
                        fieldList=' '.join(strOutput)
                        outputFile.write(fieldList+"\n")


                    logFile.write(str(int(time.time()))+","+operation+",success\n")
                else:
                    logFile.write(str(int(time.time()))+","+operation+",failure\n")
               
            else:
                logFile.write(str(int(time.time()))+","+operation+",failure\n")

        elif operationList[0]=="filter":
            xtype=operationList[2]
            condition=operationList[3]
            smallCondition=condition.split("<")
            equalCondition=condition.split("=")
            bigCondition=condition.split(">")


            lastCondition=None
            if len(bigCondition)==2:
                lastCondition=bigCondition
                op=">"
            elif len(equalCondition)==2:
                lastCondition=equalCondition
                op="="

            elif len(smallCondition)==2:
                lastCondition=smallCondition
                op="<"

            prim=lastCondition[0]
            comp=lastCondition[1]

                
            allTypes=catalogg.takeAllTypes()

            pKeyType=catalogg.takeFromAttributes(xtype,True)
            pKeyNo=int(catalogg.takeFromPrimaryKeys(xtype))
            pKeyIndex=pKeyNo-1

            intCheck=False
            if pKeyType=="int":
                intCheck=True
            

            if xtype in allTypes:
                fullbplustree=BPlusTree(filename=os.path.join(path_to_json,"full{}.db".format(xtype)),order=50, page_size=15000,key_size=20, value_size=300, cache_size=600,serializer=StrSerializer())
                check=False
                outputs=[]

                if op=="<":
                    for key, value in fullbplustree.items(): 
                        if key in fileOrg.primaryKeys[xtype]:
                            check=True
                            tempKey=key
                            tempComp=comp
                            if intCheck:
                                tempKey=int(key)
                                tempComp=int(comp)
                            if tempKey<tempComp:
                                strRecord=value.decode()
                                recordData=strRecord.split(",")
                                if intCheck:
                                    recordData[pKeyIndex]=int(recordData[pKeyIndex])

                                outputs.append(recordData)

                            

                elif op==">":
                    for key, value in fullbplustree.items():
                        if key in fileOrg.primaryKeys[xtype]:
                            check=True
                            tempKey=key
                            tempComp=comp
                            if intCheck:
                                tempKey=int(key)
                                tempComp=int(comp)
                            if tempKey>tempComp:
                                strRecord=value.decode()
                                recordData=strRecord.split(",")
                                if intCheck:
                                    recordData[pKeyIndex]=int(recordData[pKeyIndex])

                                outputs.append(recordData)
                            
                elif op=="=":
                    for key, value in fullbplustree.items():
                        if key in fileOrg.primaryKeys[xtype]:
                            check=True
                            tempKey=key
                            tempComp=comp
                            if intCheck:
                                tempKey=int(key)
                                tempComp=int(comp)
                            if tempKey==tempComp:
                                strRecord=value.decode()
                                recordData=strRecord.split(",")
                                if intCheck:
                                    recordData[pKeyIndex]=int(recordData[pKeyIndex])

                                outputs.append(recordData)

                if check:
                    sortedOutputs=sorted(outputs,key=lambda l:l[pKeyIndex])
                    for output in sortedOutputs:
                        strOutput=[str(i) for i in output]
                        fieldList=' '.join(strOutput)
                        outputFile.write(fieldList+"\n")
                    logFile.write(str(int(time.time()))+","+operation+",success\n")
                else:
                    logFile.write(str(int(time.time()))+","+operation+",failure\n")
                fullbplustree.close()
               
            else:
                logFile.write(str(int(time.time()))+","+operation+",failure\n")



