
import os


path_to_catologs=os.path.abspath(os.getcwd())


class Catalog():
    def __init__(self) -> None:
        pass



    #####################################################################ATTRIBUTE CATALOG
    def addToAttributes(self,xtype,attributes,attributeTypes):
        with open(os.path.join(path_to_catologs,'catalogattribute'),'a') as ist:
            for a in range(len(attributes)):
                ist.write(xtype +" " + attributes[a] + "," + attributeTypes[a] + " " + str(a+1) + ' \n')
                
    def deleteFromAttributes(self,xtype):
        lines=[]
        if os.path.exists('catalogattribute'):

            with open(os.path.join(path_to_catologs,'catalogattribute')) as ist:
                lines=ist.readlines()  
                temp=len(lines)  
                check=False
                a=0
                while a<temp:
                    splittedLine=lines[a].split(" ")
                    if splittedLine[0]==xtype:
                        check=True
                        lines.pop(a)
                        temp-=1
                        a-=1
                    elif check:
                        break
                    a+=1
            with open(os.path.join(path_to_catologs,'catalogattribute'),'w') as ist:
                ist.writelines(lines)
        
    def takeFromAttributes(self,xtype,takeType=False):
        lines=[]

        pKeyNo=self.takeFromPrimaryKeys(xtype)
        pKeyNoIndex=int(pKeyNo)-1

        if os.path.exists('catalogattribute'):
            with open(os.path.join(path_to_catologs,'catalogattribute')) as ist:
                lines=ist.readlines()    
                for i in range(len(lines)):
                    splittedLine=lines[i].split(" ")
                    if splittedLine[0]==xtype:
                        splittedLine=lines[i+pKeyNoIndex].split(" ")
                        attList=splittedLine[1].split(",")
                        if takeType:
                            return(attList[1])
                        return(attList[0])


            
        
       
    #####################################################################FILE RELATIONS
    def addToFileRelations(self,xtype, fileName) :
        app = False
        inList = False
        if os.path.exists('catalogrelationfile'):
            with open(os.path.join(path_to_catologs,'catalogrelationfile'),'r') as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    splitted=lines[i].split(" ")
                    if splitted[0]==xtype:
                        app=True
                        filenames=splitted[1].split(',')
                        if not (fileName in filenames):
                            inList = True
                            lines[i] = lines[i].strip() +"," +fileName + ' \n'

        if(app):
            if(inList):
                with open(os.path.join(path_to_catologs,'catalogrelationfile'), 'w') as f:
                    for line in lines:
                        f.write(line)
        else:
            with open(os.path.join(path_to_catologs,'catalogrelationfile'),'a') as f:
                f.write(xtype +" " +  fileName + ' \n')


    def deleteFromFileRelations(self,xtype):
        lines=[]
        if os.path.exists('catalogrelationfile'):
            with open(os.path.join(path_to_catologs,'catalogrelationfile')) as f:
                lines = f.readlines()
                i=0
                temp=len(lines)
                while i<temp:
                    splittedLine=lines[i].split(" ")
                    if(splittedLine[0]==xtype):
                        lines.pop(i)
                        i-=1
                        temp-=1
                        break
                    i+=1
            with open(os.path.join(path_to_catologs,'catalogrelationfile'),'w') as f:
                f.writelines(lines)
    def takeFileNamesFromFileRelations(self,xtype):
        if os.path.exists('catalogrelationfile'):
            with open(os.path.join(path_to_catologs,'catalogrelationfile')) as f:
                lines = f.readlines()
                for line in lines:
                    splittedLine=line.split(" ")
                    if(splittedLine[0]==xtype):
                        filenames=splittedLine[1].split(',')
                        return filenames    
        
    #####################################################################PRIMARYKEYCATALOG
    def addToPrimaryKeys(self,xtype,pKeyNo):
        with open(os.path.join(path_to_catologs,'catalogprimarykey'),'a') as f:
            f.write(xtype+" "+ str(pKeyNo)+" \n")
    def takeFromPrimaryKeys(self,xtype):
        if os.path.exists('catalogprimarykey'):
            with open(os.path.join(path_to_catologs,'catalogprimarykey')) as f:
                lines=f.readlines()
                for line in lines:
                    splittedLine=line.split(" ")
                    if splittedLine[0]==xtype:
                        return splittedLine[1]

    
    def deleteFromPrimaryKeys(self,xtype):
        lines=[]
        if os.path.exists('catalogprimarykey'):
            with open(os.path.join(path_to_catologs,'catalogprimarykey')) as f:
                lines = f.readlines()
                temp=len(lines)
                i=0
                while i<temp:
                    splittedLine=lines[i].split(" ")
                    if(splittedLine[0]==xtype):
                        lines.pop(i)
                        i-=1
                        temp-=1
                        break
                    i+=1
            with open(os.path.join(path_to_catologs,'catalogprimarykey'),'w') as f:
                f.writelines(lines)


    def takeAllTypes(self):
        allTypes=[]
        if os.path.exists('catalogprimarykey'):
            with open(os.path.join(path_to_catologs,'catalogprimarykey')) as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    splitted=lines[i].split(" ")
                    allTypes.append(splitted[0])
        return allTypes
                


#########################################3

    def addIndexData(self,xtype,index):
        with open(os.path.join(path_to_catologs,'catalogindex'),'a') as f:
            f.write(index +" " + self.takeFromAttributes(xtype) +' \n')

    def deleteIndexData(self,index):
        lines=[]
        with open(os.path.join(path_to_catologs,'catalogindex')) as f:
            lines=f.readlines()
            temp=len(lines)
            i=0
            while i<temp:
                splitted=lines[i].split(" ")
                indexes=splitted[0].split(",")
                if index==indexes[0]:
                    lines.pop(i)
                    i-=1
                    temp-=1
                    break
                i+=1
        
        with open(os.path.join(path_to_catologs,'catalogindex'),'w') as f:
            f.writelines(lines)
    
    def addToIndexRelations(self,xtype, index) :
        with open(os.path.join(path_to_catologs,'catalogrelationindex'),'a') as f:
            f.write(xtype+" " + index +' \n')
    
    def deleteIndexRelations(self,xtype):
        lines=[]
        with open(os.path.join(path_to_catologs,'catalogrelationindex')) as f:
            lines=f.readlines()
            temp=len(lines)
            i=0
            while i<temp:
                splitted=lines[i].split(" ")
                if xtype==splitted[0]:
                    lines.pop(i)
                    i-=1
                    temp-=1
                    break
                i+=1
        
        with open(os.path.join(path_to_catologs,'catalogrelationindex'),'w') as f:
            f.writelines(lines)

    


    

