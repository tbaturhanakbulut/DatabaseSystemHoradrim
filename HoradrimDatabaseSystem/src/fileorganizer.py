from curses.ascii import isdigit
from posixpath import split
from page import Page
from record import Record
import os
from catalog import Catalog



from bplustree import BPlusTree,StrSerializer

path_to_json=os.path.abspath(os.getcwd())
fileNos=[]
for pos_json in os.listdir(path_to_json):
    if pos_json.endswith('.txt') and pos_json.startswith('file'):
        digits=[]
        for i in range(len(pos_json)):
            if isdigit(pos_json[i]):
                digits.append(pos_json[i])
        fileNo=''.join(digits)
        fileNos.append(int(fileNo))

lst=[] #this is for page ids.
MAXPAGEINAFILE=2

catalog=Catalog()
class FileOrganizer():

    def __init__(self):
        self.primaryKeys={}
        pass

    def checkIndexStorage(self):
        global lst
        filename="indexstorage"
        if os.path.exists(filename):
            with open(os.path.join(path_to_json,filename)) as f:
                
                lines=f.readlines()
                if not lines:
                    return
                indexes=lines[0].split(",")
                for ind in range(len(indexes)):
                    lst.append(int(indexes[ind]))
                

    def writeIndexStorage(self):
        global lst
        with open(os.path.join(path_to_json,'indexstorage'),'w') as ist:
            indexes = [str(i) for i in lst]
            indexString = ",".join(indexes)
            ist.write(indexString)
        

    def giveIndex(self):
        global lst
        for i in range(10000000):
            if not (i in lst):
                return i
                
        return -1
        
    def isFileEmpty(self,filename):
        with open(os.path.join(path_to_json,filename)) as f:
            lines=f.readlines()
            fileHeader=lines[0].split(" ")
            remainingPages=int(fileHeader[2])
            if remainingPages==MAXPAGEINAFILE:
                return True

        return False



    def giveAFile(self, xtype):
        containingType=False
        #TEXT DOSYASINI CEKCEN BURADA
        global path_to_json
        filenames = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.txt')]
        availableFile=None
        if len(filenames)==0: #IF THERE ISNT ANY FILE
            availableFile=self.createAFile()
        else:
            for filename in filenames:
                
                with open(os.path.join(path_to_json,filename)) as f:
                    lines=f.readlines()
                    fileHeader=lines[0].split(" ")
                    
                    if(len(fileHeader)==1): #SO IT IS ONLY "FILE "
                        availableFile=filename
                        continue
                    filePageTypes=fileHeader[1].split(",")
                    remainingPages=int(fileHeader[2])
                    if xtype in filePageTypes:
                        containingType=True
                        return containingType,None
                    if(remainingPages>0):
                        availableFile=filename




            if availableFile==None:
                availableFile=self.createAFile()

                            
        return containingType,availableFile

    def createAFile(self):
        global fileNos
        index=0
        for i in range(10000000):
            if not(i in fileNos):
                index=i
                break
        fileNos.append(index)
        fileHeader="FILE"
        filename='file{}.txt'.format(index)
        with open(os.path.join(path_to_json,filename),'w') as f:
            f.write(fileHeader)
        return filename

    def addTypeToFile(self,filename,page):
        lines=None
        fullString=""
        global lst
        with open(os.path.join(path_to_json,filename)) as f:
            lines=f.readlines()
            fileHeader=lines[0].split(" ")
         
            page.pid=self.giveIndex() #take available pid for new page
            lst.append(page.pid)
            self.writeIndexStorage()

            if(len(fileHeader)==1):
                headerString="PAGE "+ page.xtype+" "+str(page.availableRecordCount)+" "+str(page.pid)+" \n"
                dataString=""
                index=0
                while(index<page.availableRecordCount):
                    dataString+=("RECORD "+ "0"+" "+"{}".format(index) +" "+"null"+" \n")
                    index+=1
                fullString=headerString+dataString
                types=[str(page.xtype),"1"]
                stringTypes=','.join(types)
                newFileLine="FILE "+stringTypes+" "+str(MAXPAGEINAFILE-1)+" "+ str(page.pid) +" \n"
            else:
                headerString="PAGE "+ page.xtype+" "+str(page.availableRecordCount)+" "+str(page.pid)+" \n"
                dataString=""
                index=0
                while(index<page.availableRecordCount):
                    dataString+=("RECORD "+ "0"+" "+"{}".format(index) +" "+"null"+" \n")
                    index+=1
                fullString=headerString+dataString
                types=fileHeader[1].split(",")
                pids=fileHeader[3].split(",")
                pids.append(str(page.pid))
                
                remainingPages=int(fileHeader[2])
                remainingPages-=1
                # if not (page.xtype in types): #no need but whatever
                types.append(page.xtype)
                types.append("1")

                stringTypes=','.join(types)
                stringPids=','.join(pids)
                newFileLine="FILE "+stringTypes+" "+str(remainingPages)+" "+stringPids+" \n"
  


            lines[0]=newFileLine

        with open(os.path.join(path_to_json,filename),'w') as f:
            f.writelines(lines)
        with open(os.path.join(path_to_json,filename),'a') as f:
            f.write(fullString)

    def addPageToFile(self,filename,page,record):
        lines=None
        fullString=""
        global lst
        pid=0
        with open(os.path.join(path_to_json,filename)) as f:
            lines=f.readlines()
            fileHeader=lines[0].split(" ")
         
            page.pid=self.giveIndex() #take available pid for new page
            pid=page.pid
            lst.append(page.pid)
            self.writeIndexStorage()
            recordData=','.join((record.data))
            if(len(fileHeader)==1):
                headerString="PAGE "+ page.xtype+" "+str(page.availableRecordCount-1)+" "+str(page.pid)+" \n"
                index=0
                dataString=("RECORD "+ "1"+" "+"{}".format(index) +" "+recordData+" \n")
                index+=1
                while(index<page.recordCount):
                    dataString+=("RECORD "+ "0"+" "+"{}".format(index) +" "+"null"+" \n")
                    index+=1
                fullString=headerString+dataString
                types=[str(page.xtype),"1"]
                stringTypes=','.join(types)
                newFileLine="FILE "+stringTypes+" "+str(MAXPAGEINAFILE-1)+" "+ str(page.pid) +" \n"
            else:
                headerString="PAGE "+ page.xtype+" "+str(page.availableRecordCount-1)+" "+str(page.pid)+" \n"
                index=0
                dataString=("RECORD "+ "1"+" "+"{}".format(index) +" "+recordData+" \n")
                index+=1
                while(index<page.recordCount):
                    dataString+=("RECORD "+ "0"+" "+"{}".format(index) +" "+"null"+" \n")
                    index+=1
                fullString=headerString+dataString
                types=fileHeader[1].split(",")
                pids=fileHeader[3].split(",")
                pids.append(str(page.pid))
                
                remainingPages=int(fileHeader[2])
                remainingPages-=1
                if not (page.xtype in types):
                    types.append(page.xtype)
                    types.append(1)
                else:
                    typeIndex=types.index(page.xtype)
                    types[typeIndex+1]=str(int(types[typeIndex+1])+1)
                stringTypes=','.join(types)
                stringPids=','.join(pids)
                newFileLine="FILE "+stringTypes+" "+str(remainingPages)+" "+stringPids+" \n"



            lines[0]=newFileLine

        with open(os.path.join(path_to_json,filename),'w') as f:
            f.writelines(lines)
        with open(os.path.join(path_to_json,filename),'a') as f:
            f.write(fullString)

        return [pid,0]




    def fillThePrimaryKeys(self):
        filename='primaryKeyStorage'
        if os.path.exists(filename):
            with open(os.path.join(path_to_json,'primaryKeyStorage')) as f:
                lines=f.readlines()
                for i in range(len(lines)):
                    splittedLine=lines[i].split(" ")
                    if splittedLine[1]=="\n":
                        self.primaryKeys[splittedLine[0]]=[]
                    else:
                        pKeyList=splittedLine[1].split(",")
                        self.primaryKeys[splittedLine[0]]=pKeyList


    def appendTypePKeyStorage(self,xtype):
        with open(os.path.join(path_to_json,'primaryKeyStorage'),'a') as f:
            f.write(xtype+" \n")
            


    def storeNewListPKeyStorage(self,xtype,newList):
        lines=[]
        pKeyList=','.join(newList)
        with open(os.path.join(path_to_json,'primaryKeyStorage')) as f:
            lines=f.readlines()
            for i in range(len(lines)):
                splittedLine=lines[i].split(" ")
                if splittedLine[0]==xtype:
                    lines[i]=xtype+" "+pKeyList+" \n"

        with open(os.path.join(path_to_json,'primaryKeyStorage'),'w') as f:
            f.writelines(lines)

    def storeDeletionTypePKeyStorage(self,xtype):
        lines=[]

        with open(os.path.join(path_to_json,'primaryKeyStorage')) as f:
            lines=f.readlines()
            for i in range(len(lines)):
                splittedLine=lines[i].split(" ")
                if splittedLine[0]==xtype:
                    lines.pop(i)
                    break

        with open(os.path.join(path_to_json,'primaryKeyStorage'),'w') as f:
            f.writelines(lines)
    
    # def storeDeletionRecordPKeyStorage(self,xtype,primaryKey):
    #     lines=[]

    #     with open(os.path.join(path_to_json,'primaryKeyStorage')) as f:
    #         lines=f.readlines()
    #         for i in range(len(lines)):
    #             splittedLine=lines[i].split(" ")
    #             if splittedLine[0]==xtype:
    #                 pKeyList=splittedLine[1].split(",")
    #                 pKeyList.remove(primaryKey)
    #                 newpKeyList=','.join(pKeyList)
    #                 lines[i]=xtype+" "+newpKeyList+" \n"
    #                 break

    #     with open(os.path.join(path_to_json,'primaryKeyStorage'),'w') as f:
    #         f.writelines(lines)

    def pKeyStorageOps(self,xtype,primaryKey,deleteBool=False):
        if primaryKey==None:
            if deleteBool:
                del self.primaryKeys[xtype]
                self.storeDeletionTypePKeyStorage(xtype)
                return
            self.primaryKeys[xtype]=[]
            self.appendTypePKeyStorage(xtype)
            return
        
        else:
            if deleteBool:
                newList=self.primaryKeys[xtype]
                newList.remove(primaryKey)
                self.primaryKeys[xtype]=newList
                self.storeNewListPKeyStorage(xtype,newList)
                return
            newList=self.primaryKeys[xtype]
            newList.append(primaryKey)
            self.primaryKeys[xtype]=newList
            self.storeNewListPKeyStorage(xtype,newList)
            return

    


    def createType(self,splittedStr):
        #look for all files that if it contains this type page.
        print(splittedStr)
        xtype=splittedStr[2]
        fieldCount=0
        primaryKeyOrder=0
        attributes=[]
        attributeTypes=[]
        if len(splittedStr)>3:
            fieldCount=int(splittedStr[3])
            

            primaryKeyOrder=int(splittedStr[4])
            attributes=[]
            attributeTypes=[]
            i=0
            while i<fieldCount*2:  #store attributes from splittedStr
                attributeTypes.append(splittedStr[6+i])
                attributes.append(splittedStr[5+i])
                i+=2

        page=Page(xtype=xtype,availableRecordCount=10) #create new page with given instructions
        
        containingType,filename=self.giveAFile(xtype)  #take a file 
        if containingType:
            return("FAILURE")

        self.addTypeToFile(filename,page) #add page to that file
        self.pKeyStorageOps(xtype,None)
        

        catalog.addToAttributes(xtype,attributes,attributeTypes)  #ADDED TO SYSTEM CATALOG ATTRIBUTES
        catalog.addToFileRelations(xtype,filename)
        catalog.addToPrimaryKeys(xtype,primaryKeyOrder)
        tempFileName="{}.db".format(xtype)
        tempFullFileName="full{}.db".format(xtype)
        bplustree=BPlusTree(filename=os.path.join(path_to_json,"{}.db".format(xtype)), key_size=20,serializer=StrSerializer()) 
        fullbplustree=BPlusTree(filename=os.path.join(path_to_json,"full{}.db".format(xtype)),order=50, page_size=15000,key_size=20, value_size=300, cache_size=600,serializer=StrSerializer())   
        fullbplustree.close()
        bplustree.close()
        catalog.addToIndexRelations(xtype,(tempFileName+","+tempFullFileName))
        catalog.addIndexData(xtype,(tempFileName+","+tempFullFileName))
        
        #newPage artık bizim oluşturulmuş pageimiz ama sadece zamir gibi. newPage.page bizim jsona atacağımız asıl dictionary ama page i fileda depolaycağız.
        #bir fileda bir sürü page olabilir. File dolarsa yeni file a geçiyoruz. Her page sadece bir type ı tutuyor ama bir type bir sürü pagede olabilir.

        return("SUCCESS")
    
    
    def deleteType(self,xtype):
        global path_to_json
        global lst
        global fileNos
        filenames = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.txt')]
        check=False
        gonnabeRemoved=False
        gonnabeRemovedFileName=None
        for filename in filenames:
            changed=False
            lines=[]
            with open(os.path.join(path_to_json,filename)) as f:
                if gonnabeRemoved==True:
                    digits=[]
                    for i in range(len(gonnabeRemovedFileName)):
                        if isdigit(gonnabeRemovedFileName[i]):
                            digits.append(gonnabeRemovedFileName[i])
                    fileNo=''.join(digits)
                    fileNos.remove(int(fileNo))

                    os.remove(gonnabeRemovedFileName)
                gonnabeRemoved=False
                gonnabeRemovedFileName=None
                
                lines=f.readlines()
                fileHeader=lines[0].split(" ")
                # if(len(fileHeader)==1):   NO NEED!
                #     continue  
                types=fileHeader[1].split(",")
                remainingPages=int(fileHeader[2])

                

                pids=fileHeader[3].split(",")

                if xtype in types:
                    check=True
                    changed=True
                    index=1
                    temp=len(lines)
                    while(index<temp):
                        pageHeader=lines[index].split(" ")
                        pid=pageHeader[3]

                        if(pageHeader[1]==xtype):
                            del lines[index:index+11]
                            index-=11
                            temp-=11
                            remainingPages+=1
                            pids.remove(pid)
                            lst.remove(int(pid))
                        index+=11
                    
                    typeIndex=types.index(xtype)
                    types.pop(typeIndex+1) #remove the count of the type since there is no type.
                    types.remove(xtype)
                    self.writeIndexStorage()

                stringTypes=(",".join(types))
                stringPids=(",".join(pids))

                if remainingPages==MAXPAGEINAFILE:
                    gonnabeRemoved=True
                    gonnabeRemovedFileName=filename
                    continue

                newFileLine="FILE "+stringTypes+" "+str(remainingPages)+" "+stringPids+" \n"
            lines[0]=newFileLine
            if changed: 
                with open(os.path.join(path_to_json,filename),'w') as f:
                    f.writelines(lines)
        if gonnabeRemoved:
            digits=[]
            for i in range(len(gonnabeRemovedFileName)):
                if isdigit(gonnabeRemovedFileName[i]):
                    digits.append(gonnabeRemovedFileName[i])
            fileNo=''.join(digits)
            fileNos.remove(int(fileNo))
            # print("WTF",fileNos)

            os.remove(gonnabeRemovedFileName)


        if not check:
            #ERROR NO TYPE FAILURE
            return "FAILURE"
        catalog.deleteFromFileRelations(xtype)
        catalog.deleteFromPrimaryKeys(xtype)
        catalog.deleteFromAttributes(xtype)
        catalog.deleteIndexData("{}.db".format(xtype))
        catalog.deleteIndexRelations(xtype)
        self.pKeyStorageOps(xtype,None,deleteBool=True)
        os.remove("{}.db".format(xtype))
        os.remove("full{}.db".format(xtype))

        return "SUCCESS"
        
    def listAllTypes(self):
        allTypes=[]
        global path_to_json
        filenames = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.txt')]
        for filename in filenames:
            with open(os.path.join(path_to_json,filename)) as f:
                line=f.readline()
                fileHeader=line.split(" ")
                if(len(fileHeader)==1):
                    continue
                types=fileHeader[1].split(",")

                allTypes=allTypes+types
        
        return allTypes

        #newPage artık bizim oluşturulmuş pageimiz ama sadece zamir gibi. newPage.page bizim jsona atacağımız asıl dictionary ama page i fileda depolaycağız.
        #bir fileda bir sürü page olabilir. File dolarsa yeni file a geçiyoruz. Her page sadece bir type ı tutuyor ama bir type bir sürü pagede olabilir.
    
    def givePage(self,filename,index):
       
        lines=[] #to use lines in file
        pageLines=[]
        with open(os.path.join(path_to_json,filename)) as f:
            lines=f.readlines()            
            pageLines=lines[index:index+11]
        return pageLines


    def writePage(self,pageLines,newPageLine, index, newRecordLine):
        pageLines[0]=newPageLine
        pageLines[index]=newRecordLine
        return pageLines
    
    def deletePage(self,filename,lines,index):
            fileHeader=lines[0].split(" ")
            remainingPages=int(fileHeader[2])
            types=fileHeader[1].split(",")
            pids=fileHeader[3].split(",")
            pageHeader=lines[index].split(" ")
            pid=pageHeader[3]
            xtype=pageHeader[1]

            typeIndex=types.index(xtype)

            del lines[index:index+11] #delete the page
            remainingPages+=1

            if remainingPages==MAXPAGEINAFILE:
                return True

            types[typeIndex+1]=str(int(types[typeIndex+1])-1)
            if int(types[typeIndex+1])==0:
                types.pop(typeIndex+1)
                types.pop(typeIndex)

            pids.remove(pid)
            lst.remove(int(pid))
            self.writeIndexStorage()

            stringTypes=','.join(types)
            stringPids=','.join(pids)
            newFileLine="FILE "+stringTypes+" "+str(remainingPages)+" "+ stringPids +" \n"
            lines[0]=newFileLine
            return lines


        

    def changePageForInsertion(self, xtype,record):  

        bplustree=BPlusTree(filename=os.path.join(path_to_json,"{}.db".format(xtype)),key_size=20,serializer=StrSerializer())
        fullbplustree=BPlusTree(filename=os.path.join(path_to_json,"full{}.db".format(xtype)),order=50, page_size=15000,key_size=20, value_size=300, cache_size=600,serializer=StrSerializer())  
        
        #CHECK FROM SYSTEM CATALOG THAT TYPE CONSISTS!!!!
        filenamesForCheck=catalog.takeFileNamesFromFileRelations(xtype) 
        filenames = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.txt')]
        if filenamesForCheck==None:
            return None,None #there is no such type


         #check if new record's primary key is same with previous ones.
        #take pKeyNo catalog
        pKeyNo=int(catalog.takeFromPrimaryKeys(xtype))
        primaryKey=record.data[pKeyNo-1]

        primaryKey=record.data[pKeyNo-1]

        if primaryKey in self.primaryKeys[xtype]:
            return "FAILURE","FAILURE"


        self.pKeyStorageOps(xtype,primaryKey) #add primarykeys dictionary the primary key.



        availableFileName=None #this is the B plan for if there isn't any place in any pages for the type. So we take a available file for new page.        

        for filename in filenames:
            with open(os.path.join(path_to_json,filename)) as f:
                lines=f.readlines()
                fileHeader=lines[0].split(" ")
                
                remainingPages=int(fileHeader[2])  #this is the check for is there any place in file for new page(the B PLAN)
                if(remainingPages>0):
                    availableFileName=filename
                    if len(filenamesForCheck)==0: #if there is no file containing the type, however there is the type then find the first available file to put new page.
                        page=Page(xtype=xtype,availableRecordCount=10)
                        self.addPageToFile(availableFileName,page, record)
                        return -1,-1

                filePageTypes=fileHeader[1].split(",")
                if xtype in filePageTypes:
                    index = 1
                    while(index<len(lines)):
                        pageLines=self.givePage(filename,index) #TAKE PAGES ONE BY ONE
                        pageHeader=pageLines[0].split(" ")
                        availableRecordCount=int(pageHeader[2])
                        if(pageHeader[1]==xtype and int(pageHeader[2])>0):
                            index2=1
                            while(index2<11):
                                recordHeader=pageLines[index2].split(" ")
                                rid=recordHeader[2]
                                pid=pageHeader[3]
                                stringRecord=','.join(record.data)
                                 

                                if(recordHeader[1]=='0'):
                                    availableRecordCount-=1 #we use one more record stock in page.
                                    newRecordLine="RECORD "+"1"+" "+rid+" "+stringRecord+" \n"
                                    
                                    newPageLine="PAGE "+ pageHeader[1]+" "+str(availableRecordCount)+" "+pageHeader[3]+" \n"                   
                                    #created new lines for the file, we found the record now return it.
                                    pageLines=self.writePage(pageLines=pageLines,newPageLine=newPageLine,index=index2,newRecordLine=newRecordLine)
                                    lines[index:index+11]=pageLines
                                    


                                    #insert the bplustree
                                    strRecord=','.join(record.data)
                                    recordID=[str(pid),str(rid)]
                                    strRID=','.join(recordID)
                                    try:
                                        bplustree.insert(primaryKey,str.encode(strRID))                                  
                                        fullbplustree.insert(primaryKey,str.encode(strRecord))
                                    except:
                                        pass


                                    
                                    fullbplustree.close()
                                    bplustree.close()
                                    
                                    return(lines,filename)
                                index2+=1



                        index+=11

        page=Page(xtype=xtype,availableRecordCount=10)

        if availableFileName==None:
            newFileName=self.createAFile()
            catalog.addToFileRelations(page.xtype,newFileName)
            recordID=self.addPageToFile(newFileName,page,record)
            pid=recordID[0]
            rid=recordID[1]
            recordID=[str(pid),str(rid)]
            strRecord=','.join(record.data)
            strRID=','.join((recordID))
            try:
                bplustree.insert(primaryKey,str.encode(strRID))
                fullbplustree.insert(primaryKey,str.encode(strRecord))
            except:
                pass
            bplustree.close()
            fullbplustree.close()
            
        else:
            recordID=self.addPageToFile(availableFileName,page,record)
            catalog.addToFileRelations(page.xtype,availableFileName)
            pid=recordID[0]
            rid=recordID[1]
            recordID=[str(pid),str(rid)]
            strRecord=','.join(record.data)
            strRID=','.join((recordID))
            try:
                bplustree.insert(primaryKey,str.encode(strRID))
                fullbplustree.insert(primaryKey,str.encode(strRecord))
            except:
                pass
            bplustree.close()
            fullbplustree.close()

        return -1,-1

    def insertRecord(self, splittedStr):
        xtype=splittedStr[2]
        fields=[]

        for i in range(3,len(splittedStr)):
            fields.append(splittedStr[i])

        record=Record(fields)
        lines,filename=self.changePageForInsertion(xtype,record)


        if lines=="FAILURE":
            return "FAILURE"
        elif lines==None:
            #print("NO INSERT!")
            return "FAILURE"
        elif(lines==-1):
            #print("New Page Generated!")
            return "SUCCESS"
        else: 
            #print("Added to a Page")
            with open(os.path.join(path_to_json,filename),'w') as f:
                f.writelines(lines)
            return "SUCCESS"

            


        #look for all files find the free page corresponds the type
        #found the page we need
        #json.load file sonra page i al filan recordu ekle


    #bir sekilde recordId nin gelmesi gerekiyor bana.
    #we reach this recordId with primary key by using bplustree. when we delete the record we need the delete it from primary keys. #Bplus tree de check etcez var mı yok mu diye
    #eğer record yoksa zaten buraya girmez. varsa zaten buraya gircek. 
    def deleteRecord(self, xtype,recordID):
        #eğer record yoksa zaten buraya girmez. varsa zaten buraya gircek. 
        pid=int(recordID[0])
        rid=int(recordID[1])

        primaryKey=None
        pKeyNo=int(catalog.takeFromPrimaryKeys(xtype))
        lines=[]
        filenames=catalog.takeFileNamesFromFileRelations(xtype)
        found=False #we found the record or not
        foundFileName=None
        gonnaBeRemovedFilename=None
        for filename in filenames:
            if not found:
                with open(os.path.join(path_to_json,filename)) as f:
                    lines=f.readlines()
                    fileHeader=lines[0].split(" ")
                    filePids=fileHeader[3].split(",")
                    for ind in range(len(filePids)):
                        filePids[ind]=int(filePids[ind])
                    if pid in filePids:

                        index=1
                        while(index<len(lines) and not found):
                            pageLines=self.givePage(filename,index) #TAKE PAGES ONE BY ONE
                            pageHeader=pageLines[0].split(" ")
                            availableRecordCount=int(pageHeader[2])
                            if(pid==int(pageHeader[3])): #if the page has the searched pid
                                availableRecordCount=availableRecordCount+1
                                oldRecordLine=pageLines[rid+1]
                                strOldRecordHeader=oldRecordLine.split(" ")
                                oldRecordData=strOldRecordHeader[3].split(",")
                                primaryKey=oldRecordData[pKeyNo-1]

                                if availableRecordCount==10: #if the available record count is 10 then the page is empty so delete the page.
                                    lines=self.deletePage(filename,lines,index)
                                    gonnaBeRemovedFilename=filename
                                    found=True
                                    
                                    break
                                
                                newRecordHeader="RECORD "+ "0"+" "+str(rid) +" "+"null"+" \n"  #take the new record header put in the belonging place
                                newPageLine="PAGE "+ pageHeader[1]+" "+str(availableRecordCount)+" "+pageHeader[3]+" \n"   #new page we substract one record so increase available record count
                                pageLines=self.writePage(pageLines,newPageLine,rid+1,newRecordHeader)
                                
                                lines[index:index+11]=pageLines
                                found=True
                                foundFileName=filename
                
                                break

                            index+=11

        if lines==True: #it is only true when we need to remove the file
            os.remove(gonnaBeRemovedFilename)
            return

        self.pKeyStorageOps(xtype,primaryKey,True) #delete the primary key from dictionary since the record is gonna be deleted

        with open(os.path.join(path_to_json,foundFileName),'w') as f:
            f.writelines(lines)
            
    #yine bplustree ye gidiyor o yuzden kontroller orada saglaniyor
    def updateRecord(self,xtype,recordID, newFields):
        #pKeyNo=catalog.takeFromPrimaryKeys(xtype)
        #pKeyNoIndex=pKeyNo-1                           no check for if it is trying to change primary key or not !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        lines=[]

        pid=int(recordID[0])
        rid=int(recordID[1])
        filenames=catalog.takeFileNamesFromFileRelations(xtype)
        found=False
        foundFileName=None
        for filename in filenames:
            if not found:
                with open(os.path.join(path_to_json,filename)) as f:
                    
                    lines=f.readlines()
                    fileHeader=lines[0].split(" ")
                    filePids=fileHeader[3].split(',')
                    for ind in range(len(filePids)):
                        filePids[ind]=int(filePids[ind])
                    if pid in filePids:
                        index=1
                        while(index<len(lines)):
                            pageLines=self.givePage(filename,index) #TAKE PAGES ONE BY ONE
                            pageHeader=pageLines[0].split(" ")

                            if(pid==int(pageHeader[3])):
                                #no check for if it is trying to change primary key or not !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                stringRecord=','.join(newFields)

                                newRecordLine="RECORD "+"1"+" "+str(rid)+" "+stringRecord+" \n"
                                pageLines[rid+1]=newRecordLine
                                
                                for i in range(index,index+11):
                                    
                                    lines[i]=pageLines[i-index]

                                found=True
                                foundFileName=filename
                                break
                            index+=11
        with open(os.path.join(path_to_json,foundFileName),'w') as f:
            f.writelines(lines)
            


    #yine bplustree ye gidiyor o yuzden kontroller orada saglaniyor
    def searchRecord(self,xtype,recordID):

        pid=int(recordID[0])
        rid=int(recordID[1])
        filenames=catalog.takeFileNamesFromFileRelations(xtype)
        for filename in filenames:
            with open(os.path.join(path_to_json,filename)) as f:
                lines=f.readlines()
                fileHeader=lines[0].split(" ")
                filePids=fileHeader[3].split(",")
                for ind in range(len(filePids)):
                    filePids[ind]=int(filePids[ind])
                if pid in filePids:
                    index=1
                    while(index<len(lines)):
                        pageLines=self.givePage(filename,index) #TAKE PAGES ONE BY ONE
                        pageHeader=pageLines[0].split(" ")
                        if(pid==int(pageHeader[3])):
                            recordStr=pageLines[rid+1]
                            splittedRecord=pageLines[rid+1].split(" ")
                            fields=splittedRecord[3].split(",")
                            record=Record(fields)
                            return record
                        index+=11
            
#PRIMARY KEY STORAGE YOK