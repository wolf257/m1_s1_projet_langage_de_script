#!/usr/bin/env python3
# -*- coding : utf8 -*-

import pprint
import requests
import csv
import json

from modules import champs

# VarFichier
ficSourcePop = '../1_source/estim-pop-dep-sexe/'
ficIntermedPop = '../2_resultats_intermediaires/2_pop_parDept.csv'

ficSourceInsertion = '../1_source/fr-esr-insertion_professionnelle-master.csv'
ficIntermedInsertion = '../2_resultats_intermediaires/1_insertion_parEtabl.csv'

ficIntermedUniv = '../2_resultats_intermediaires/0_effectifs-etudiants.csv'

# VarChamps
champsOusseynou = champs.champsOusseynou
champsAndrea = champs.champsAndrea
champsLucia = champs.champsLucia


def generation_tableau_intermediaire_sur_demographie():
    liste_annees = ['2010', '2011', '2012', '2013', '2014', '2015']

    dico = {}
    for annee in liste_annees:
        fic = f"{ficSourcePop}{annee}.csv"

        # TEST :
        # print(f"****** Traitement année : {annee} *******")

        # On l'ouvre
        with open(fic, mode='r', encoding='utf8') as filein:

            # On skippe les 4 premieres lignes (0 à 3)
            for x in range(4):
                next(filein)

            for ligne in filein:

                ligne = ligne.strip()
                field = ligne.split(',')

                id_dept = field[0]

                if not id_dept.isdigit():
                    continue

                n_dept = field[1]

                estimation_brute = field[3]
                estimation_chiffre = ''
                for char in estimation_brute:
                    if char.isdigit():
                        estimation_chiffre += char

                # TEST
                # print(f"id : {id_dept}, nom : {n_dept}, pop : {estimation}")

                dico.setdefault(n_dept, {})

                dico[n_dept].setdefault('id_dept', 0)
                dico[n_dept]['id_dept'] = id_dept

                dico[n_dept].setdefault(annee, 0)
                dico[n_dept][annee] = int(estimation_chiffre)

    with open(ficIntermedPop, mode='w', encoding='utf8') as fileout:

        finit = f"nomDept , id_dept , 2010 , 2011 , 2012 , 2013 , 2014 , 2015"
        fileout.write(finit + '\n')

        for nomDept in dico.keys():
            id_dept = dico[nomDept].get('id_dept', 'na')
            c2010 = dico[nomDept].get('2010', 'na')
            c2011 = dico[nomDept].get('2011', 'na',)
            c2012 = dico[nomDept].get('2012', 'na',)
            c2013 = dico[nomDept].get('2013', 'na',)
            c2014 = dico[nomDept].get('2014', 'na',)
            c2015 = dico[nomDept].get('2015', 'na',)

            fDept = f"{nomDept} , {id_dept} , {c2010} , {c2011} , {c2012} , {c2013} , {c2014} , {c2015}"
            fileout.write(fDept + '\n')

        print(f"-  Le fichier '{ficIntermedPop.split('/')[-1]}' a été créé et rempli. ")


def filtered_csv_generator(file_name, new_file, sep, headers):
    '''
    Takes a csv file as an input and returns a new csv file
    with filtered headers and columns as an output.
    '''

    with open(file_name, 'r') as file_in:
        csv_reader = csv.DictReader(file_in, delimiter=sep)

        with open(new_file, 'w') as file_out:
            csv_writer = csv.DictWriter(file_out, fieldnames=headers,
                                        extrasaction='ignore', delimiter=sep)

            csv_writer.writeheader()

            for line in csv_reader:
                csv_writer.writerow(line)


def generation_tableau_intermediaire_sur_insertionPro():

    # headers = ['annee', 'numero_de_l_etablissement', 'domaine', 'discipline',
    #            'taux_dinsertion', 'emplois_stables', 'salaire_brut_annuel_estime',
    #            'taux_de_chomage_regional', 'salaire_net_mensuel_median_regional']

    filtered_csv_generator(ficSourceInsertion, ficIntermedInsertion, ';', champsAndrea)

    print(f"-  Le fichier '{ficIntermedInsertion.split('/')[-1]}' a été créé et rempli. ")


def get_datas_from_api(champsOusseynou):
    """docstring for get_datas_from_api"""

    site = 'https://data.enseignementsup-recherche.gouv.fr/'
    api = 'api/records/1.0/search/'
    arguments = {'dataset': 'fr-esr-statistiques-sur-les-effectifs-d-etudiants-inscrits-par-etablissement',
                 'rows': 500,
                 'facet': [elt[0] for elt in champsOusseynou]}

    # test
    # print(f"Facets = {arguments['facet']}")

    link = f"{site}{api}"

    # test
    # print(f"La requête sera faite à partir de : {link}")

    myrequest = requests.get(link, params=arguments)

    # test
    # print(f'Le lien est : {myrequest.url}')

    return myrequest, champsOusseynou


def transform_json_to_csv(myrequest, listChamps, ficSortie):
    """docstring for transform_json_to_csv"""

    myjson = json.loads(myrequest.text)

    f = csv.writer(open(ficSortie, "w+"))

    listNoms = [elt[1] for elt in listChamps]
    listClef = [elt[0] for elt in listChamps]

    f.writerow(listNoms)

    for elt in myjson['records']:
        if (2010 <= int(elt['fields'].get('rentree', 0)) <= 2015):
            datas = [elt['fields'].get(arg, 'na') for arg in listClef]
            f.writerow(datas)

    print(f"-  Le fichier '{ficSortie.split('/')[-1]}' a été créé et rempli. ")


def generation_tableau_intermediaire_sur_Univ():
    """docstring for main"""

    myrequest, listChamps = get_datas_from_api(champsOusseynou)

    if myrequest.status_code == 200:
        print(f'\nLa requête API a réussi.')
        transform_json_to_csv(myrequest, listChamps, ficIntermedUniv)
    else:
        print(f'Bad requests, we have code : {myrequest.status_code}.')


if __name__ == '__main__':
    print("Je ne sers pas à grand chose seul :-). Go to main.py")
