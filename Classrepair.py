class Repair:  # repair class is defined here
    def __init__(self,scorerepair,weightrepair,numberofrepairs):
        # scores and weight are defined here
        self.scorerepair = scorerepair  # 5
        self.weightrepair = weightrepair # 5
        self.numberofrepairs = numberofrepairs  # number of iterations used

    def printinfo(self):
        print("""scorerepair:{}-weightrepair:{}-numberofrepairs:{}""".format(self.scorerepair, self.weightrepair,self.numberofrepairs))

    def randominsertion(self, N, Solutions,Jobs, Incompat):
        import random
        Uncov = 0
        sayac = 0
        while sayac < N + N and len(Solutions[0].uncoveredjob) != 0 and Uncov != -1:  #sayac <
            for j in Solutions[0].uncoveredjob:
                Uncov = int(j)

            if Uncov == -1 or Uncov == 0:
                sayac = N + N + N
            if Uncov != -1:
                k = 0 #location
                k2 = 0 #location
                nurseno = random.randint(0, (N-1))  # determine the nurse first
                while ((Incompat[nurseno][Uncov - N]) == 0):  # select an appropriate nurse
                    nurseno = int(random.randint(0, (N-1)))  # determine another appropriate nurse

                if len(Solutions[nurseno].routing) > 2:   # if selected nurse is not a free nurse
                    if Incompat[nurseno][Uncov - N] != 0:
                        for i in range(1, len(Solutions[nurseno].routing)):
                            if int(Solutions[nurseno].routing[i]) < N + N:
                                if (Jobs[int(Solutions[nurseno].routing[i])-N].jtwa >= Jobs[Uncov - N].jtwa):
                                    k = i #   print("********i.nurse route k", nurseno, i, Solutions[nurseno].routing[i], k)
                                elif (Jobs[int(Solutions[nurseno].routing[i])-N].jtwa < Jobs[Uncov - N].jtwa):
                                    k2 = i #   print("**SONA**i.nurse route k2 ", nurseno, i, Solutions[nurseno].routing[i],k2)

                        if k != 0 and k <= N - 2:  # Uncoveredjobs is assigned here
                            Solutions[nurseno].routing.insert(k,str(Uncov))
                         #   print("Araya", nurseno, Solutions[nurseno].routing)
                            Solutions[int(nurseno)].change = 1
                            Uncov = -1
                            Solutions[0].uncoveredjob.pop() #delete from the list
                        if k == 0 and k2 != 0:  # and k2<=N-2:# Uncoveredjobs is assigned here
                            Solutions[nurseno].routing.insert(k2, str(Uncov))
                            Solutions[int(nurseno)].change = 1
                        #    print("Sona", nurseno, Solutions[nurseno].routing)
                            Uncov = -1
                            Solutions[0].uncoveredjob.pop()

                if (len(Solutions[nurseno].routing) < 2 and Incompat[nurseno][Uncov - N] != 0):
                #    print("Assignment for idle nurseno", nurseno, Incompat[nurseno][Uncov - N])
                    Solutions[nurseno].routing.append(str(Uncov))
                    Solutions[int(nurseno)].change = 1
                    Uncov = -1
                    Solutions[0].uncoveredjob.pop()

            if len(Solutions[0].uncoveredjob) != 0:
                if Solutions[0].uncoveredjob[0] != str(-1):
                    Uncov = 0
            if len(Solutions[0].uncoveredjob)==0:
                Solutions[0].uncoveredjob.append(str(-1))

            sayac += 1

      #  self.OrderJTwa(N,Solutions,Jobs) !!!! gerek var mı sonra bakılacak

    def OrderJTwa(self,N,Solutions,Jobs):
        #  print("OrderJTwa")
        for i in Solutions:
            if len(i.routing) > 1:
                for m in range(0, len(i.routing)):
                    for j in range(1, len(i.routing)-1):
                        if i.routing[j] >= N and i.routing[j] < N + N and i.routing[j + 1] >= N and i.routing[j + 1] < N + N:
                            if Jobs[int(i.routing[j])-N].jtwa > Jobs[int(i.routing[j+1])-N].jtwa:
                                hold = i.routing[j+1]
                                i.routing[j+1] = i.routing[j]
                                i.routing[j] = hold

        #  print("OrderJTwa 22")

