from copy import*
from random import*
import pandas as pd
import numpy as np


def support_seul(liste, valeur):

    '''
    :param liste: liste avec toutes les séquences
    :param valeur: valeur dont on veut connaître le support
    :return: Support(valeur) i.e : (nbre séquences où la valeur apparaît)/(nbre total de séauences)
    '''

    if len(liste) == 0:
        return "La liste entrée est vide"
    else:
        return (number_of_sequences_present(liste, valeur)) / len(liste)


def number_of_sequences_present(liste, valeur):

    '''
    :param liste: liste avec toutes les séquences
    :param valeur: valeur dont on veut connaître le nbre de sous-séquence où elle est présente
    :return: nbre de sous-liste où la valeur est présente
    '''

    sum = 0
    for i in range(len(liste)):
        if valeur in liste[i]:
            sum = sum + 1
    return sum


def are_present(liste, candidates):

    '''
    :param candidates: liste de candidats
    :param liste: liste avec toutes les séquences
    :return: True si les valeurs de candidats sont dans la liste et dans le même ordre
             False sinon
    '''

    presence = 0
    for i in range(len(candidates)):
        if candidates[i] in liste:
            liste = liste[liste.index(candidates[i]) + 1:]
            presence = presence + 1
    if presence == len(candidates):
        return True
    else:
        return False


def generate_candidates(liste, min_sup, k):

    '''
    :param liste: liste avec toutes les séquences
    :param min_sup: définis le support minimal en dessous duquel une séquence n'est pas fréquente
    :param k: longueur des candidats que l'on veut générer
    :return: liste des candidats de longueur k
    '''

    items = []
    for i in range(len(liste)):
        for elt in liste[i]:
            if elt not in items:
                items.append(elt)
    items.sort()
    if k == 1:
        return items
    elif k == 2: # . ------------------------------------------|
        tamp = [] # .                                          |
        for i in generate_frequent(liste, min_sup, k-1): # .   |
            for j in generate_frequent(liste, min_sup, k-1): # |> POUR LA RECURSIVITE
                tamp.append([i, j]) # .                        |
        return tamp # . ---------------------------------------|
    else:
        tamp = [] # . ---------------------------------------------|
        for i in generate_frequent(liste, min_sup, k-1):  # .      |
            for j in generate_frequent(liste, min_sup, k-1):  # .  |
                if i[1:] == j[:len(j) - 1]:  # .                   |
                    list_tampon = deepcopy(i)  # .                 |> TOUT CA SERT POUR LES CANDIDATS k-SEQUENTS
                    list_tampon.append(j[len(j) - 1])  # .         |
                    tamp.append(list_tampon)  # .                  |
        return tamp # . -------------------------------------------|


def generate_frequent(liste, min_sup, k):

    '''
    :param liste: liste avec toutes les séquences
    :param min_sup: définis le support minimal en dessous duquel une séquence n'est pas fréquente
    :param k: longueur des séquences fréquentes que l'on veut obtenir
    :return: liste des séquences fréquentes de longueur k
    '''

    if k == 1:
        tamp = []
        for elt in generate_candidates(liste, min_sup, 1):
            if support_seul(liste, elt) >= min_sup:
                tamp.append(elt)
        return tamp

    else:
        candidat = generate_candidates(liste, min_sup, k)  # Egale a la liste des candidats qu'on enlevera s'ils marchent pas
        tamp_candidat = []  # Liste vide, on ajoutera les candidats qui marchent
        list_a_regarder = []  # Sous liste a regarder
        for i in range(len(liste)):
            if len(liste[i]) >= k:
                list_a_regarder.append(liste[i])  # tamp_list = uniquement les sous listes de longueur >= k
        for elt in candidat:
            count = 0
            for i in range(len(list_a_regarder)):
                if are_present(list_a_regarder[i], elt ) is True: # Si les elt de candidats sont dans la liste à regarder (et dans le bon ordre)
                    count = count + 1  # On ajoute dans la liste des candidats qui marchent si count > min_sup
            if count / len(liste) >= min_sup:  # On regarde si ca passe le support
                tamp_candidat.append(elt)  # Si ca passe le sup_min, on ajoute dans la liste a renvoyer
        return tamp_candidat


def support(liste, elt_frequent):

    '''
    :param liste: liste avec toutes les séquences
    :param elt_frequent: elt (peut etre une liste d'elt) dont on veut le support
    :return: retourne le support i.e le nbre de sous-listes ou apparait l'elt divisé par le nombre total de sous-listes
    '''

    list_a_regarder = []
    count = 0
    for i in range(len(liste)):
        if len(liste[i]) >= len(elt_frequent):
            list_a_regarder.append(liste[i])

    for i in range(len(list_a_regarder)):

        if are_present(list_a_regarder[i], elt_frequent) is True:
            count = count + 1

    return count/len(liste)



