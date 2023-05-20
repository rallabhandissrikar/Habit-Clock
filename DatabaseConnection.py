from pymongo import MongoClient
from datetime import *
import datetime as datetime
import random

client = MongoClient("mongodb://localhost:27017")

def add_Single_Data(database:str, collection:str, data:dict):
    tempDatabase = client[database]
    tempCollection = tempDatabase[collection]
    data_insert_ID = tempCollection.insert_one(data).inserted_id
    return data_insert_ID

def add_multiple_Data(database:str, collection:str, data:list):
    tempDatabase = client[database]
    tempCollection = tempDatabase[collection]
    data_insert_ID = tempCollection.insert_many(data).inserted_ids
    return data_insert_ID

def get_single_Data(database:str, collection:str, filter:dict):
    tempDatabase = client[database]
    tempCollection = tempDatabase[collection]
    tempData = tempCollection.find_one(filter=filter)
    if tempData != None:
        tempData.pop('_id')
    return tempData

def get_complete_Data_Collection(database:str, collection:str):
    tempDatabase = client[database]
    tempCollecion = tempDatabase[collection]
    rawData = tempCollecion.find({})
    tempData = []
    for x in rawData:
        x.pop("_id")
        tempData.append(x)
    if tempData == [] :
        return None
    else : 
        return tempData

def update_single_Doccument(database:str, collection:str, filter:dict, updateDict:dict):
    tempDatabase = client[database]
    tempCollection = tempDatabase[collection]
    updateStatus = tempCollection.update_one(filter=filter, update={"$set":updateDict})
    return updateStatus

def remove_single_Doccument(database:str, collection:str, filter:dict):
    tempDatabase = client[database]
    tempCollection = tempDatabase[collection]
    tempCollection.delete_one(filter=filter)

def ath_user(name:str, passw:str):
    dat = get_single_Data('HC', 'users', {'name' : name})
    if dat :
        if dat['name'] == name and dat['passw'] == passw:
            return True
        else :
            return False
    elif dat == None : 
        return False
    
def create_user(name:str, passw:str):
    tempData = get_single_Data('HC', 'users', {'name' : name})
    if tempData == None:
        datDict = {
            'name' : name,
            'passw' : passw,
        }
        add_Single_Data('HC', 'users', datDict)
        return True
    else :
        return False

def VerifiedId_todo(name:str):
    temp_id = random.randint(0,1000)
    snap1 = get_single_Data('HC-Todo', name, {'id' : temp_id})
    while snap1 != None:
        temp_id = random.randint(0,1000)
        snap1 = get_single_Data('HC-Todo', name, {'id' : temp_id})
    else :
        return temp_id

def VerifiedId_habit(name:str):
    temp_id = random.randint(0,50)
    snap1 = get_single_Data('HC-Todo', name, {'id' : temp_id})
    while snap1 != None:
        temp_id = random.randint(0,20)
        snap1 = get_single_Data('HC-Todo', name, {'id' : temp_id})
    else :
        return temp_id


def add_todo_new(name:str, title:str, ed:str):
    if name and title and ed :
        snap1 = get_single_Data('HC', 'users', {'name' : name})
        if snap1 != None :
            eTime = datetime.datetime(
                day=int(ed[8:].strip()),
                month=int(ed[5:7].strip()),
                year=int(ed[:4].strip()),
            )
            tempData = {
                'title' : title,
                'end' : eTime,
                'id' : VerifiedId_todo(name=name)
            }
            
            add_Single_Data('HC-Todo', name, tempData)
            return True
        else : 
            return False

def get_todo_from_user(name:str):
    snap1 = get_single_Data('HC', 'users', {'name' : name})
    if snap1 != None :
        tempDat = get_complete_Data_Collection('HC-Todo', name)
        if tempDat == None :
            return []
        else :
            for i in tempDat :
                i['end'] = str(i['end'].date())
            return tempDat
    else :
        return []

def update_todo(name:str, id:int) :
    snap1 = get_single_Data('HC', 'users', {'name' : name})
    if snap1 != None :
        remove_single_Doccument('HC-Todo', name, {'id' : id})
        return True
    else :
        return False
    
def add_habit_new(name:str, title:str, sd:str):
    snap1 = get_single_Data('HC', 'users', {'name' : name})
    sd_time = datetime.datetime(
        day=int(sd[8:].strip()),
        month=int(sd[5:7].strip()),
        year=int(sd[:4].strip()),
    )
    if snap1 != None:
        dat = {
            'title' : title,
            'day' : 1,
            'sch' : sd_time,
            'id' : VerifiedId_habit(name=name)
        }
        add_Single_Data('HC-Ht', name, dat)
        return True
    else :
        return False
    
def update_habit(name:str, id:int):
    snap1= get_single_Data('HC', 'users', {'name':name})  
    if snap1 != None :
        snap2 = get_single_Data('HC-Ht', name, {'id' : id})
        if snap2 != None :
            if datetime.datetime.now().date() == snap2['sch'].date() :
                sd_new = snap2['sch'] + datetime.timedelta(days=1)
                prog_new = snap2['day']+1
                if prog_new > 21 :
                    remove_single_Doccument('HC-Ht', name, {'id' : id})
                else :
                    update_single_Doccument('HC-Ht', name, {'id' : id},{'sch' : sd_new, 'day' : prog_new})
                return True
            else :
                return False
        else :
            return False
    else :
        return False
    
def restart_habit(name:str, id:str, sd:str):
    snap1= get_single_Data('HC', 'users', {'name':name})
    sd_time = sd_time = datetime.datetime(
        day=int(sd[8:].strip()),
        month=int(sd[5:7].strip()),
        year=int(sd[:4].strip()),
    )
    if snap1 != None:
        snap2 = get_single_Data('HC-Ht', name, {'id':id})
        if snap2 != None :
            if '-' in str(snap2['sch']-datetime.datetime.now()) :
                update_dat = {
                    'day' : 1,
                    'sch' : sd_time
                }
                update_single_Doccument('HC-Ht', name, {'id' : id}, update_dat)
                return True
            else :
                return False
        else :
            return False
    else :
        return False
    
def get_habits_from_user(name:str) :
    snap1= get_single_Data('HC', 'users', {'name':name})
    if snap1 != None :
        tempdat = get_complete_Data_Collection('HC-Ht', name)
        if tempdat != None :
            for i in tempdat:
                i['sch'] = str(i['sch'].date())
            return tempdat
        else :
            return []
    else:
        return []
    
def remove_habit(name:str, id:int):
    snap1 = get_single_Data('HC', 'users', {'name' : name})
    if snap1 != None :
        snap2 = get_single_Data('HC-Ht', name, {'id' : id})
        if snap2 != None:
            remove_single_Doccument('HC-Ht', name, {'id' : id})
            return True
        else :
            return False
    else :
        return False