#Cheapestinsertion
    def cheapestinsertion(self, N,Solutions,Jobs,Dmatris, Incompat):
      #  print("Cheapestinsertion starts")

        if len(Solutions[0].uncoveredjob) != 0:  # Uncov != -1 and
            Uncov = 0
            for j in (Solutions[0].uncoveredjob):
                Uncov = int(j)
          #  print("Uncoveredjobs Uncov", Uncov,Solutions[0].uncoveredjob)
            if Uncov!=-1:
                big = 1000
                big2 = 1000
                k = 0
                k2 = 0
                nurseno = -1
                nurseno2 = -1
                for i in Solutions:
                    if len(i.routing) > 1:
                        for j in range(1, len(i.routing)):
                            if (int(i.routing[j]) >= N and int(i.routing[j]) < N + N and Incompat[int(i.routing[0])][Uncov - N] != 0):  # working nurse
                                if (Jobs[int(i.routing[j]) - N].jtwa >= Jobs[Uncov - N].jtwa): # suitable assignment
                                    dist = int(Dmatris[int(i.routing[j])][Uncov]) + int(Dmatris[Uncov][int(i.routing[j])])
                                    if big > dist:  # find the minimum dist
                                        nurseno = int(i.routing[0])
                                        k = int(j)
                                        big = dist
                    if (len(i.routing) < 2 and Incompat[int(i.routing[0])][Uncov - N] != 0):  # idle nurse
                        dist2 = int(Dmatris[int(i.routing[0])][Uncov]) + int(Dmatris[Uncov][int(i.routing[0])])
                        if big2 > dist2:  # find the minimum dist
                            nurseno2 = int(i.routing[0])
                            k2 = 1
                            big2 = dist2

                if k != 0 and Uncov != -1:  # Uncoveredjobs is assigned here to working EV
                    Solutions[nurseno].routing.insert(k, str(Uncov))
                    Solutions[int(nurseno)].change = 1
                    Uncov = -1
                   # print("----doluya Uncoveredjobs Uncov", Uncov, Solutions[nurseno].routing)
                    Solutions[0].uncoveredjob.pop()
                if k2 != 0 and Uncov != -1: # Uncoveredjobs is assigned here to free EV
                    Solutions[nurseno2].routing.append(Uncov)
                    Solutions[int(nurseno2)].change = 1
                    Uncov = -1
                    Solutions[0].uncoveredjob.pop()
                   # print("--boşa--atama",Solutions[nurseno2].routing,Solutions[0].uncoveredjob )
                if len(Solutions[0].uncoveredjob)==0:
              #      print("ata -1 Randominsertion", Solutions[0].uncoveredjob)
                    Solutions[0].uncoveredjob.append(str(-1))
                  #  (Routing, Uncoveredjobs) = Randominsertion(Routing, Uncoveredjobs, Incompat)