def combiner_lignes(liste, nbre_listes_a_combiner = 1):

    '''
    :param liste: liste avec toutes les séquences
    :param nbre_ligne_a_combiner: définis le nombre de lignes à combiner
    :return: new_l : liste qui combine les sous-listes.

            Ex : nbre_ligne_a_combiner = 2 pour liste l = [[1, 2], [4], [5, 6], [7]]
                 new_l = [[1, 2, 4], [4, 5, 6], [5, 6, 7]]

            Ex : nbre_ligne_a_combiner = 3 pour liste l = [[1, 2], [4], [5, 6], [7]]
                 new_l = [[1, 2, 4, 5, 6], [4, 5, 6, 7]]
    '''

    new = [[]] * (len(liste) - (nbre_listes_a_combiner - 1))
    for i in range(len(liste) - (nbre_listes_a_combiner - 1)):
        count = 0

        while count != nbre_listes_a_combiner:
            new[i] = new[i] + liste[i + count]
            count = count + 1

    return new


def regrouper_achats(liste_totale, liste_id_product):

    '''
    :param liste_totale des séquences (potentiellement combiné, cette liste pourra être (combiner_listes(liste, nbre_lsites_a_combiner)): ATTEENTION DOIT ETRE LISTE DE LISTES
    :param liste_id_product: liste de tous id_product
    :return: retourne la liste totale avec 'achat' à la place des id_products.

            Cette fonction permet de ne pas se soucier de quel produit a été acheté par le client.
            Une séquence sera repérée avec un achat, pas forcément un produit spécifique.
    '''

    for i in liste_totale:
        for j in range(len(i)):
            if i[j] in liste_id_product:
                i[j] = 'purchase'
    return liste_totale


def generate_one_random_user(semaine, id_product, proba_connexion):

    '''
    :param semaine_min: Nombre de semaine sur laquelle on va travailler
    :param liste_id_products: Liste contenant les id_products
    :param proba_connexion: Probabilité que l'utilisateur se connecte (au moins 1 fois)sur une semaine
    :return: Comportement d'un utilisateur
    '''

    semaine_random = [[]] * semaine
    for l in range(len(semaine_random)):
        connexion = random()
        if connexion <= proba_connexion:
            n = randint(1, 3)
            if n == 1:
                semaine_random[l] = semaine_random[l] + ['desktop']
            elif n == 2:
                semaine_random[l] = semaine_random[l] + ['mobile_web']
            elif n == 3:
                semaine_random[l] = semaine_random[l] + ['android']

    for i in range(len(semaine_random)):

        if len(semaine_random[i]) != 0:
            count = 0
            n = randint(0, 6)
            while count != n:
                rand = randint(1, 11)
                if rand == 1 or rand == 2 or rand == 3:
                    semaine_random[i] = semaine_random[i] + ['desktop']
                elif rand == 4 or rand == 5 or rand == 6:
                    semaine_random[i] = semaine_random[i] + ['mobile_web']
                elif rand == 7 or rand == 8 or rand == 9:
                    semaine_random[i] = semaine_random[i] + ['android']
                else:
                    semaine_random[i] = semaine_random[i] + ['purchase']
                count = count + 1
            index = [idx for idx, e in enumerate(semaine_random[i]) if e == 'purchase']
            for j in index:
                semaine_random[i][j] = id_product[randint(0, len(id_product) - 1)]
    return semaine_random


def generate_k_random_users(semaine, id_product, number_of_users, proba_connexion):
    users = []
    for i in range(number_of_users):
        users.append(generate_one_random_user(semaine, id_product, proba_connexion))
    return users


def nombre_apparition(liste, sequence):

    '''
    :param liste: liste totale des sequences
    :param sequence: sequence dont on veut connaitre le nombre d'apparition dans la sous-liste
    :return: renvoie le nombre d'apparition dans la sous liste
    '''
    liste_tamp  = deepcopy(liste)
    count = 0
    for i in range(len(liste_tamp)):
        while are_present(liste_tamp[i], sequence) is True:
            count = count + 1
            for j in range(len(sequence)):
                liste_tamp[i] = liste_tamp[i][liste_tamp[i].index(sequence[j]) + 1:]
    return count


def achat_manque(liste, sequence_avec_achat):

    '''
    :param liste: liste totale des sequences
    :param sequence_avec_achat: sequence (qui finit par un achat) dont on veut connaitre le nombre de fois ou elle a été réalisé sans mener à un achat
    :return: renvoie le nombre de fois où la séquence a été réalisé sans mener à un achat
    '''
    sequence_sans_achat = deepcopy(sequence_avec_achat)
    del sequence_sans_achat[-1]
    print("avec achat =", sequence_avec_achat)
    print("sans achat =", sequence_sans_achat)
    return nombre_apparition(liste, sequence_sans_achat) - nombre_apparition(liste, sequence_avec_achat)

