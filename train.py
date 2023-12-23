

import sys
#import nat
from IemocapDataset import IemocapDataset
from torch.utils.data import Dataset,DataLoader,random_split
import torch
import torch.nn as nn
import torch.optim as optim
if(len(sys.argv) < 2):
    raise Exception("vous devez saisir le chemin du dataset")
dataset_dir = sys.argv[1]

print("\n-------Chargement des données-------\n")
# chargement du dataset
full_dataset = IemocapDataset(dataset_dir,range(1,6))
#normalisation
full_dataset.images = full_dataset.images / 255
total_length = full_dataset.__len__()
train_length = int(0.8 * total_length)
val_length = int(0.1 * total_length)
test_length = total_length - train_length - val_length
# séparation du dataset
train_dataset, val_dataset, test_dataset = random_split(full_dataset, [train_length, val_length, test_length])

train_dataloader = DataLoader(train_dataset, batch_size=128, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=128, shuffle=True)

# initialisation du modèle
model =nat.NAT(
        num_classes = 10,
        depths=[1, 1],
        num_heads=[1, 2],
        embed_dim=64,
        mlp_ratio=3,
        drop_path_rate=0.2,
        kernel_size=7,
        
    )
print("\n-------Phase d'entrainement-------\n")
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001)
model.train() # mode entrainement
for epoch in range(1,2):
    run_loss=0
   
    print(epoch)
    for inputs,labels in train_dataloader:
	
        optimizer.zero_grad()
       
        # propagation
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backpropagation
        loss.backward()

        # Mise à jour des parameters
        optimizer.step()
        run_loss+= loss.item()

    print(f"epoch : {epoch} => Loss : {run_loss/len(train_dataloader)}")

print("\n-------Phase de test-------\n\n")
model.eval()

correct_predictions=0
for inputs, labels in test_dataloader:        
    outputs = model(inputs)
    for i in range(len(outputs)):
            if(outputs[i].argmax()==labels[i].argmax()):
                correct_predictions+=1


accuracy = correct_predictions/test_length
print(f'Test Accuracy: {accuracy * 100:.2f}%')