class Heuristic ():
    def __init__(self,Bestobj,Currentobj,Sprimeobj):
        self.Bestobj = Bestobj      # Best solution
        self.Currentobj = Currentobj   # solution S
        self.Sprimeobj = Sprimeobj  # # solution S' generated from S
    # neighbourhoods or destroy-repair operators generated here
    def neighbourhood(self,Remove,Repair):
        # there are 5 repair and 8 remove operators
        import Classrepair
        import Classremove
        i = 0
        while (i < 8):
            Rem = Classremove.Remove(0, 1, 0)
            Remove.append(Rem)
            i = i + 1
        i = 0
        while (i < 5):
            Rep = Classrepair.Repair(0, 1, 0)
            Repair.append(Rep)
            i = i + 1

    # Total objective funtion is computed here
    def totalobjectivefuntion(self,Solutions):
        Totalobj =0
        for i in Solutions:
           # print("----i.obj---------",i.obj)
            Totalobj+=i.obj
        #print("----Totalobj--------", Totalobj)
        return Totalobj

        # Total objective funtion is computed here
    def totalobj(self, Solutions):
        Totalobj = 0
        for i in Solutions:
            if len(i.routing) > 1:
               i.obj=float(i.workercost)*0.5+float(i.distance)*0.077
            Totalobj += i.obj
            # print("----Totalobj--------", Totalobj)
        return Totalobj

    # score of each operator is computed here
    def scoreadjust(self, Solutions,Bestsolutions,Currentsolutions ,Repair, Remove, iteration,T,whichremove,whichrepair):
        # there are 5 repair and 8 remove operators
        import math
        import random
        import copy
        alfa1 = 10
        alfa2 = 7
        alfa3 = 3
        bad = 500
        check = 0
        u=0
        Aexp=0
      #  print("*******Scoreadjust********",iteration)

        if iteration == 0:
            self.Currentobj = self.totalobjectivefuntion(Solutions)
            self.Bestobj = self.Currentobj # initial solution is assigned as the best solution
            self.Sprimeobj= self.Currentobj
            Bestsolutions = copy.deepcopy(Solutions) # initial solution is assigned as the best solution
            Currentsolutions= copy.deepcopy(Solutions)
        #print("*******Scoreadjust********",Bestsolutions[0].uncoveredjob,Currentsolutions[0].uncoveredjob,Solutions[0].uncoveredjob)

        if int(iteration) > 0:
            self.Sprimeobj = self.totalobjectivefuntion(Solutions)
            penalty = 0
            if len(Solutions[0].uncoveredjob) != 0:
                if Solutions[0].uncoveredjob[0] != str(-1):  # to eliminate uncovered job issue
                    penalty += 1000 * len(Solutions[0].uncoveredjob)

                #  print("self.Bestobj", self.Bestobj, self.Currentobj, self.Sprimeobj)
            elif float(self.Bestobj) > float(self.Sprimeobj) and penalty == 0:  # scores are adjusting for removals
                # print("*********BEST !!!!!!Sprimeobj",self.Bestobj, self.Sprimeobj)
                Remove[whichremove].scoreremove += alfa1
                Remove[whichremove].numberofremoves += 1
                Repair[whichrepair].scorerepair += alfa1
                Repair[whichrepair].numberofrepairs += 1
                check = 1

            elif self.Bestobj <= self.Sprimeobj and self.Sprimeobj < self.Currentobj and penalty == 0:
              #  print("not BEST not better than current!!!!!!", self.Currentobj)
                Remove[whichremove].scoreremove += alfa2
                Remove[whichremove].numberofremoves += 1
                Repair[whichrepair].scorerepair += alfa2
                Repair[whichrepair].numberofrepairs += 1
                check = 2

            elif self.Sprimeobj < (self.Currentobj + bad) and T > 1 and penalty == 0:  # Sprimeobj!=Currentobjtemprerature
             #   print("worse than current!!!!!! S' and current", self.Sprimeobj, self.Currentobj)
                Aexp = round(math.exp(-(self.Sprimeobj - self.Currentobj) / T), 4)
                u = round(random.uniform(0, 1), 4)  # generate random number

             #   print("!!!Aexp", Aexp, u, T)
                if u < Aexp and penalty == 0:
                    Remove[whichremove].scoreremove += alfa3
                    Remove[whichremove].numberofremoves += 1
                    Repair[whichrepair].scorerepair += alfa3
                    Repair[whichrepair].numberofrepairs += 1
                    check = 3

           # print("self.Bestobj out", self.Bestobj, self.Currentobj, self.Sprimeobj)
            if float(self.Bestobj) > float(self.Sprimeobj) and penalty == 0:  # scores are adjusting for removals
              #  print("*********BEST !!!!!", self.Bestobj, self.Sprimeobj)
                # print("Sprimeobj unc", Bestsolutions[0].uncoveredjob,Solutions[0].uncoveredjob)
                self.Bestobj = self.Sprimeobj
                self.Currentobj = self.Sprimeobj
                Bestsolutions = copy.deepcopy(Solutions)
                Currentsolutions = copy.deepcopy(Solutions)

            elif (self.Bestobj <= self.Sprimeobj and self.Sprimeobj < self.Currentobj) and penalty == 0:  # not best but better than current
              #  print("not BEST but better!!!!!", self.Bestobj, self.Currentobj, self.Sprimeobj)
                self.Currentobj = self.Sprimeobj
                Currentsolutions = copy.deepcopy(Solutions)


            elif self.Sprimeobj < (self.Currentobj + bad) and penalty == 0:
                if u < Aexp and penalty == 0:
                 #   print("worse than current!!!!!!", self.Currentobj)
                    self.Currentobj = self.Sprimeobj
                    Currentsolutions = copy.deepcopy(Solutions)

            if check == 0:
              #  print("Sprimeobj is deleted Currentobj", self.Sprimeobj, self.Currentobj)
                self.Sprimeobj = self.Currentobj
                Solutions = copy.deepcopy(Currentsolutions)
              #  print("Sprimeobj unc", Solutions[0].uncoveredjob)
                # Solutions[0].uncoveredjob = [str(-1)]

            """
            print("\n---Solutions")
            for i in Solutions:
                        if len(i.routing)>1:
                            i.printinfo3()

            """
        return (Solutions,Bestsolutions,Currentsolutions)

    # weight of each operator is computed here
    def weightadjust(self, Repair, Remove):
        rho = 0.25  #
       # print("Remove.weightremove")
        # for i in range(0, len(Remove.weightremove)):
        for i in Remove:
            if i.numberofremoves > 0:
                i.weightremove = (1 - rho) * i.weightremove + rho * i.scoreremove / i.numberofremoves
            elif i.numberofremoves == 0:
                i.weightremove = (1 - rho) * i.weightremove
        for i in Repair:
            if i.numberofrepairs > 0:
                i.weightrepair = (1 - rho) * i.weightrepair + rho * i.scorerepair / i.numberofrepairs
            elif i.numberofrepairs == 0:
                i.weightrepair = (1 - rho) * i.weightrepair

        #print("in----------   Weightremove,Weightrepair", Weightremove, Weightrepair)

    # repair and remove operators are selected here
    def drfinder(self, Solutions, Repair, Remove):

        import random
        whichremove = 0
        whichrepair = 0
        sumremove = 0
        sumrepair = 0
        for i in Remove:
            sumremove += float(i.weightremove)
        for i in Repair:
            sumrepair += float(i.weightrepair)

        Weightprobremove = []
        Removeroulette = []
        Weightprobrepair = []
        Repairroulette = []
        Solutions[0].assignzeros(7, Weightprobremove)
        Solutions[0].assignzeros(7, Removeroulette)

        Solutions[0].assignzeros(4, Weightprobrepair)
        Solutions[0].assignzeros(4, Repairroulette)

        for i in range(0, 7):
            Weightprobremove[i] = float(Remove[i].weightremove / sumremove)
            j = i
            while j < 7:
                Removeroulette[j] = Removeroulette[j] + Weightprobremove[i]
                j = j + 1

        for i in range(0, 4):
            Weightprobrepair[i] = float(Repair[i].weightrepair / sumrepair)
            j = i
            while j < 4:
                Repairroulette[j] = Repairroulette[j] + Weightprobrepair[i]
                j = j + 1

        Rem = 0
        Rep = 0
        Rem = random.uniform(0, 1)
        Rep = random.uniform(0, 1)

        for i in range(0, 7):
            if Removeroulette[i] <= Rem:
                whichremove = i
          #  Remove[0].printinfo()
        for i in range(0, 4):
            if Repairroulette[i] <= Rep:
                whichrepair = i
          #  Repair[0].printinfo()
      #  print("\nChosen Removeroulette, Repairroulette", Removeroulette,Rem, Repairroulette,Rep)
        Solutions[0].changeeliminate(Solutions)
        #print("Chosen whichremove, whichrepair", whichremove, whichrepair)

        return (whichremove, whichrepair)

    #ALNS is carried out here
    def alns(self,N, S,Solutions,Bestsolutions,Currentsolutions,Jobs,EVs, Repair, Remove,Maximumiteration,Dmatris,Incompat): # ALNS procedure is achieved here!!
        initialobj=self.totalobjectivefuntion(Solutions)
        T = initialobj * 0.5 / 0.69314718056
       # alfa=0.5
        whichremove = 0
        whichrepair = 0

        for iteration in range(0, Maximumiteration):
            Tk = T * 0.99
          # Tk = T / (1 + alfa * iteration ** 2)
            T = Tk
           # print(" iteration- temperature",iteration,Tk)
            ((Solutions,Bestsolutions,Currentsolutions))=self.scoreadjust(Solutions,Bestsolutions, Currentsolutions,Repair, Remove, iteration,T,whichremove,whichrepair)
            self.weightadjust(Repair, Remove)
            (whichremove, whichrepair) = self.drfinder(Solutions, Repair, Remove)

           # whichremove=7 #sil
            #whichrepair=0#sil
            if whichremove == 0:
              #  print("d0 in")
                Remove[0].randomremove(N, Solutions)
              #  print("d0 out")
            elif whichremove == 1:
              #  print("d1 in")
               Remove[0].randomremove2(N, Solutions) # n number of jobs removed randomly
             #   print("d1 out")
            elif whichremove == 2:
              #  print("d2 in")
               Remove[0].randomremove3(N, Solutions, Dmatris)
              #  print("d2 out")
            elif whichremove == 3:
              #  print("d3 in")
                Remove[0].worstremove(N, Solutions, Dmatris)
              #  print("d3 out")
            elif whichremove == 4:
              #  print("d4 in")
                Remove[0].randomEVremove(N, Solutions) # check hatalı
              #  print("d4 out")
            elif whichremove == 5:
               # print("d5 in")
               Remove[0].worsttimeremove(N, Solutions, Dmatris)
              #  print("d5 out")
            #elif whichremove == 6: #this is carried out in Calculateoverall2
            #    print("d6 in")
             #   Remove[0].stationremove(N, Solutions)
              #  print("d6 out")
          #  elif whichremove == 7: #this is carried out in Calculateoverall2
           #     print("d7 in")
              #  Remove[0].chargetechremove(N, Solutions)
               # print("d7 out")

            if whichrepair == 0:
              #  print("r0 in")
                Repair[0].randominsertion(N, Solutions, Jobs, Incompat)
              #  print("r0 out")
            elif whichrepair == 1:
              #  print("r1 in")
                Repair[0].cheapestinsertion(N, Solutions, Jobs, Dmatris, Incompat)
              #  print("r1 out")
            elif whichrepair == 2:
               # print("r2 in")
                Repair[0].leasttimeinsertion(N, Solutions, Jobs, Dmatris, Incompat)
               # print("r2 out")
           # elif whichrepair == 3:
           #   print("r3 in")
            #  Repair[0].neareststationinsertion(N, S, Solutions, Dmatris) #this is carried out in Calculateoverall2
              #  print("r3 out")
           # elif whichrepair == 4:
           #     print("r4 in")
              #  Repair[0].chargetechset(N, S, Solutions, Dmatris) #this is carried out in Calculateoverall2
              #  print("r4 out")
            # here sprime/ generated solution is updated
            Solutions[0].Calculateoverall2(N, S, Solutions, Jobs, EVs, Dmatris, Incompat)
           #
            #local search is achieved here
            if (iteration % 500)==0: # this is also a parameter
                self.localsearch(N,S, Solutions,Bestsolutions,Currentsolutions, Jobs, EVs,Repair,Dmatris, Incompat,self.Bestobj, self.Currentobj, self.Sprimeobj)
            #print("****************self.Bestobj***",self.Bestobj)
        return (Solutions,Bestsolutions,Currentsolutions)

    def localsearch(self,N,S, Solutions,Bestsolutions,Currentsolutions, Jobs, EVs,Repair,Dmatris, Incompat,Bestobj, Currentobj, Sprimeobj):
        #variable neighbourhood descend search based local search
        k = 1
        Maximumiteration2=400  # this is also a parameter
        for iteration2 in range(0, Maximumiteration2):
           # print("**iteration2**",iteration2,k)
          #  print("local search objs", Bestobj, Currentobj, Sprimeobj)

            if k == 1:
               Solutions=Repair[0].onerouteterminator(N, Solutions, Incompat)
               k=1
            if k == 2:
               Solutions=Repair[0].verticalswap(N, Solutions, Incompat)
               k=2
            elif k == 3:
               Solutions=Repair[0].verticalinsert(N, Solutions, Incompat)
               k=3
            elif k == 4:
                Solutions=Repair[0].horizontalswap( N, Solutions)
                k=4
            elif k == 5:
                Solutions=Repair[0].horizontalsinsert(N, Solutions)
                k=5
            Solutions[0].Calculateoverall2(N, S, Solutions, Jobs, EVs, Dmatris, Incompat)
            (k,Solutions,Bestsolutions,Currentsolutions,Bestobj, Currentobj, Sprimeobj)=self.keepsolution(Solutions, Bestsolutions, Currentsolutions,Bestobj, Currentobj, Sprimeobj, k)



    def keepsolution(self, Solutions, Bestsolutions, Currentsolutions,Bestobj, Currentobj, Sprimeobj, k):

        import copy
        check = 0
        Sprimeobj = self.totalobjectivefuntion(Solutions)

        if float(Bestobj) > float(Sprimeobj):  # scores are adjusting for removals
          #  print("keepsolution *********BEST !!!!!", Bestobj, Sprimeobj)
            Bestobj = Sprimeobj
            Currentobj = Sprimeobj
            Bestsolutions = copy.deepcopy(Solutions)
            Currentsolutions = copy.deepcopy(Solutions)
            check=1

        if (float(Currentobj) < float(Sprimeobj) and check!=1) :  # if it is not the best than delete it
            k = k + 1
            if k >= 6:
                k = 1
           # print("delete s'", self.Bestobj, self.Currentobj, self.Sprimeobj)
            Sprimeobj=Currentobj
            Solutions= copy.deepcopy(Currentsolutions)
        """
        print("\n-ls--Solutions")
        for i in Solutions:
            if len(i.routing) > 1:
                i.printinfo3()
        """


        return (k,Solutions,Bestsolutions,Currentsolutions,Bestobj, Currentobj, Sprimeobj)
