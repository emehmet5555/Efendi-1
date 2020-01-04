class Solution ():  # Solution class is defined here

    def __init__(self,routing,scheduling,charging,chargetechnology,percentage,uncoveredjob,distance,workercost,chargecost,consumption,obj,change):
        self.routing=routing
        self.scheduling = scheduling
        self.charging = charging
        self.chargetechnology = chargetechnology
        self.percentage = percentage
        self.uncoveredjob=uncoveredjob
        self.distance=distance
        self.workercost=workercost
        self.chargecost=chargecost   # (dist/50*60)*0.077=0,0924
        self.consumption=consumption #0.66 150 km range
        self.obj=obj
        self.change=change # if any change in route, charge, schedule then assign 1; otherwise 0.

    def printinfo(self):
        print("""
               Solution objesinin özellikleri
               Routing:{}
               Uncovered:{}
               Scheduling: {}
               Charging:{}
               ChargeTechnology:{}
               Chargepercentage:{}
               Chargecost:{}
               Distance:{}
               Staffcost:{}
               Objective:{}
               """.format(self.routing, self.uncoveredjob, self.scheduling, self.charging, self.chargetechnology,self.percentage,self.chargecost,self.distance,self.workercost,self.obj))

    def printinfo2(self):
        print("""Routing:{} 
                 Scheduling: {} 
                 Charging:{}""".format(self.routing,self.scheduling,self.charging)) # Schedule, Charging))
    def printinfo3(self):
        print("""Routing: {} """.format(self.routing))
    def addjob(self,component):
        self.routing.append(component)

    def assignzeros(self,N, vector):  # N zero vector
        i = 0
        while i < N:
            vector.append(0)
            i = i + 1
        return vector

    def assign2zeros(self, N, vector):  # NxN zero matrix
        for j in range(N):
            column = []
            for i in range(N):
                column.append(0)
            vector.append(column)
        return vector

    def assign1ones(self, N, vector):  # NxN 1 matrix
        for j in range(N):
            column = []
            for i in range(N):
                column.append(1)
            vector.append(column)
        return vector

    def changeeliminate(self, Solutions):
        for i in Solutions:
            i.change = 0

    def calculateincompat(self,N,EVs,Jobs):
        Compat = []
        Incompat = []
        self.assign2zeros(N, Compat)
        self.assign1ones(N, Incompat)
        ev = 0
        job = 0
        for i in EVs:
            for j in Jobs:
                i.compatibility(Compat, Incompat, ev, job, i.genderfemale, i.gendermale, i.catallergy, i.dogallergy,
                                 i.smokingallergy, j.genderfemale, j.gendermale, j.catownership, j.dogownership,
                                 j.smokinghabit, i.etwa, i.etwb, j.jtwa, j.jtwb, j.duration, i.experience,
                                 j.requirement, j.jobscore)
                job += 1
            job = 0
            ev += 1
        return Incompat



    def adduncoveredjob(self,component):
        self.routing.append(component)

    def addschedule(self,twa,inn,out,twb):

        self.scheduling.append(twa)
        self.scheduling.append(inn)
        self.scheduling.append(out)
        self.scheduling.append(twb)

    def addschedule2(self, routing,schedulearray,charging,N):
       # print(" schedulearray",schedulearray,routing)
        if len(routing) >1:  # return home
            for i in range(1, len(routing)):
                if int(routing[i]) < (N + N) :
                    schedulearray[4*(i)+1]=float(schedulearray[4*(i)+1])+float(schedulearray[4*(i-1)+2])
                    if float(schedulearray[4*i+1])< float(schedulearray[4*i]) :#i.out---->(i+1).in
                        schedulearray[4 *i+1] = schedulearray[4 * (i)]
                    schedulearray[4 *(i)+2] = float(schedulearray[4 * (i)+2])+float(schedulearray[4*(i)+1])
                if int(routing[i]) >= (N + N):
                    schedulearray[4 * (i) + 1] = float(schedulearray[4 * (i) + 1]) + float(schedulearray[4 * i - 2])
                    schedulearray[4 * (i) + 2] = float(schedulearray[4 * (i) + 2]) + float(schedulearray[4 * (i) + 1])
                    # charge duration neredesin

            if i==len(routing)-1: # return home
              #  print(" schedulearray",schedulearray,routing,charging,len(schedulearray),len(routing))
                schedulearray[4 * (i+1) + 1] = float(schedulearray[4 * (i+1) + 1]) + float(schedulearray[4 * (i) + 2])

          #  print("2 schedulearray", schedulearray)

