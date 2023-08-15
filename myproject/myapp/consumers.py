import time
import json
import asyncio
from urllib import response
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import DataCivil, DataGroup, DataStatus
from django.db.models import Count
from django.db.models.functions import TruncDate, Trunc
from datetime import datetime, timedelta


from .tasks import *


class getGreetingWs(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.accept()
        print("connected Websocket . . .")

        #add.delay(10,5) #celery async tasks
        
        data = await self.get_data()
        

        #print(groupd)

        await self.send(data)

    async def receive(self, text_data):
        # in javascript must used socket.onopen and use send() function websocket, will be handle here
        print("server says client message received", text_data)
        await self.send(text_data)

    def disconnect(self, text_data):
        pass
    
    @database_sync_to_async
    def get_data(self):
        getdata = DataCivil.objects.all()
        group = DataGroup.objects.all()
        
        datestart = "2023-08-01"
        dateend = "2023-08-31"
        dateformat = "%Y-%m-%d"

        datestartformat = datetime.strptime(datestart, dateformat).date()
        dateendformat = datetime.strptime(dateend, dateformat).date()

        num_days = (dateendformat - datestartformat).days + 1

        datachart = []
        labeldate = []

        for day in range(num_days):
            current_date = datestartformat + timedelta(days=day)
            labeldate.append(current_date.strftime('%m/%d/%Y'))

        group_a = DataCivil.objects.filter(group__initial="A")
        group_b = DataCivil.objects.filter(group__initial="B")
        group_c = DataCivil.objects.filter(group__initial="C")
        group_d = DataCivil.objects.filter(group__initial="D")

        for groups in group:

            dataByDate = []
            for day in range(num_days):
                current_date = datestartformat + timedelta(days=day)
                dataCivil = DataCivil.objects.filter(group__namagroup=groups, created_dt__date=current_date)

                dataDay = {
                    "count" : len(dataCivil),
                    "date"  : current_date.strftime('%Y-%m-%d'),
                    "group" : groups
                }

                dataByDate.append(dataDay['count'])
                
            
                
            #dataCivil = DataCivil.objects.filter(group__namagroup=groups).annotate(date=TruncDate('created_dt')).values('date').annotate(count=Count('id')).values('count','date')
            # for civil in dataCivil:
            #     dataByDate.append(civil['count'])

            xchart = {
                "name" : "{}".format(groups),
                "type" : "area",
                "data" : dataByDate
            }

            datachart.append(xchart)

        data_a = len(group_a)
        data_b = len(group_b)
        data_c = len(group_c)
        data_d = len(group_d)

        ds = []
        
        for datasource in getdata:
            username = datasource.userid.username
            email = datasource.userid.email
            alamat = datasource.alamat
            telp = datasource.telp
            grouping = datasource.group.namagroup
            status = datasource.status.status

            ds.append({"username" : username, "email" : email, "alamat" : alamat, "telp" : telp, "grouping" : grouping, "status" : status})

        result = {
            "type" : "onmessage",
            "result" : ds,
            "box_a" : data_a,
            "box_b" : data_b,
            "box_c" : data_c,
            "box_d" : data_d,
            "chart" : datachart,
            "date" : labeldate
        }

        return json.dumps(result)
    
    @database_sync_to_async
    def get_group(self):
        data = DataGroup.objects.all()
        datagroup = []

        for group in data:
            grp = {"initial" : group.initial, "group" : group.namagroup}
            datagroup.append(grp)

        #print(datagroup)
        return json.dumps(datagroup)

class SendData(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("ws_submit_group", self.channel_name)

        print("Open websocket SendData . . .")

    async def receive(self, text_data):
        
        labeldate = []
        datachart = []

        payload = json.loads(text_data)
        datajson = {"userid":payload['userid'], "alamat":payload['alamat'], "status":payload['status'], "telp": payload['telp'], "group":payload['group']}
        
        await self.insertData(json.dumps(datajson)) #insert to database with json string.

        dataSend = await self.get_data_by_id(payload['userid'])
        #grp = await self.get_data_group()
        
        #print(grp)

        datestart = "2023-08-01"
        dateend = "2023-08-31"
        dateformat = "%Y-%m-%d"

        datestartformat = datetime.strptime(datestart, dateformat).date()
        dateendformat = datetime.strptime(dateend, dateformat).date()

        num_days = (dateendformat - datestartformat).days + 1

        for days in range(num_days):
            current_date = datestartformat + timedelta(days=days)
            labeldate.append(current_date.strftime('%m/%d/%Y'))

        
        
        grouping = await self.get_groups()

        for groups in grouping:

            dataByDate = []
            for date in labeldate:
                datep = datetime.strptime(date, "%m/%d/%Y")
                datef = datep.strftime("%Y-%m-%d")
                datadate = await self.getDataChart(groups['initial'], datef)
                dataByDate.append(datadate)

            xchart = {
                "name" : "{}".format(groups['group']),
                "type" : "area",
                "data" : dataByDate,
            }

            datachart.append(xchart)
        
        group_a = await self.getDataCivilbyGroup("A")
        group_b = await self.getDataCivilbyGroup("B")
        group_c = await self.getDataCivilbyGroup("C")
        group_d = await self.getDataCivilbyGroup("D")

        jsonData = {
            "datatable" : dataSend,
            "box_a" : group_a,
            "box_b" : group_b,
            "box_c" : group_c,
            "box_d" : group_d,
            "labeldate" : labeldate,
            "chart" : datachart
        }


        await self.channel_layer.group_send(
            "ws_submit_group",
            {
                "type" : "ws_send",
                "json_send" : json.dumps(jsonData)
            }
        )

        #data = await self.get_data()
        #await self.send(data)
    
    async def ws_send(self, event):
        #send message to websocket
        await self.send(text_data=event['json_send'])

    #if not using channel_layer/realtime data
    @database_sync_to_async
    def get_data_by_id(self, id):
        getdata = DataCivil.objects.filter(userid=id).last()
        
        ds = []

        username = getdata.userid.username
        email = getdata.userid.email
        alamat = getdata.alamat
        telp = getdata.telp
        grouping = getdata.group.namagroup
        status = getdata.status.status

        ds.append({"username" : username, "email" : email, "alamat" : alamat, "telp" : telp, "grouping" : grouping, "status" : status})

            
        # for datasource in getdata:
        #     username = datasource.userid.username
        #     email = datasource.userid.email
        #     alamat = datasource.alamat
        #     telp = datasource.telp
        #     grouping = datasource.group.namagroup
        #     status = datasource.status.status

        #     ds.append({"username" : username, "email" : email, "alamat" : alamat, "telp" : telp, "grouping" : grouping, "status" : status})

            
        return json.dumps(ds)
    
    @database_sync_to_async
    def insertData(self, datajson):

        data = json.loads(datajson)
        
        userid = User.objects.get(pk=data['userid'])
        status = DataStatus.objects.get(pk=data['status']) 
        group  = DataGroup.objects.get(pk=data['group'])

        obj = DataCivil(userid=userid, alamat=data['alamat'], status=status, telp=data['telp'], group=group)
        obj.save()

        #return DataGroup.objects.get(pk=id)

    @database_sync_to_async
    def getDataCivilbyGroup(self, initial):
        data = DataCivil.objects.filter(group__initial=initial)
        return len(data)
    
    @database_sync_to_async
    def get_groups(self):
        data = DataGroup.objects.all()
        datagroup = []

        for group in data:
            grp = {"initial" : group.initial, "group" : group.namagroup}
            datagroup.append(grp)

        #print(datagroup)
        return datagroup
    
    @database_sync_to_async
    def getDataChart(self, group, date):
        data = DataCivil.objects.filter(group__initial=group,created_dt__date=date)
        return len(data)

class BackgroundProcess(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("bg_process", self.channel_name)

        print("Strating Background Process . . .")

    async def receive(self, text_data):
        
        x = text_data #from frontend function .send()
        data = bg_process.delay(x).get() #celery tasks
        
        #number = json.loads(data)
        #print(bg_process.delay(x).state)

        await self.channel_layer.group_send(
            "bg_process",
            {
                "type" : "bg_send",
                "return" : data
            }
        )

    async def bg_send(self, event):

        #send message to websocket
        await self.send(text_data = event['return'])