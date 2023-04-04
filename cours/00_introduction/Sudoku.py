import tkinter as tk
import random
from tkinter import filedialog
from tkinter import messagebox
racine = tk.Tk()
racine.title("Sudoku")


def créer_barre_boutons():
    barre_boutons = tk.Frame(racine)

    bouton_nouveau = tk.Button(barre_boutons, text="Nouveau", command=grille)
    bouton_nouveau.pack(side="left", padx=(0, 0))

    bouton_quitter = tk.Button(barre_boutons, text="Quitter", command=racine.destroy)
    bouton_quitter.pack(side="left", padx=(0, 0))

    bouton_generer = tk.Button(barre_boutons, text="generer", command=remplir_aleatoire)
    bouton_generer.pack(side="left", padx=(0, 0))

    bouton_verifier = tk.Button(racine, text="Vérifier", command=lambda: verifier_grille(entrees))
    bouton_verifier.pack(side="bottom", pady=10)

    bouton_resoudre = tk.Button(barre_boutons, text="Résoudre", command=lambda: resoudre(entrees))
    bouton_resoudre.pack(side="left", padx=(0, 0))

    barre_boutons.pack(side="top", fill="x", pady=(0, 0))

# grille :
entrees = []
def grille():
    global entrees # permet d'accéder à la variable globale
    # supprime les anciennes entrées quand on utilise le bouton "nouveau"
    for ligne in entrees:
        for entree in ligne:
            entree.destroy()

    entrees = [] #réinitialise la grille
    cadre = tk.Frame(racine)
    for i in range(9):
        ligne = []
        for j in range(9):
            entree = tk.Entry(cadre, width=2, font=("Helvetica", 20), justify="center")
            if j % 3 == 0:
                entree.grid(row=i, column=j, padx=(5, 0), pady=(5, 0))
            else:
                entree.grid(row=i, column=j, pady=(5, 0))
            ligne.append(entree)
        entrees.append(ligne)
    cadre.pack(side="top", padx=10, pady=(0, 10))

def remplir_aleatoire():
    global entrees
    x = 1                   #créer un bouton qui permet de changer la valeur de X suivant la difficulté souhaitée
    for i in range(9):
        for j in range(9):
            if random.random() < x:
                valeur = random.randint(1, 9)
                grille_valide = False
                
                #Vérification validité de la valeur dans ligne et colonne
                for k in range(9):
                    if entrees[i][k].get() == str(valeur) or entrees[k][j].get() == str(valeur):
                        break
                else:
                    #Vérification validité de la valeur dans le bloc 3x3
                    bloc_i = (i // 3) * 3
                    bloc_j = (j // 3) * 3
                    for l in range(3):
                        for m in range(3):
                            if entrees[bloc_i+l][bloc_j+m].get() == str(valeur):
                                break
                        else:
                            continue
                        break
                    else:
                        #si valeur valide, on la place dans la case correspondante
                        entrees[i][j].insert(0, str(valeur))


def verifier_grille(grille):
    for i in range(9):
        for j in range(9):
            if grille[i][j].get() == "":
                messagebox.showerror("Erreur", f"La case {i+1}, {j+1} est vide.")
                return

    # vérification des blocs de 3x3
    for bloc_i in range(3):
        for bloc_j in range(3):
            valeurs = []
            for i in range(3):
                for j in range(3):
                    valeur = grille[bloc_i*3+i][bloc_j*3+j].get()
                    if valeur != "" and valeur in valeurs:
                        messagebox.showerror("Erreur", f"La case {bloc_i*3+i+1}, {bloc_j*3+j+1} contient une valeur en double.")
                        return
                    valeurs.append(valeur)

    #vérification des lignes
    for i in range(9):
        valeurs = []
        for j in range(9):
            valeur = grille[i][j].get()
            if valeur != "" and valeur in valeurs:
                messagebox.showerror("Erreur", f"La case {i+1}, {j+1} contient une valeur en double.")
                return
            valeurs.append(valeur)

    #vérification des colonnes
    for j in range(9):
        valeurs = []
        for i in range(9):
            valeur = grille[i][j].get()
            if valeur != "" and valeur in valeurs:
                messagebox.showerror("Erreur", f"La case {i+1}, {j+1} contient une valeur en double.")
                return
            valeurs.append(valeur)

    #si fonction n'a pas retourné d'erreur
    messagebox.showinfo("Félicitations !", "Vous avez résolu la grille !")




def resoudre(grille):
    for i in range(9):
        for j in range(9):
            if grille[i][j].get() == "":
                # Tester chaque valeur possible
                for k in range(1, 10):
                    valide = True
                    #valeur valide dans la ligne et la colonne
                    for l in range(9):
                        if grille[i][l].get() == str(k) or grille[l][j].get() == str(k):
                            valide = False
                            break
                    if not valide:
                        continue
                    #valeur valide dans le bloc 3x3
                    bloc_i = (i // 3) * 3
                    bloc_j = (j // 3) * 3
                    for l in range(3):
                        for m in range(3):
                            if grille[bloc_i+l][bloc_j+m].get() == str(k):
                                valide = False
                                break
                        if not valide:
                            break
                    if not valide:
                        continue
                    grille[i][j].insert(0, str(k))
                    if resoudre(grille):
                        return True                   
                    grille[i][j].delete(0, tk.END)
                return False
    return True

créer_barre_boutons()
grille()
racine.mainloop()
