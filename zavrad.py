from github import Auth
from github import Github
import sys

githubToken=sys.argv[1]
auth = Auth.Token(githubToken)

g = Github(auth=auth)

def postociJezika(jezici):
    suma=0
    povratnaVrijednost=""
    for jezik in jezici:
        suma+=jezici[jezik]
    for jezik in jezici:
        povratnaVrijednost+="\n"+jezik+" "+"{:.2f}".format(jezici[jezik]/suma*100)+"%"
    return povratnaVrijednost

class repozitorijOsnovniPodaci:
    def __init__(self, repo):
        self.ime = repo.name
        self.doprinositelji = repo.get_contributors()
        self.jezici = repo.get_languages()
        self.stvoren = repo.created_at

    def ispisiSve(self):
        print("\nIme direktorija:", self.ime)
        podaci.write("\n\nStvoreno:\n" + str(self.stvoren.date()))
        print("\nDoprinositelji:")
        for doprinositelj in self.doprinositelji:
            print(doprinositelj.login)
        print("\nJezici:")
        postociJezika(self.jezici)

    def upisiSveOsnovniPodaci(self, podaci):
        podaci.write("Ime direktorija:\n"+self.ime)
        podaci.write("\n\nStvoreno:\n" + str(self.stvoren.date()))
        podaci.write("\n\nDoprinositelji:")
        for doprinositelj in self.doprinositelji:
            podaci.write("\nIme-"+str(doprinositelj.name)+" prijava-"+doprinositelj.login)
        podaci.write("\n\nJezici:")
        podaci.write(postociJezika(self.jezici))
        podaci.write("\n\n\n")

podaci=open("podaciOsnovni.txt", "a")
obradeniR=open("obradeniOsnovni.txt", "r")
obradeniA=open("obradeniOsnovni.txt", "a")
brojac=0
obradeniR=obradeniR.read().split("\n")

for repo in g.get_user().get_repos():
    if(repo.name not in obradeniR):
        repozitorijOsnovniPodaci(repo).upisiSveOsnovniPodaci(podaci)
        obradeniA.write(repo.name+"\n")
        print(brojac)
print()

#drugi dio ispisa

class repozitorijSadrzaj:
    def __init__(self, repo):
        self.ime = repo.name
        self.sadrzaj = repo.get_contents("")
        self.korjenskaStrukturaRepozitorija={}
        self.dubinskaStrukturaRepozitorija=[]
        self.selenium = False
        sadrzajKopija=self.sadrzaj.copy()
        while sadrzajKopija:
            datotekaSadrzaj = sadrzajKopija.pop(0)
            if datotekaSadrzaj.type == "dir":
                sadrzajKopija.extend(repo.get_contents(datotekaSadrzaj.path))
            elif datotekaSadrzaj.type == "file":
                if "pom.xml"==datotekaSadrzaj.name.lower() or "package.json"==datotekaSadrzaj.name.lower():
                    seleniumSadrzaj = repo.get_contents(datotekaSadrzaj.path).decoded_content.decode("utf-8")
                    if("selenium" in str(seleniumSadrzaj)):
                        self.selenium=True
                        break
        self.ReadMe=None
        self.licenca=None
        try:
            self.ReadMe = repo.get_readme()
        except:
            self.ReadMe = False
        try:
            self.licenca = repo.get_license()
        except:
            self.licenca = False

    def upisiSveSadrzaj(self, podaci):
        podaci.write("Ime direktorija:\n"+self.ime)
        podaci.write(self.ime+"\n\nKorijenska struktura direktorija:\n")
        for i in self.korjenskaStrukturaRepozitorija:
            podaci.write(i)
            for j in self.korjenskaStrukturaRepozitorija[i]:
                podaci.write("|" + j + ":" + str(self.korjenskaStrukturaRepozitorija[i][j]))
            podaci.write("\n")
        podaci.write("\nDubinska struktura direktorija:\n")
        for i in self.dubinskaStrukturaRepozitorija:
            podaci.write(i)
            for j in self.dubinskaStrukturaRepozitorija[i]:
                podaci.write("|" + j + ":" + str(self.dubinskaStrukturaRepozitorija[i][j]))
            podaci.write("\n")
        if(self.ReadMe==False):
            podaci.write("\nRepozitorij ne sadrzi ReadMe\n")
        else:
            podaci.write("\nRepozitorij sadrzi ReadMe\n")
        if(self.licenca==False):
            podaci.write("\nRepozitorij ne sadrzi licencu\n")
        else:
            podaci.write("\nRepozitorij sadrzi licencu\n")
        if (self.selenium == False):
            podaci.write("\nRepozitorij ne koristi Selenium alat za testiranje\n")
        else:
            podaci.write("\nRepozitorij koristi Selenium alat za testiranje\n")
        podaci.write("\n\n\n")

