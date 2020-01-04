class Ev:  # nurse or EV class is defined here

    def __init__(self, name, etwa, etwb, experience, genderfemale, gendermale, catallergy, dogallergy, smokingallergy,cost,assignedjobs):
        self.name = name
        self.etwa = etwa
        self.etwb = etwb

        self.experience = experience

        self.genderfemale = genderfemale
        self.gendermale = gendermale
        self.catallergy = catallergy
        self.dogallergy = dogallergy
        self.smokingallergy = smokingallergy
        self.cost = cost

        self.assignedjobs=assignedjobs
       # self.uncoveredjob=uncoveredjob

    def printinfo(self):
        print("""
        Nurse/EV objesinin özellikleri
        İsim:{}
        TWA:{}
        TWB:{}
        EXPERIENCE:{}
        GENDERFEMALE:{}
        GENDERMALE:{}
        CATALLERGY:{}
        DOGALLERGY:{}
        SMOKINGALLERGY:{}
        COST:{}
        """.format(self.name, self.etwa, self.etwb, self.experience, self.genderfemale, self.gendermale,
                   self.catallergy,
                   self.dogallergy, self.smokingallergy, self.cost))

    def printscoreinfo(self):
        print("""İsim:{}, Score:{}""".format(self.name, self.evscore))

    def score(self, component1, component2):
        w1 = 0.7
        w2 = 0.3
        # component1=(wtwb-wtwa)/(maxjtwb-minjtwa)
        # component3=(experience)/(total experience)
        self.evscore = w1 * (component1) + w2 * (component2)

    def takeSecond(self, elem):
        return elem[1]

    def takeFirst(self, elem):
        return elem[0]

    def Scoreev(self,EVs):
        j = 0
        minetwa = 1000
        maxetwb = 0
        totalexperience = 0
        ratio = []
        ratio2 = []
        difference = []
        Order = []
        Ordere = []
        Score = []
        for i in EVs:
            if int(i.etwa) < minetwa:
                minetwa = int(i.etwa)
            if int(i.etwb) > maxetwb:
                maxetwb = int(i.etwb)
            difference.append((int(i.etwb) - int(i.etwa)))
            totalexperience += int(i.experience)

        for i in difference:
            ratio.append(i / (maxetwb - minetwa))

        for i in ratio:
            ratio2.append(i / sum(ratio))

        # the ratio2 holds the score for the time window
        j = 0
        for i in EVs:
            i.score(ratio2[j], int(i.experience) / totalexperience)
            #       i.printscoreinfo()
            Order.append(j)
            Score.append(i.evscore)
            j = j + 1
        # these lines calculate the the order of EVS according to the their score
        Ordere = [[x, y] for x, y in zip(Order, Score)]
        #  print("Orderjob11 ", Order)
        self.takeSecond(Ordere)
        Orderev = sorted(Ordere, key=self.takeSecond, reverse=True)
        j = 0
        for i in Orderev:
            Ordere[j] = self.takeFirst(i)
            #  print(takeFirst(i))
            j = j + 1
        print("OrderEV", Ordere)
        return Ordere

    def addjob(self,job):
        print("EV*****", job,AAA)
        self.AAA.append(job)

    def assign2zeros(self,N, vector):  # NxN zero matrix
        for j in range(N):
            column = []
            for i in range(N):
                column.append(0)
            vector.append(column)
        return vector

    def assign1ones(self,N, vector):  # NxN 1 matrix
        for j in range(N):
            column = []
            for i in range(N):
                column.append(1)
            vector.append(column)
        return vector

    # compatibility issue is concerning here*****************************
    def compatibility(self,Compat, Incompat,i,j, genderfemale, gendermale, catallergy, dogallergy, smokingallergy,jgenderfemale,
                      jgendermale,catownership,dogownership,smokinghabit, etwa, etwb, jtwa,jtwb,duration, experience,requirement,jobscore):
                #i= EV, j = job
            Compat[i][j] += int(genderfemale)*int(jgenderfemale)
            Compat[i][j] += int(gendermale) * int(jgendermale)
            Compat[i][j] += int(catallergy) * int(catownership)
            Compat[i][j] += int(dogallergy) * int(dogownership)
            Compat[i][j] += int(smokingallergy) * int(smokinghabit)
            if int(Compat[i][j]) == 1:
                Incompat[i][j] = 0
            if int(requirement) > int(experience):  # competence imcompatibility
                Incompat[i][j] = 0
            if (int(etwa) > int(jtwb)):   # case 2 drop outside
                Incompat[i][j] = 0
            if  (int(etwb) < int(jtwa)):
                Incompat[i][j] = 0
            Incompat[i][j] = Incompat[i][j] * jobscore

            return Incompat



