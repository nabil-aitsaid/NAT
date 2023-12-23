import os
import cv2
import json
import numpy as np
from torch.utils.data import Dataset
import torch
class IemocapDataset(Dataset):
    
    def __init__(self, root_dir,sessions):
            self.root_dir = root_dir
            self.sessions=sessions
            self.images,self.labels = self.load_data()
            
           

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        return image, label
    
    def __len__(self):
        return len(self.images)
    
    def load_data(self):
        images_list=[]
        labels_list=[]
        for s in self.sessions: # pour chaque session
            images_path = f"{self.root_dir}/Session{s}/dialog/images"
            json_path = f"{self.root_dir}/Session{s}/dialog/EmoEvaluation/Categorical/Session{s}.json"
            #chargement du fichier json qui les évaluations de la session s 
            json_file=open(json_path,"r")
            labels=json.load(json_file)
            dirs = os.listdir(images_path)
            dirs = [d for d in dirs if (d.endswith("avi") and not d.startswith("."))]
            dirs.sort()
            for i,dir in enumerate(dirs): # for chaque video
                video_images_path = images_path+"/"+dir
                images_files = os.listdir(video_images_path)
                # pour chaque image
                for imgname in images_files:
                    gender=imgname[0] # récupérer le genre (1er caractère du nom de l'image)
                    num = imgname[1:-4] # récupérer le numéro de l'image (qui correspond à l'instant dans la vidéo)
                    
                    lab=labels[i][gender].get(num,0) # essayer d'obtenir l'évaluation à l'instant num
                    if(lab): # si l'évaluation existe
                        img=cv2.imread(video_images_path+"/"+imgname) # récupérer l'image
                        img = np.array([img[:,:,0],img[:,:,1],img[:,:,2]],dtype=np.float32) # mise en forme pour pytorch
                        # création de l'input et du label 
                        images_list.append(img)
                        labels_list.append(np.array(lab,dtype=np.float32))
                   


        return torch.tensor(images_list) , torch.tensor(labels_list)         