podaci=open("podaciSadrzaj.txt", "a")
obradeniR=open("obradeniSadrzaj.txt", "r").read().split("\n")
obradeniA=open("obradeniSadrzaj.txt", "a")

nastavciStraznjegKraja=["py", "java", "cpp", "c", "cs"]
nastavciPrednjegKraja=["html", "css", "js", "ts", "php", "dart", "tsx", "jsx", "ejs"]
brojacTrganja=0
savSadrzajDirektorija=[]
for repo in g.get_user().get_repos():
    if repo.name in obradeniR:
        continue
    print(repo.name)
    repozitorij=repozitorijSadrzaj(repo)
    for datoteka in repozitorij.sadrzaj:
        if datoteka.type == "dir":
            savSadrzajDirektorija.append(datoteka)
            # print(file.name)
            sadrzajDirektorija = repo.get_contents(datoteka.path)
            for i in sadrzajDirektorija:
                if i.type=="dir":
                    savSadrzajDirektorija.append(i)
            sadrzajDatoteka=[]
            while sadrzajDirektorija:
                content=sadrzajDirektorija.pop(0)
                if(content.type=="dir"):
                    sadrzajDirektorija.extend(repo.get_contents(content.path))
                    for c in repo.get_contents(content.path):
                        if c.type=="dir":
                            savSadrzajDirektorija.append(c)
                else:
                    sadrzajDatoteka.append(content)
    sadrzajDubinskihDirektorija={}
    for j in savSadrzajDirektorija:
        dictionary={"back":0, "front":0, "doc":0}
        types=[]
        try:
            if(repo.get_contents(j.path) is not []):
                for i in repo.get_contents(j.path):
                    if i.name.split(".")[-1] in nastavciStraznjegKraja:
                        dictionary["back"]+=1
                    elif i.name.split(".")[-1] in nastavciPrednjegKraja:
                        dictionary["front"]+=1
                    elif i.name.split(".")[-1]=="tex":
                        dictionary["doc"]+=1
                for i in dictionary:
                    if dictionary[i] > 0:
                        types.append(i)
                if set(dictionary.values())!={0}:
                    print(j.path)
                    sadrzajDubinskihDirektorija[j.path]={}
                    for k in dictionary:
                        if dictionary[k]>0:
                            print(dictionary[k], k)
                            sadrzajDubinskihDirektorija[j.path][k]=dictionary[k]
                    print()
        except:
            print("Direktorij nije bilo moguce otvoriti")
    print(sadrzajDubinskihDirektorija)
    sadrzajKorijesnogDirektorija={}
    for i in sadrzajDubinskihDirektorija:
        if i.split("/")[0] not in sadrzajKorijesnogDirektorija:
            sadrzajKorijesnogDirektorija[i.split("/")[0]]=sadrzajDubinskihDirektorija[i]
        else:
            for j in sadrzajDubinskihDirektorija[i]:
                if j not in sadrzajKorijesnogDirektorija[i.split("/")[0]]:
                    sadrzajKorijesnogDirektorija[i.split("/")[0]][j]=sadrzajDubinskihDirektorija[i][j]
                else:
                    sadrzajKorijesnogDirektorija[i.split("/")[0]][j]+=sadrzajDubinskihDirektorija[i][j]
    print(sadrzajKorijesnogDirektorija)
    repozitorij.dubinskaStrukturaRepozitorija=sadrzajDubinskihDirektorija
    repozitorij.korjenskaStrukturaRepozitorija=sadrzajKorijesnogDirektorija
    repozitorij.upisiSveSadrzaj(podaci)
    obradeniA.write(repozitorij.ime + "\n")
    # if brojacTrganja==1:
    #     break
    # brojacTrgana+=1
    sadrzajKorijesnogDirektorija={}
    savSadrzajDirektorija=[]
    sadrzajDirektorija=[]