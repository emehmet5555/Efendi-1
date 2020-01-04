class Job:  # Job class is defined here
    def __init__(self,name,jtwa,jtwb,duration,requirement,genderfemale,gendermale,catownership,dogownership,smokinghabit):
        self.name=name
        self.jtwa = jtwa
        self.jtwb = jtwb
        self.duration = duration

        self.requirement = requirement

        self.genderfemale = genderfemale
        self.gendermale = gendermale
        self.catownership = catownership
        self.dogownership = dogownership
        self.smokinghabit = smokinghabit

    def printinfo(self):
        print("""
               Job objesinin özellikleri
               İsim:{}
               TWA:{}
               TWB:{}
               DURATION:{}
               REQUIREMENT:{}
               GENDERFEMALE:{}
               GENDERMALE:{}
               CATOWNERSHIP:{}
               DOGOWNERSHIP:{}
               SMOKINGHABIT:{}

               """.format(self.name, self.jtwa, self.jtwb, self.duration, self.requirement, self.genderfemale, self.gendermale,
                          self.catownership, self.dogownership, self.smokinghabit))
    def printscoreinfo(self):
        print("""İsim:{}, Score:{}""".format(self.name,  self.jobscore))
    def score(self,component1,component2,component3):
        # the weights of initial stage
        w1=0.5
        w2=0.3
        w3=0.2
        #component1=(jtwb-jtwa)/(maxjtwb-minjtwa)
        # component2=(duration)/(total duration)
        # component3=(requirement)/(total requirement)
        self.jobscore=w1*(component1)+w2*(component2)+w3*(component3)

    def takeSecond(self,elem):
        return elem[1]

    def takeFirst(self,elem):
        return elem[0]

    # this function calculates the scores for each job
    def Scorejob(self,Jobs):
        j = 0
        minjtwa = 1000
        maxjtwb = 0
        totalduration = 0
        totalrequirement = 0
        ratio = []
        ratio2 = []
        difference = []
        Order = []
        Otwa = []
        Score = []
        for i in Jobs:
            if int(i.jtwa) < minjtwa:
                minjtwa = int(i.jtwa)
            if int(i.jtwb) > maxjtwb:
                maxjtwb = int(i.jtwb)
            difference.append((int(i.jtwb) - int(i.jtwa)))
            totalduration += int(i.duration)
            totalrequirement += int(i.requirement)
        # print("--min- max-------",totalduration,i.duration)

        for i in difference:
            ratio.append(i / (maxjtwb - minjtwa))

        # print("++++",ratio,sum(ratio))
        for i in ratio:
            ratio2.append(sum(ratio) / i)
        ratio = []
        for i in ratio2:
            ratio.append(i / sum(ratio2))
        # the ratio holds the score for the time window
        j = 0
        for i in Jobs:
            i.score(ratio[j], (int(i.duration) / totalduration), int(i.requirement) / totalrequirement)
            #    i.printscoreinfo()
            Order.append(j)
            Otwa.append(int(i.jtwa))
            Score.append(i.jobscore)
            j = j + 1
        # these lines calculate the the order of jobs according to the their score
        Order = [[x, y] for x, y in zip(Order, Score)]
        #  print("Orderjob11 ", Order)
        self.takeSecond(Order)
        Orderjob = sorted(Order, key=self.takeSecond, reverse=True)
        j = 0
        for i in Orderjob:
            Order[j] = self.takeFirst(i)
            j = j + 1
        print("Orderjob", Order)

        # jobs squencing according to the twa
        Otwa = [[x, y] for x, y in zip(Order, Otwa)]
        # takeSecond(Otwa)
        Orderjob = sorted(Otwa, key=self.takeSecond, reverse=False)
        j = 0
        for i in Orderjob:
            Order[j] = self.takeFirst(i)
            j = j + 1
        print("revised Orderjob", Order)

        return Order



    def OrderJTwa(self,Solutions,Jobs,N): # order first wrt jtwa and then generate scheduling variable
      for i in Solutions:
          if len(i.routing) >= 2:
              hold = []
              holdtwa = []
              hold2=[]
              for j in range(0, len(i.routing)):
                  if int(i.routing[j]) >= N and int(i.routing[j]) < N + N:
                       hold.append(int(i.routing[j]))
                       holdtwa.append(int(Jobs[(int(i.routing[j])-N)].jtwa))

              hold2 = [[x, y] for x, y in zip(hold, holdtwa)]
              hold2 = sorted(hold2, key=self.takeSecond, reverse=False)
              j = 0
              for k in hold2:
                  hold[j] = self.takeFirst(k)
                  i.routing[j+1]=str(self.takeFirst(k))
                  j = j + 1
