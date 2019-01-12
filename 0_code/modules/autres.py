#!/usr/bin/env python3
# -*- coding : utf8 -*-

import os
##############################################################
# Fonction : generation_arborescence()
##############################################################

def generation_arborescence():
    folders = ['2_resultats_intermediaires', '3_resultats_finaux']

    for folder in folders:

        if os.path.exists(f"../{folder}/"):
            print(f'- Dossier {folder}/ déjà existant')
        else:
            print(f"- Création du dossier : {folder}")
            try:
                os.makedirs(f'../{folder}/')
            except Exception as e:
                print('\tPROBLEME LORS DE LA CREATION DU DOSSIER.')
            else:
                print('\tCréation du dossier réussi.\n')


if __name__ == '__main__':
    print("Je ne sers pas à grand chose seul :-). Go to main.py")
