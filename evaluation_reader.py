import os
import xml.etree.ElementTree as ET
from pprint import pprint
from collections import Counter
import json
import sys

#une fonction qui prend en paramètre la racine du fichier XML et retourne les données de la personne avec le genre donné en paramètre ("Female" ou "Male")
def get(root,gender):
    dict={}
    track=root.find('body/track[@name="'+gender+'.Emotion"]')
    for el in track.findall("./"): # pour chaque element du track
        cats=[]
        #une boucle pour récupérer les émotions au instants start -> end
        for at in el.findall("./"):
            cats.append(at.get("name"))
        
        start = int(float(el.get("start")))
        end = int(float(el.get("end")))
        #associer les émotions à chaque seconde de l'intervale [start , end]
        for t in range(start,end+1):
            dict[t]=cats
    return dict

#une fonction qui prend en paramètre un fichier XML et retourne les données d'évaluation dans un dicionnaire
def parse(file):
    tree = ET.parse(file)
    root = tree.getroot()
    dict = {}
    # récupération des données des deux interlocuteurs
    dict['F']=get(root,"Female")
    dict['M']=get(root,"Male")
    return dict

#une fonction qui applique le onehotencoding sur les émotions
def onehot(cat):
    categories = {"Anger":[1,0,0,0,0,0,0,0,0,0],
                  "Happiness":[0,1,0,0,0,0,0,0,0,0], 
                  "Sadness":[0,0,1,0,0,0,0,0,0,0],
                  "Neutral state":[0,0,0,1,0,0,0,0,0,0], 
                  "Frustration":[0,0,0,0,1,0,0,0,0,0], 
                  "Excited":[0,0,0,0,0,1,0,0,0,0], 
                  "Fear":[0,0,0,0,0,0,1,0,0,0], 
                  "Surprise":[0,0,0,0,0,0,0,1,0,0],
                  "Disgust":[0,0,0,0,0,0,0,0,1,0], 
                  "Other":[0,0,0,0,0,0,0,0,0,1]}
    return categories[cat]



#une fonction qui génére un fichier json pour une session de vidéos
def generate_session_json(session,path):

    # récupération des fichiers XML associés aux vidéos de la session
    files = os.listdir(path)
    files = [f for f in files if (f.endswith("anvil") and not f.startswith("."))]
    files.sort()

    dicts=[]
    # il existe trois évaluations par vidéo, donc trois fichiers XML associés à une même video.
    # boucle pour récupérer les fichiers XML trois par trois
    for i in range(0,len(files),3):
        ds = [parse(path+f) for f in files[i:i+3]]
        dic=ds[0]
        #boucle pour fusionner les trois évaluations
        for i in range(1,len(ds)):
            for g,dv in ds[i].items():
                
                for k,l in dv.items():     
                    x = dic[g].get(k,[])
                    dic[g][k]=l+x

        dicts.append(dic)        


# boucle pour obtenir et encoder l'émotion la plus fréquente
    for d in dicts:
        for g,dv in d.items():
            for k,l in dv.items():
                if "Confidence" in l: l.remove("Confidence")
                counter = Counter(l)
                most_frequent = counter.most_common(1)[0][0]
                d[g][k] = onehot(most_frequent)

    print(len(dicts))
    # enregistrement des données dans un fichier JSON
    f = open(path+"Session"+str(session)+".json","w")
    json.dump(dicts,f)


# début du programme principale

if(len(sys.argv) < 2):
    raise Exception("vous devez saisir le chemin du dataset")

dir = sys.argv[1]

# génération des fichiers json pour toutes les sessions
for session in range(1,6):
    sessionpath = dir+"/Session"+str(session)+"/dialog/EmoEvaluation/Categorical/"
    generate_session_json(session , sessionpath)