#Leasttimeinsertion
    def leasttimeinsertion(self,N,Solutions,Jobs,Dmatris, Incompat):

        if len(Solutions[0].uncoveredjob) != 0:  # Uncov != -1 and
            Uncov = 0

            k = 0
            k2 = 0
            nurseno = -1
            nurseno2 = -1
            for j in Solutions[0].uncoveredjob:
                Uncov = int(j)
            if Uncov!=-1:
                for i in Solutions:  # Uncoveredjobs is assigned here to working nurse
                    if len(i.routing) > 1:
                        for j in range(1, len(i.routing)):
                            if (int(i.routing[j]) >= N and int(i.routing[j]) < N + N and Incompat[int(i.routing[0])][Uncov - N] != 0):  # working nurse
                                if (Jobs[int(i.routing[j]) - N].jtwa >= Jobs[Uncov - N].jtwa ):  # suitable assignment
                                    time1 = (int(Dmatris[int(i.routing[j])][Uncov]) / 50) * 60
                                    time2 = (((int(Dmatris[int(i.routing[j])][Uncov]) + int(Dmatris[Uncov][int(i.routing[j])])) / 50) * 60)
                                    if (float (i.scheduling[4 * j + 1]) + time1 + float (Jobs[Uncov - N].duration) <= float (Jobs[Uncov - N].jtwb)
                                    and  float(i.scheduling[4 * j + 1]) + float(time2)+ float(Jobs[Uncov - N].duration) + float(Jobs[j].duration) <=  float (Jobs[int(i.routing[j]) - N].jtwb)):

                                        nurseno = int(i.routing[0])
                                        k = int(j)
                    if (len(i.routing) < 2 and Incompat[int(i.routing[0])][Uncov - N] != 0):  # idle nurse
                        time2 = (((int(Dmatris[int(i.routing[0])][Uncov]) + int(Dmatris[Uncov][int(i.routing[0])])) / 50) * 60)
                        if (float (i.scheduling[2]) + time2 < float (i.scheduling[3])):
                           # print("Cheapestinsertion idle nurseno2", nurseno)
                            k2 = 1
                            nurseno2 = int(i.routing[0])

                if k != 0:  # Uncoveredjobs is assigned here to idle nurse
                  #  print("----doluya 1", Uncov, Solutions[nurseno].routing)
                    Solutions[nurseno].routing.insert(k, str(Uncov))
                    Solutions[int(nurseno)].change = 1
                    Uncov = -1
                    Solutions[0].uncoveredjob.pop()
                  #  print("----doluya Uncoveredjobs Uncov", Uncov, Solutions[nurseno].routing)

                if k != 0 and Uncov != -1:  # Uncoveredjobs is assigned here k != 0
                    Solutions[nurseno2].routing.append(Uncov)
                    Solutions[int(nurseno2)].change = 1
                    Uncov = -1
                    Solutions[0].uncoveredjob.pop()
                 #   print("--boşa--atama",Solutions[nurseno2].routing,Solutions[0].uncoveredjob )

                #if Uncov != -1:
                 #   print("atama yok", Uncov)
                   # (Routing, Uncoveredjobs) = Randominsertion(Routing, Uncoveredjobs, Incompat)
                if len(Solutions[0].uncoveredjob)==0:
                    Solutions[0].uncoveredjob.append(str(-1))


#Nearest station insertion
    def neareststationinsertion(self,N,S,Solutions,Dmatris):
        #print("neareststationinsertion starts ")
        visit = 0
        check = []
        Solutions[0].assignzeros( N, check)
        self.calculateallSOC(N,Solutions,Dmatris)  # just calculate the SOC for all working EVs/routes

        for i in Solutions:
            if len(i.routing) > 1:
                for j in range(1, len(i.routing)):
                    if int(i.charging[2 * j]) < 0 and int(i.charging[2 * j]) > -90:
                        check[int(i.routing[0])]=-1
       # print("neareststationinsertion ", check)
        for i in Solutions:
            if len(i.routing) > 1 and check[int(i.routing[0])] != 0:  # check the negative SOC

                # insert or eliminate the CS
                i.routing = i.stationinsertdrop(Dmatris,  i.routing, i.charging, N, S)
                Solutions[int(i.routing[0])].change = 1
                i.charging=i.chcalculate(Dmatris, i.routing, i.charging, N)  # just calculate the SOC for ONE EV/route
                visit = i.checkstationvisit(i.routing, visit, N)
                if int(visit) == 1:  # sarj istasyonuna ugramazsa hesaplamasyn
                    i.charging = i.chargecalculaterevised(i.routing, i.charging, N)  # calculate the percentage of energy at CS


    def calculateallSOC(self,N,Solutions,Dmatris):  # just calculate the SOC for all working EVs/routes
        for i in Solutions:
            i.charging=i.chcalculate(Dmatris, i.routing, i.charging, N)

