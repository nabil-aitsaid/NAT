import cv2
import sys
import os
import shutil

# une fonction qui génére les images d'une vidéo
def convert(outdir,filepath,gender):
    vidcap = cv2.VideoCapture(filepath)
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
            imgg,imgd = image[120:360,5:355] , image[120:360,365:715]
            genders=["M","F"]
            # générer l'image de l'interlocuteur de gauche qui porte les capteurs (gender)
            cv2.imwrite(outdir+"/"+gender+str(count)+".jpg", imgg)     # save frame as JPG file
            genders.remove(gender)
            # générer l'image de l'autre interlocuteur (droite)
            cv2.imwrite(outdir+"/"+genders[0]+str(count)+".jpg", imgd)
        return hasFrames
    
    sec = 0
    frameRate = 1 #capturer les images à chaque seconde
    count=1
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)



if(len(sys.argv) < 2):
    raise Exception("vous devez saisir le chemin du dataset")
dir = sys.argv[1]
#pour chaque session
for i in range(1,6):
    sessionpath = dir+"/Session"+str(i)
    divxpath = sessionpath+"/dialog/avi/DivX"
    files = os.listdir(divxpath) # lister les vidéos de la session i
    files = [f for f in files if (f.endswith("avi") and not f.startswith("."))]
    
    
    imagespath = sessionpath+"/dialog/images"
    # si un dossier images, on le supprimer
    if(os.path.exists(imagespath)):
        shutil.rmtree(imagespath)
    #creation du dossier images    
    os.mkdir(imagespath)
    for file in files :
        viddir = imagespath+"/"+file
        os.mkdir(viddir)
         #enregistrement des images dans Session<i>/dialog/images
        convert(viddir,divxpath+"/"+file,file[5])

