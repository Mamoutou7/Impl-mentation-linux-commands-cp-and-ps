#!/usr/bin/env python
import os
import sys

try:
    file_name = str(sys.argv[1])
    dest_name = str(sys.argv[2])
    if not os.path.isdir(file_name):
        print("dossier source non existant")
        exit(-1)
    if not os.path.isdir(dest_name):
        print("dossier de destination non existant")
        question = raw_input('voulez-vous la cree o/n:   ')
        if question == 'o':
            try:
                os.mkdir(dest_name)
            except:
                print('le dossier ne peut pas etre cree')
        else:
            exit(-1)
except:
    print("vous n'avez pas renseigner un nom de  dossier source ou de destination existant")
    exit(-1)


def copyfile(src_file, dest_name, filename):
    """
    permet de copier un fichier

    :param src_file:  lien vers le fichier a copier
    :param dest_name: lien vers le dossier de la copie
    :param filename: nom de la copie
    :return:
    """

    # ouverture du fichier "SrcFile" en mode lecture
    with open(src_file, 'r') as file:
        # lecture du fichier
        read_file = file.read()
        # ouverture d'un fichier ""(non existant) d'un fichier en ecriture
        #  qui va permettre la creation de ce fichier non exisatnt
        file_to_copy = dest_name + '/' + filename
        # on ecrit le contenu du fichier
        file_to_copy = open(read_file)
        file_to_copy.close()
        file.close()




def copy(source, dest):
    """
    Permet de parcourir et copier le contenu d'un dossier
    :param source: le chemin du dossier source a copier
    :param dest: le chemin du dossier de destination
    :return:
    """
    # un dico contenant comme cle l'inode de l'element et comme valeur son chemin(src)
    inode = {}
    file_list = os.listdir(source)
    # print("--------------------------------------------------------")
    # print("le dossier "+From+"/contient:"+str(Listfile))
    ################## gestion des inodes #####################

    # si elle contient un dossier


    # Et pour les fichiers on test si on a pas encore croise un
    # autre fichiers du meme inode et on la copie, sinon on

    # deja racontrer
    # parcours du contenu du dossier

    # on parcours tout le contenu du dossier From
    for file_name in file_list:
        # on cree un dossier du meme nom dans la destination
        src_file_path = source + '/' + file_name
        # puis on relance la copie sur ce nouveau dossier
        dest_path_copy = str(dest + '/' + file_name)
        # cree une copie qui va partager le meme inode que le fichier
        inode_file = os.stat(src_file_path).st_ino
        # si c'est un dossier
        if os.path.isdir(src_file_path):
            try:
                os.mkdir(dest_path_copy)
            except:
                # print('not success '+srccopy+'y existe deja')
                pass
            copy(src_file_path, dest_path_copy)
        # si c'est un fichier
        else:
            if inode_file not in inode:
                copyfile(src_file_path, dest, file_name)
                inode[inode_file] = dest_path_copy
            else:
                try:
                    # print('creation du ficher '+srccopy+' en lien symbolique avec le fichier '+Inode[InodeFile])
                    os.link(inode[inode_file], dest_path_copy)
                except:
                    # print('not success'+srccopy+'y existe deja')
                    pass


if __name__ == '__main__':
    source = ""
    dest = ""
    copy(source, dest)