#Chargetechset technology
    def chargetechset(self,N,S,Solutions,Dmatris):
        import random

        for i in Solutions:
            if len(i.routing) > 1:
                for j in range(1, len(i.routing)):
                    if int(i.routing[j]) > N+N:
                        nurseno=int(i.routing[0])
                        travelingtime = float( Dmatris[int(i.routing[j])][int(i.routing[j + 1])]) / 50 * 60
                        # more than one visits !!!
                        a = (float(i.percentage[0]) * 30) / 100
                        b = (float(i.percentage[0]) * 180) / 100
                        c = (float(i.percentage[0]) * 420) / 100
                        #print("percentage-->duration", a,b,c)

                        cc = -1
                        if float(i.scheduling[4 * j + 1])+ c <= float(Solutions[nurseno].scheduling[4 * (j + 1) + 3]) - travelingtime and cc == -1:
                          #  print("normal charge ", c)
                            cc = 1
                            i.chargetechnology = [str(3)]
                            Solutions[int(i.routing[0])].change = 1
                        if float(i.scheduling[4 * j + 1])+ b <= float(Solutions[nurseno].scheduling[4 * (j + 1) + 3]) - travelingtime and cc == -1:
                          #  print("fast charge", b)
                            cc = 1
                            i.chargetechnology = [str(2)]
                            Solutions[int(i.routing[0])].change = 1
                        if float(i.scheduling[4 * j + 1])+ a <= float(Solutions[nurseno].scheduling[4 * (j + 1) + 3]) - travelingtime and cc == -1:
                           # print("super fast charge", a)
                            cc = 1
                            i.chargetechnology = [str(1)]
                            Solutions[int(i.routing[0])].change = 1
       # print("Chargetechset finishied ")


        ################################# LOCAL SEARCH ##############################################################

