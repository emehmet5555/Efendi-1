class Remove:  # Heuristic class is defined here
    def __init__(self,scoreremove,weightremove,numberofremoves):
        # scores and weight are defined here
        self.scoreremove = scoreremove  # 8
        self.weightremove = weightremove # 8
        self.numberofremoves = numberofremoves # number of iterations used

    def printinfo(self):
        print("""scoreremove:{}-weightremove: {}-numberofremoves:{}""".format(self.scoreremove, self.weightremove, self.numberofremoves))

    def adduncoveredjob(self,Solutions,component):
        self.Solutions[0].uncoveredjob.append(component)

    def randomremove(self,N,Solutions):
        import random
       # print("removal 1 starts")
        nurseno = random.randint(0, N-1)  # determine the nurse first
        while (len(Solutions[int(nurseno)].routing)==1):  # if selected nurse is not a free nurse
             nurseno = random.randint(0, N-1)  # determine the nurse first

        if (len(Solutions[nurseno].routing)>1):  # if selected nurse is not a free nurse
            counter = 0
            jobno = random.randint(0, int(len(Solutions[int(nurseno)].routing)))  # determine the job second
            while jobno==0 or len(Solutions[nurseno].routing)==jobno or int(Solutions[int(nurseno)].routing[int(jobno)]) >= (N+N) and counter <=N+N:#
                jobno = random.randint(0, int(len(Solutions[int(nurseno)].routing)))  # determine the job second
                counter += 1
            if int(Solutions[int(nurseno)].routing[int(jobno)]) < (N+N):
                if Solutions[0].uncoveredjob==['-1']:
                    Solutions[0].uncoveredjob=[str(int(Solutions[int(nurseno)].routing[jobno]))]
                elif (Solutions[0].uncoveredjob)!=['-1']:
                    Solutions[0].uncoveredjob.append(str((Solutions[int(nurseno)].routing[jobno])))

            del  Solutions[int(nurseno)].routing[jobno]
            Solutions[int(nurseno)].change=1


    def randomremove2(self,N,Solutions): # n number of jobs removed randomly
        import random
       # print("removal2 1")
        jobnumbers=random.randint(round(0.1*N), round(0.4*N))
        i=1
        while  i<jobnumbers:# or jobnumbers > len(Solutions[int(0)].uncoveredjob):
             self.randomremove(N, Solutions)
             i=i+1

    def randomremove3(self,N,Solutions,Dmatris):
     #   print("******Randomremove3")
        import random
        Array = []
        Ratio=[]
        Name=[]
        numbers=0
        for i in Solutions:
            if len(i.routing) >1:
                Array.append(i.obj)
                Name.append(i.routing[0])
                numbers+=1
        hold = 0
        for i in Array:
            hold+=(float(i/sum(Array)))
            Ratio.append(hold)

        proportion = random.random()  # determine random number
        nurseno=0
        for i in range(0, numbers-1): # roulette wheel selection
            if Ratio[i]<proportion:
                nurseno=i+1

        jobnumber = random.randint(round(0.1 * N), round(0.4 * N))
     # burada worst remove n kez çalistirilacak
        i = 0
        while i<=jobnumber:
            self.worstremove2(N,Solutions,Dmatris,int(Name[nurseno]))
            i = i + 1


    def worstremove2(self, N,Solutions,Dmatris,nurseno):
        big = 0
        job1 = 0
        for j in range(0, len(Solutions[nurseno].routing)> - 1):
            if (j + 2 < len(Solutions[nurseno].routing)):
                dist =  int(Dmatris[int(Solutions[nurseno].routing[j])][int(Solutions[nurseno].routing[j + 1])])
                dist +=  int(Dmatris[int(Solutions[nurseno].routing[j+1])][int(Solutions[nurseno].routing[j + 2])])
                if big < dist:
                    job1 = j
                    big = dist
                    if job1 == 0 and big != 0:
                       job1 = 1

            if (int(Solutions[nurseno].routing[job1]) >= N and int(Solutions[nurseno].routing[job1])< N + N):  # if selected nurse is not a free nurse
                i = job1  # assign
                if Solutions[0].uncoveredjob == ['-1']:
                    Solutions[0].uncoveredjob = [str(int(Solutions[int(nurseno)].routing[job1]))]
                elif (Solutions[0].uncoveredjob) != ['-1']:
                    Solutions[0].uncoveredjob.append(str((Solutions[int(nurseno)].routing[job1])))
                del Solutions[int(nurseno)].routing[job1]
                Solutions[int(nurseno)].change = 1

    def worstremove(self,N,Solutions,Dmatris):
       # print("Worst removal 1")
        big=0
        job1=0
        for i in Solutions:
            if len(i.routing) > 2:
                for j in range(0, len(i.routing)):
                    if (j+2<len(i.routing)):
                        dist = int(Dmatris[int(i.routing[j])][int(i.routing[j + 1])])
                        dist+= int(Dmatris[int(i.routing[j+1])][int(i.routing[j + 2])])
                    if big < dist:
                        nurseno=int(i.routing[0])
                        job1=j
                        big=dist
                        if job1 == 0 and big != 0:
                            job1 = 1


        if (job1!= 0 and int(Solutions[nurseno].routing[job1]) < N+N):  # if selected nurse is not a free nurse
            i =job1 #assign
            if Solutions[0].uncoveredjob == ['-1']:
                Solutions[0].uncoveredjob = [str(int(Solutions[int(nurseno)].routing[job1]))]
            elif (Solutions[0].uncoveredjob) != ['-1']:
                Solutions[0].uncoveredjob.append(str((Solutions[int(nurseno)].routing[job1])))
            del Solutions[int(nurseno)].routing[job1]
            Solutions[int(nurseno)].change = 1

    def randomEVremove(self,N,Solutions):
        import random

        nurseno = random.randint(0, (N-1))  # determine the nurse first
        while len(Solutions[nurseno].routing)<2:  # if selected nurse is not a free nurse
            nurseno = random.randint(0, (N-1))  # determine the nurse first

        i = 0
        while int(len(Solutions[nurseno].routing)) != 1:
            if Solutions[0].uncoveredjob == ['-1'] and int(Solutions[int(nurseno)].routing[len(Solutions[nurseno].routing)-1])<N+N :
                Solutions[0].uncoveredjob = [str(int(Solutions[int(nurseno)].routing[len(Solutions[nurseno].routing)-1]))]
            elif (Solutions[0].uncoveredjob) != ['-1'] and int(Solutions[int(nurseno)].routing[len(Solutions[nurseno].routing)-1]) < N+N :
                Solutions[0].uncoveredjob.append(str((Solutions[int(nurseno)].routing[len(Solutions[nurseno].routing)-1])))
            Solutions[int(nurseno)].routing.pop()
            Solutions[int(nurseno)].change = 1
            i+=1

    def worsttimeremove(self,N,Solutions,Dmatris):
      #  print("Worsttime removal 1")
        big = 0
        job1 = 0
        for i in Solutions:
            if len(i.routing) > 1 and  (len(i.routing)+1)*4==len(i.scheduling):
                for j in range(1, len(i.routing)):
                    if( float(i.scheduling[4*j]) == float(i.scheduling[4*j+1]) ): # calculate the idle time
                        time=float(i.scheduling[4*j])-float(i.scheduling[(4*(j-1)+2)])
                        time +=float(int(Dmatris[int(i.routing[j-1])][int(i.routing[j])])/50*60)
                        if big < time:
                            nurseno = int(i.routing[0])
                            job1 = j
                            big = time


        if (job1 != 0 and int(Solutions[nurseno].routing[job1]) < N + N):  # if selected nurse is not a free nurse
            i = job1
            if Solutions[0].uncoveredjob == ['-1']:
                Solutions[0].uncoveredjob = [str(int(Solutions[int(nurseno)].routing[job1]))]
            elif (Solutions[0].uncoveredjob) != ['-1']:
                Solutions[0].uncoveredjob.append(str((Solutions[int(nurseno)].routing[job1])))
            del Solutions[int(nurseno)].routing[job1]
            Solutions[int(nurseno)].change = 1

    def assignzeros(self, N, vector):  # N zero vector
        i = 0
        while i < N:
            vector.append(0)
            i = i + 1
        return vector

    def stationremove(self,N,Solutions):
        import random
        Visit = 0
        EVvisit = []
        self.assignzeros(N, EVvisit)
        k=0
        for i in Solutions:
            if len(i.routing) > 1:
                for j in range(1, len(i.routing)):
                    if int(i.routing[j]) >= N + N:
                        Visit = 1
                        EVvisit[k] = 1
            k+=1
        if Visit != 0:
            nurseno = random.randint(0, (N - 1))  # determine the nurse first
            while EVvisit[nurseno] == 0:
                nurseno = random.randint(0, (N - 1))

            job1 = 0
            if len(Solutions[nurseno].routing)>1:  # if selected nurse is not a free nurse
                for j in range(1, len(Solutions[nurseno].routing)):
                        if (int(Solutions[nurseno].routing[j]) >= N + N):
                            job1 = j

            if (job1 != 0):
                Solutions[nurseno].routing.remove(Solutions[nurseno].routing[job1])
                Solutions[int(nurseno)].change = 1


    def chargetechremove(self,N,Solutions):
        import random
        Visit = 0
        EVvisit = []
        self.assignzeros(N, EVvisit)
        k = 0
        for i in Solutions:
            if len(i.routing) > 1:
                for j in range(1, len(i.routing)):
                    if int(i.routing[j]) >= N + N:
                        Visit = 1
                        EVvisit[k] = 1
            k += 1

        if Visit != 0:
            nurseno = random.randint(0, (N - 1))  # determine the nurse first
            while EVvisit[nurseno] == 0:
                nurseno = random.randint(0, (N - 1))

            job1 = 0
            if len(Solutions[nurseno].routing) > 1:  # if selected nurse is not a free nurse
                for j in range(1, len(Solutions[nurseno].routing)):
                    if (int(Solutions[nurseno].routing[j]) >= N + N):
                            Solutions[nurseno].chargetechnology = [str(0)]
                            Solutions[int(nurseno)].change = 1

            #!!!!!!!!!!!!!! more than one visits may be considered and check incase the infeasible!!!!!!!