##############################################################
    # initial assignment is achieved here
    def initialassignment(self,N,Solutions,Incompat, Ordere, Order):
        Incompat2 = []
        self.assign1ones( N, Incompat2)

        for i in Ordere:  # evs
            for j in Order:  # jobs
                Incompat2[i][j] = Incompat[i][j]
                if Incompat2[i][j] != 0 and Incompat2[i][j] != 1000:
                    Solutions[i].addjob(str(j + N))
                    Order.remove(j)
                    for m in range(0, len(Incompat2)):
                        Incompat2[m][j] = 1000
        if len(Order) != 0:  # if the jobs could not covered then assigned to uncovered job list in the first soln object
            for j in Order:
                Solutions[0].adduncoveredjob(str(j + N))



#######################################################

    def distancematrix(self,Dmatris):
        Distance = open("F:/AA makale/Distance.txt", "r") #!!!!!!!!!! km not time !!!!!!!!!!!!!!
        # print('Distance list:', Distance.read())
        dizi = Distance.readlines()
        # print('Distance list:',dizi)

        for i in dizi:
            liste = i.split(",")  # Virgüle göre parçalama
            column = []
            for j in liste:
                column.append(j)
            Dmatris.append(column)

        Distance.close()
        return Dmatris

    def calculate1(self,Dmatris,routing,charging,consumption):

        dist=0
        if len(routing)>1:
            for j in range(0, len(routing) - 1):
                    dist = dist+ int(Dmatris[int(routing[j])][int(routing[j + 1])])
                    charging[(2 * (j+1))] = float(charging[(2 * (j+1))]) - dist*consumption
                    charging[(2 * (j+1) + 1)] = float(charging[(2 * (j+1) + 1)]) - dist*consumption

            dist = dist+int(Dmatris[int(routing[j+1])][int(routing[0])])

            charging[(2 * (len(routing)) )]=float(charging[(2 * (len(routing)) )])-dist*consumption
            charging[(2 * (len(routing)) + 1)]=float(charging[(2 * (len(routing)) + 1)])-dist*consumption
        return (dist)

    def calculate2(self,Dmatris,routing,scheduling,charging,N):
        if len(routing) >1:
            hold=0
            holdcharge=0
            if ((len(routing)+1)*4)>len(scheduling):
                for i in range (0,4):
                    scheduling.append(0)
                for i in range(0, len(routing) - 1):
                    if int(routing[i])>=(N+N):
                        hold=i
                        holdcharge=float(charging[2*hold+1]-charging[2*hold])
            if ((len(routing)+1)*4)==len(scheduling) :
                if hold!=0:
                    j = len(scheduling)-1
                    while j > (4*hold - 1):  ## insert the station two node before
                        scheduling[j] = scheduling[j - 4]
                        j = j - 1
                    scheduling[4*hold] = str(360)
                    scheduling[4 * hold+1] = str(0)
                    scheduling[4 * hold+2] = str(float((holdcharge/100)*30)) # charge tech super fast
                    scheduling[4 * hold+3] = str(1380)
                dist=0

                if len(routing)>1:
                    for j in range(0, len(routing) - 1):
                            dist = dist+ int(Dmatris[int(routing[j])][int(routing[j + 1])])
                            scheduling[(4*(j+1)+1)]=str((int(Dmatris[int(routing[j])][int(routing[j + 1])])/ 50) * 60)

                    dist = dist+int(Dmatris[int(routing[j+1])][int(routing[0])])
                    scheduling[(4 * (len(routing)) + 1)]=str((int(Dmatris[int(routing[j+1])][int(routing[0])]) / 50) * 60)

        return (scheduling)

    def addcharge(self,ch):
        self.charging.append(ch)
        self.charging.append(ch)
    # check EV visit the charging station or not
    def addcharge2(self,ch,size):
        for i in range(0, size):
            self.charging.append(ch)
            self.charging.append(ch)
    def checkstationvisit(self,routing, visit,N):
        if len(routing)>1:
            for j in range(0, len(routing) ):
                    if int(routing[j]) >= (N + N):
                        visit = 1

        return visit

    # This function finds the first location of negative charging
    def negativeSOC(self, routing, charging):
        j = 0
        for j in range(0, len(routing)+1):
           if int(charging[2 * j]) < 0 and int(charging[2 * j]) > -90:
                return j

        return (j)

    def positiveSOC(self,routing, charging):  # This function finds the location of 100> charging
        for j in range(0, len(routing)):
            if float(charging[2 * j]) > 100:
                 return j
        return j

    def neareststation(self,Dmatris,location, routing,N,S):
        T = 1000 # big number
        stationname = 0   # name the station
        i=N+N
        while i < (N+N+S):
            Mesafe = int(Dmatris[int(routing[location - 2])][i]) + int(Dmatris[i][int(routing[location - 1])])
            if Mesafe < T:
                T = Mesafe
                stationname = i
            i+=1
        return stationname

    def chcalculate(self,Dmatris, routing, charging,consumption, N ): # just calculate the SOC for ONE EV/route

        SOC=[]
        self.assignzeros(2*len(routing)+2, SOC)

        SOC[0] = 100
        SOC[1] = 100

        dist = 0
        if len(routing) > 1:
            for j in range(0, len(routing) -1):
                    dist =  int(Dmatris[int(routing[j])][int(routing[j + 1])])
                    SOC[2 * j + 2] = float(SOC[2 *j + 1]) - dist*consumption #means that *0.66 # 150 km range
                    SOC[(2 * j +3)] = float(SOC[2 * j + 2])
                    if (int(routing[j]) >= (N + N)):
                        Addedcharge = (100 - float(SOC[2 *j]) )
                        SOC[2 *j+1]= 100
                        SOC[2 * (j+1)] = SOC[2 *(j+1)]  + float(Addedcharge)
                        SOC[2 * (j + 1)+1] = SOC[2 * (j+1)+1] + float(Addedcharge)
            # return to home/depot
            dist = int(Dmatris[int(routing[j + 1])][int(routing[0])])
            SOC[2 * len(routing)] = float(SOC[2 * len(routing)-1]) - dist*consumption
            SOC[(2 * (len(routing)) + 1)] = float(SOC[(2 * (len(routing)) )])
            charging=SOC

        return charging

    # by means of this we insert the nearest station to the route to eliminate negative charging
    # and we drop the station from the route if it is necessary to visit the station
    def stationinsertdrop(self, Dmatris,routing, charging,N,S):
        if len(routing) > 2:
            location=0
            location2=0
            location = self.negativeSOC(routing, charging)
           # print("**Negative SOC detected loc route", location, routing[0],charging[2*location])
            if location != 0 and float(charging[2*location])<0 : #
               # print("Negative SOC detected loc route",location, routing[0],charging[2*location])
               # print("stationinsertdrop charging",routing,charging)
                stationname = self.neareststation(Dmatris,location, routing,N,S)  # nearest station is selected

              #  print("***loc",stationname)
                routing.insert((location - 1), stationname)

            #######################++++++++++ soc ##################################
            (location2) = self.positiveSOC(routing, charging)
           # print("Positive SOC",routing, charging,len(routing),location2)
            if location2 != 0 and float(charging[2*location])>100 :#location2!=(len(routing)-1) :
               # print("Positive SOC", nurseno,b)
                routing.remove(routing[location2])

        return routing

    def chargecalculate(self, Dmatris,routing,scheduling, charging,consumption,N,S):
        visit=0
        self.stationinsertdrop(Dmatris, routing, charging, N, S)
        charging=self.chcalculate(Dmatris, routing, charging,consumption, N)
        (visit)=self.checkstationvisit(routing, visit, N)
        if visit == 1:  # sarj istasyonuna ugramazsa hesaplamasyn
            charging = self.chargecalculaterevised(routing, charging,N)  # calculate the percentage of energy at CS
            # here scheduling variable extends
            self.calculate2(Dmatris, routing, scheduling, charging, N)

        return charging

    def chargecalculaterevised(self,routing, charging,N):

        excessivecharge=charging[len(charging)-1]-1
        locationofcs = 0
        numberofvisits = 0

        for j in range(0, len(routing) - 1):
            if (int(routing[j]) >= (N + N)):
                locationofcs = j
                numberofvisits += 1
        for j in range(2*locationofcs+1, len(charging) - 1):

            charging[j]=float(charging[j]-excessivecharge)
            charging[j+1] = float(charging[j+1])
        charging[len(charging)-1] = float(charging[len(charging)-2])
        self.percentage=[str(charging[2*locationofcs+1]-charging[2*locationofcs])]

        return charging

    def schedule(self, Dmatris,routing, scheduling, charging, N):
        self.calculate2( Dmatris,routing,scheduling,charging,N)
        #apppend station
        schedule=self.addschedule2(routing, scheduling, N)# ilk önce scheduling update olacak

    def chargetechopt(self, routing, scheduling, charging, N):
        # tek istasyon için test tamam
        visit=0
        location=0
        if len(routing) > 1:
            for j in range(0, len(routing) - 1):
                if int(routing[j]) >= (N + N):
                    visit = 1
                    location=j

        if visit == 1:  # if ev visit station
            """
            calculation of idle time
            station [stwa s-in s-out stwb]
            following job [jtwa j-in j-out jtwb]
            idle time=jtwb-duration of the following job- s-in
            """
         #   print("location",location,routing[location],routing[location+1])
            idletime=float(scheduling[4 * (location + 1) + 3]) - float(scheduling[4 * (location + 1) + 2] - scheduling[4 * (location + 1) + 1])- float(scheduling[4 * location + 1])
            percentage=float(charging[2 * location + 1] - charging[2 * location])
            chargeduration = float((percentage / 100) * 420)  # normal charger
            if idletime>= chargeduration:
              #  print("normal charger chargeduration", chargeduration)
                chargetechnology=[str(3)]

            chargeduration = float((percentage / 100) * 180)  # fast charger
            if idletime >= chargeduration:
               # print("fast charger chargeduration", chargeduration)
                chargetechnology=[str(2)]

            chargeduration = float((percentage / 100) * 30)  # super fast charger
            if idletime >= chargeduration:
               # print("super fast charger chargeduration", chargeduration)
                self.chargetechnology = [str(1)]


    def objective(self,routing,scheduling,charging,consumption,chargetechnology,percentage,uncoveredjob,distance,workercost,chargecost,obj,Incompat,N):
        self.obj=0
        routepenalty=0
        if len(routing) > 1:

            # self.obj=float(workercost)*0.5+float(distance)*0.077
            self.obj = float(workercost)  + float(distance)
            self.workercost=float(workercost)

            if chargetechnology==1:
                self.obj=self.obj+float(((percentage / 100)*30)* 0.5)
                self.chargecost=float(((percentage / 100)*30)* 0.5)
            if chargetechnology==2:
                self.obj=self.obj+float(((percentage / 100) * 180)* .03)
                self.chargecost =float(((percentage / 100) * 180)* .03)
            if  chargetechnology == 3:
                self.obj=self.obj+float(((percentage / 100) *  420)* 0.02)
                self.chargecost = float(((percentage / 100) *  420)* 0.02)
            routepenalty=self.penalty(Incompat,routing,scheduling,charging,uncoveredjob,N)
            self.obj += routepenalty
           # print("objective function value for ev",routing[0],self.obj,routepenalty,uncoveredjob)

      # super fast * 0.5 + fast * .03 + normal * 0.02 ------>these are cost
      #(super fast*30 + fast* 180 + normal*  420)/100 ------>these are full time duration for 100%

    def penalty(self,Incompat,routing,scheduling,charging,uncoveredjob,N):
        routepenalty=0
        synchronizedpenalty=0
        # ev tw violation penalizes
      #  if float(scheduling[4 * len(routing) + 1]) > float(scheduling[4 * len(routing) + 3]):
      #      routepenalty += 1000

        for j in range(1, len(routing)-1):
            if int(routing[j])<(N+N):
                if Incompat[int(routing[0])][int(routing[j]) - N] ==0: #incompatibility penalizes
                    routepenalty +=1000
                   # print("incompatibility penalizes")
                if float(scheduling[4*j+1])<float(scheduling[4*j]) or float(scheduling[4*j+1])>float(scheduling[4*j+3]): #job tw violation penalizes
                   # print("1 route time penalty", routing[0], routing[j], float(scheduling[4 * j]),float(scheduling[4 * j + 1]), float(scheduling[4 * j + 2]), float(scheduling[4 * j + 3]))
                    routepenalty += 1000
                # ev tw violation penalizes


                if  float(charging[2*j]<0) or float(charging[2*j+1]<0):
                    #print(" charging ev job incompat1 ", int(routing[0]), int(routing[j]), int(routing[j]) - N)
                    routepenalty += 1000
                if float(charging[2 * j] > 100) or float(charging[2 * j + 1] >100):
                    #print(" charging ev job incompat1 ", int(routing[0]), int(routing[j]), int(routing[j]) - N)
                    routepenalty += 1000
                # for synchronized jobs we can extends these if blocks !!
                if int(routing[j])==(N+N-1):#synchronized jobs
                    #synchronizedpenalty=1
                    for i in routing:
                        if int(i) ==(N+N-2): #synchronized jobs
                            routepenalty += 1000
                          #  print(" synchronized jobs", N + N - 1, N + N - 2)
                if int(routing[j])==(N+N-2): #synchronized jobs
                    for i in routing:
                        if int(i) ==(N+N-1): #synchronized jobs
                            routepenalty += 1000
                           # print(" synchronized jobs", N + N - 1, N + N - 2)



        #print("**** uncoveredjob ", uncoveredjob,len(uncoveredjob))
        if len(uncoveredjob)!= 0:
            if uncoveredjob[0]!=str(-1):
                routepenalty += 1000*len(uncoveredjob)
        #print(" routepenalty ", routepenalty)
        return routepenalty







    # this method calculate overall routing, scheduling, and charging decisions and their cost charges
    def Calculateoverall(self,N,S, Solutions, Jobs, EVs,Dmatris,Incompat):
        for i in Solutions:
            if len(i.routing) > 1:
                for j in range(1, len(i.routing) + 1):
                    if j != len(i.routing) and int(i.routing[j]) < (N + N):
                        i.addschedule(Jobs[(int(i.routing[j]) - N)].jtwa, str(0), Jobs[(int(i.routing[j]) - N)].duration,
                                      Jobs[(int(i.routing[j]) - N)].jtwb)
                    if j == len(i.routing):# and int(i.routing[j]) < (N + N):
                        i.addschedule(EVs[(int(i.routing[0]))].etwa, str(0), str(0), EVs[(int(i.routing[0]))].etwb)
                    i.addcharge(100)

        for i in Solutions:
            # this method calculate dist,workercost,charging from the generate route
            (i.distance) = self.calculate1(Dmatris, i.routing, i.charging,i.consumption)
            # this method recalculate charging from the generate route
            # it can add and eliminate station from the route and also optimize the percentage of charge
            # and it extends the scheduling variable interms of station's time window
            i.charging = i.chargecalculate(Dmatris, i.routing, i.scheduling, i.charging,i.consumption, N, S)

            i.addschedule2(i.routing, i.scheduling, i.charging, N)

            i.objective(i.routing, i.scheduling, i.charging,i.consumption ,i.chargetechnology, i.percentage, Solutions[0].uncoveredjob, i.distance,
                        i.workercost, i.chargecost, i.obj, Incompat, N)

           # print("\nInitial solution is generated !", totalobj)

        # this method calculate overall routing, scheduling, and charging decisions and their cost charges
    def Calculateoverall2(self, N, S, Solutions, Jobs, EVs, Dmatris, Incompat):


        for i in Solutions:

            if len(i.routing) > 1 and i.change == 1:
                # first the current station is eliminated
                for j in i.routing:
                    stationvisit = 1
                    if int(j) >= N + N:
                        stationvisit = int(j)
                        i.routing.remove(int(j))
                i.charging = []  # for the new charge calculation for the new route
                i.percentage = [str(0)]  # for the new charge calculation for the new route
                i.addcharge2(100, len(i.routing)+1)

                i.scheduling = []  # for the new charge calculation for the new route
                i.addschedule(EVs[(int(i.routing[0]))].etwa, str(0), EVs[(int(i.routing[0]))].etwa, EVs[(int(i.routing[0]))].etwb)
                for j in range(1, len(i.routing) + 1):
                    if j != len(i.routing) and int(i.routing[j]) < (N + N):
                           # print("---------- ",int(i.routing[j]),len(i.routing),len(i.scheduling))
                            i.addschedule(Jobs[(int(i.routing[j]) - N)].jtwa, str(0),
                                          Jobs[(int(i.routing[j]) - N)].duration,
                                          Jobs[(int(i.routing[j]) - N)].jtwb)

                    if j == len(i.routing):# and int(i.routing[j])< (N + N):
                            i.addschedule(EVs[(int(i.routing[0]))].etwa, str(0), str(0), EVs[(int(i.routing[0]))].etwb)

        for i in Solutions:
            if len(i.routing) > 1 and i.change == 1:
                # this method calculate dist,workercost,charging from the generate route
                # here charge does not considered just consumption is calculated !!
                (i.distance) = i.calculate1(Dmatris, i.routing, i.charging,i.consumption)
                # this method recalculate charging from the generate route
                # it can add and eliminate station from the route and also optimize the percentage of charge
                # and it extends the scheduling variable interms of station's time window
                i.charging = i.chargecalculate(Dmatris, i.routing, i.scheduling, i.charging,i.consumption, N, S)

                i.addschedule2(i.routing, i.scheduling, i.charging, N)

                i.objective(i.routing, i.scheduling, i.charging,i.consumption, i.chargetechnology, i.percentage, Solutions[0].uncoveredjob,i.distance,i.workercost, i.chargecost, i.obj, Incompat, N)

           # the idle ev is considered here seperately and clean all its parameters
            if len(i.routing) == 1 and i.change == 1:

                i.charging = []  # for the new charge calculation for the new route
                i.charging =[str(100), str(100)]
                i.scheduling = []
                i.scheduling= [str(EVs[int(i.routing[0])].etwa), str(0), str(EVs[int(i.routing[0])].etwa), str(EVs[int(i.routing[0])].etwb)]
                i.distance=0
                i.obj=0


        return Solutions