# local search neighbourhoods considers only the working EVs

    def verticalswap(self, N, Solutions, Incompat):
       # print("verticalswap")
        import random

        nurseno1 = random.randint(0, (N - 1))  # determine the nurse first
        nurseno2 = random.randint(0, (N - 1))  # determine the nurse first

        while len(Solutions[nurseno1].routing) < 2:  # if selected nurse is not a free nurse
            nurseno1 = random.randint(0, (N - 1))  # determine the nurse

        while len(Solutions[nurseno1].routing) < 2:  # if selected nurse is not a free nurse
            nurseno2 = random.randint(0, (N - 1))  # determine the nurse

        i = 0
      #  print("nurseno", nurseno1, nurseno2)
       # print(" Routes",Solutions[nurseno1].routing,Solutions[nurseno2].routing)
        if len(Solutions[nurseno1].routing) > 2 and len(Solutions[nurseno2].routing) > 2 and nurseno1 != nurseno2:  # if selected nurse is a free nurse
            job1 = random.randint(0, len(Solutions[nurseno1].routing)-1)  # from  nurseno1
            job2 = random.randint(0, len(Solutions[nurseno2].routing)-1)  # from  nurseno2
           # print("1 # from  nurseno1 job1", job1)
           # print("1 # from  nurseno2 job2", job2)
            while int(Solutions[nurseno1].routing[job1]) >= N + N or int(Solutions[nurseno1].routing[job1]) < N or int(Solutions[nurseno2].routing[job2]) >= N + N or int(Solutions[nurseno2].routing[job2]) < N :
                #or len(Solutions[nurseno1].routing)<job1 or len(Solutions[nurseno2].routing)<job2:
                job1 = random.randint(1, len(Solutions[nurseno1].routing)-1)
                job2 = random.randint(1, len(Solutions[nurseno2].routing)-1)

             #   print("2 # from  nurseno1  job1", job1)
             #   print("2 # from  nurseno2job2", job2)
                i += 1

            if Incompat[nurseno1][int(Solutions[nurseno2].routing[job2]) - N] != 0 and Incompat[nurseno2][int(Solutions[nurseno1].routing[job1]) - N] != 0:  # and Routing[nurseno1][job1] Routing[nurseno2][job2]:
               # print("vertical swap is occured between jobs ")
                Solutions[int(nurseno1)].change = 1
                Solutions[int(nurseno2)].change = 1
                swap = int(Solutions[nurseno1].routing[job1])
                Solutions[nurseno1].routing[job1] = (Solutions[nurseno2].routing[job2])
                (Solutions[nurseno2].routing[job2]) = str(swap)
            #    print("vertical swap is occured between jobs in ", Solutions[nurseno1].routing,Solutions[nurseno2].routing)
        return Solutions

    def verticalinsert(self, N, Solutions, Incompat):
      #  print("verticalinsert")
        import random
        nurseno1 = random.randint(0, (N-1))  # determine the nurse first
        nurseno2 = random.randint(0, (N-1))  # determine the nurse first

        while len(Solutions[nurseno1].routing) < 2:  # if selected nurse is not a free nurse
            nurseno1 = random.randint(0, (N - 1))  # determine the nurse

        while len(Solutions[nurseno1].routing) < 2:  # if selected nurse is not a free nurse
            nurseno2 = random.randint(0, (N - 1))  # determine the nurse

       # i = 0
        #print("nurseno", nurseno1,nurseno2)
        if len(Solutions[nurseno1].routing) > 2 and len(Solutions[nurseno2].routing) > 2 and nurseno1 != nurseno2:  # if selected nurse is a free nurse
            job1 = random.randint(0, len(Solutions[nurseno1].routing) - 1)  # from  nurseno1
            location = random.randint(0, len(Solutions[nurseno2].routing) - 1)  # from  location

            while int(Solutions[nurseno1].routing[job1]) >= N + N or int(Solutions[nurseno1].routing[job1]) < N  or int(Solutions[nurseno2].routing[location]) >= N + N or int(Solutions[nurseno2].routing[location]) < N:
            #len(Solutions[nurseno1].routing) < job1 or len(Solutions[nurseno2].routing) < location
                job1 = random.randint(1, len(Solutions[nurseno1].routing) - 1)
                location = random.randint(1, len(Solutions[nurseno2].routing) - 1)

             #   i += 1

          #  print("vertical insert is occured between jobs out ", i, nurseno1, nurseno2, Routing[nurseno1][job1],Routing[nurseno2][location])
            if Incompat[nurseno2][int(Solutions[nurseno1].routing[job1])-N] != 0 :
         #       print("vertical insert is occured between jobs in ", Solutions[nurseno2].routing,location)
                Solutions[int(nurseno1)].change = 1
                Solutions[int(nurseno2)].change = 1
                Solutions[nurseno2].routing.insert(location,  Solutions[nurseno1].routing[job1])
           #     print("dfvb ",Solutions[nurseno2].routing)
        return Solutions

    def horizontalswap(self, N, Solutions):
      #  print("horizontalswap")

        import random
        nurseno = random.randint(0, (N-1))  # determine the nurse first
        i=0
        while (len(Solutions[nurseno].routing)<3) and i<(N+N):  # if selected nurse is not a free nurse
            nurseno = random.randint(0, (N-1))  # determine the nurse first
            i+=1
         #   print("1 nurseno", nurseno, Solutions[nurseno].routing, (len(Solutions[nurseno].routing)))
      #  print("2 nurseno", nurseno,Solutions[nurseno].routing,(len(Solutions[nurseno].routing)))
        if (len(Solutions[nurseno].routing)>2):  # if selected nurse is a not free nurse
            job1 = random.randint(0, (len(Solutions[nurseno].routing)-1))
            job2 = random.randint(0, (len(Solutions[nurseno].routing)-1))
          #  print("1 job1", job1)
         #   print("1 job2", job2)
            while int(Solutions[nurseno].routing[job1]) <N or int(Solutions[nurseno].routing[job1])>=N+N :
                job1 = random.randint(0, (len(Solutions[nurseno].routing)-1))
               # print("2 job1", nurseno, job1, Routing[nurseno][job1])
          #      i1+=1
         #   print("****2 job1", nurseno, job1, Solutions[nurseno].routing[job1])
            while int(Solutions[nurseno].routing[job1]) == int(Solutions[nurseno].routing[job2]) or int(Solutions[nurseno].routing[job2]) < N or int(Solutions[nurseno].routing[job2]) > N + N:
                job2 = random.randint(0, (len(Solutions[nurseno].routing)-1))
           #     print("2 job2",nurseno, job2,Routing[nurseno][job2])
           #     i2 += 1
          #  print("**2 job2", nurseno, job2, Solutions[nurseno].routing[job2])
           # print(" Horizontal swap is occured between jobs",Solutions[nurseno].routing[job1], Solutions[nurseno].routing[job2])
          #  print("2  Routing", Solutions[nurseno].routing)
            Solutions[int(nurseno)].change = 1
            swap = Solutions[nurseno].routing[job1]
            Solutions[nurseno].routing[job1] = Solutions[nurseno].routing[job2]
            Solutions[nurseno].routing[job2] = swap
         #   print("2  Routing",Solutions[nurseno].routing)
        return Solutions

    def horizontalsinsert(self, N, Solutions):
        # print("horizontalsinsert")
        """
        print("\n-ls hi--Solutions")
        for i in Solutions:
            if len(i.routing) > 1:
                i.printinfo3()
        """
        import random
        nurseno = random.randint(0, (N - 1))  # determine the nurse first
        i=0
        while (len(Solutions[nurseno].routing) < 3 and i<(N+N)):  # if selected nurse is not a free nurse
            nurseno = random.randint(0, (N - 1))  # determine the nurse first
            i+=1
        #print("1  Routing", Solutions[int(nurseno)].routing)
        if (len(Solutions[nurseno].routing)>2):  # if selected nurse is a not free nurse
            job1 = random.randint(0, (len(Solutions[nurseno].routing)-1))
            location = random.randint(0, (len(Solutions[nurseno].routing)-1))
         #   print("2  Routing", Solutions[int(nurseno)].routing,job1,location)
            while int(Solutions[nurseno].routing[job1]) < N or int(Solutions[nurseno].routing[job1]) >= N + N:
                job1 = random.randint(0, (len(Solutions[nurseno].routing)-1))
         #   print("3  Routing", Solutions[int(nurseno)].routing, job1, location)
            while int(Solutions[nurseno].routing[job1]) == int(Solutions[nurseno].routing[location]) or int(Solutions[nurseno].routing[location]) < N or int(Solutions[nurseno].routing[location]) > N + N:
                location = random.randint(0, (len(Solutions[nurseno].routing)-1))
          #  print(" seçilen iş", Solutions[nurseno].routing[job1],location)
            Solutions[int(nurseno)].change = 1
            hold = Solutions[nurseno].routing[job1]
            del Solutions[int(nurseno)].routing[job1]
            Solutions[nurseno].routing.insert(location, str(hold))
           # print("2  Routing", Solutions[nurseno].routing)
        return Solutions

    def onerouteterminator(self, N, Solutions,Incompat):
        import random
        onejob=-1
        nurse1=-1
        nurseno=-1
        nurse2=[]
        for i in Solutions: # first find the route with one-job
            if len(i.routing) == 2:
                onejob=int(i.routing[1])
                nurse1 = int(i.routing[0])
        for i in Solutions:
            if len(i.routing) > 2 and nurse1!=-1:
                nurse2.append((i.routing[0]))



        #print("*****nurseno ",nurse1,nurse2)
        if  nurse1 != -1:

            nurseno = random.randint(0, len(nurse2) - 1)  # determine the nurse first
            nurseno = int(nurse2[int(nurseno)])
            #print("*****nurseno ", nurse1, nurse2, nurseno)
            if Incompat[nurseno][onejob - N] != 0:
                    location = random.randint(1, (len(Solutions[nurseno].routing) - 1))
                    #print("ONE route terminated ",Solutions[int(nurse1)].routing,Solutions[nurseno].routing)
                    Solutions[int(nurse1)].change = 1
                    Solutions[nurseno].change = 1
                    hold = Solutions[nurse1].routing[1]
                    del Solutions[int(nurse1)].routing[1]
                    Solutions[nurseno].routing.insert(location, str(hold))
                    onejob = -1
                    nurse1 = -1
               #     print("ONE job route terminated ", Solutions[int(nurse1)].routing, Solutions[nurseno].routing)
                   # nurse2[nurseno] = -1

        return Solutions
