#!/usr/bin/env python
import os, sys


try:
	FileName=str(sys.argv[1])
	DestName=str(sys.argv[2])
	if not os.path.isdir(FileName):
		print("dossier source non existant")
		exit(-1)
	if not os.path.isdir(DestName):
		print("dossier de destination non existant")
		question=raw_input('voulez-vous la cree o/n:   ')
		if question == 'o':
			try:
				os.mkdir(DestName)
			except:
				print('le dossier ne peut pas etre cree')
		else:
			exit(-1)
except:
	print("vous n'avez pas renseigner un nom de  dossier source ou de destination existant")
	exit(-1)
#############################################################################################
                                                                 #permet de copier un fichier
#############################################################################################
#parametres de la fonction:
    #SrcFile: lien vers le fichier a copier
    #DestName: lien vers le dossier de la copie
    #filename: nom de la copie
def copyfile(SrcFile,DestName,filename):
	############################################################
	#ouverture du fichier "SrcFile" en mode lecture
	#lecture du fichier
	#ouverture d'un fichier ""(non existant) d'un fichier en ecriture
	#  qui va permettre la creation de ce fichier non exisatnt
	#on ecrit le contenu du fichier  
	############################################################
	File=open(SrcFile,'r')
	ReadFile=File.read()
	#print "copie du fichier '"+filename +"' dans le dossier "+DestName+"/"
	CopyFile=DestName+'/'+filename
	CopyFile=open(CopyFile,'w')
	CopyFile.write(ReadFile)	
	CopyFile.close()	
	File.close()
#############################################################################################
                                       #permet de parcourir et copier le contenu d'un dossier
#############################################################################################
Inode={}#un dico contenant comme cle l'inode de l'element et comme valeur son chemin(src)
#parametres:
#   From: le chemin du dossier source a copier
#   To: le chemin du dossier de destination
def copy(From,To):
	Listfile = os.listdir(From)
	# print "--------------------------------------------------------"
	#print "le dossier "+From+"/contient:"+str(Listfile)
	################## gestion des inodes #####################
	# on parcours tout le contenu du dossier From
	# si elle contient un dossier
	# on cree un dossier du meme nom dans la destination
	# puis on relance la copie sur ce nouveau dossier
	# Et pour les fichiers on test si on a pas encore croise un
	# autre fichiers du meme inode et on la copie, sinon on 
	# cree une copie qui va partager le meme inode que le fichier
	# deja racontrer
	########### parcours du contenu du dossier #################
	for FileName in Listfile:
		srcfile = From+'/'+FileName 
		srccopy=str(To+'/'+FileName)
		InodeFile=os.stat(srcfile).st_ino
		# si c'est un dossier
		if os.path.isdir(srcfile):
			#print "creation du dossier "+srccopy
			try:
				os.mkdir(srccopy)
				#print "success"
			except:
				#print 'not success '+srccopy+'y existe deja'
				pass
			copy(srcfile,srccopy)
		# si c'est un fichier
		else:
			
			if InodeFile not in Inode:
				copyfile(srcfile,To,FileName)
				Inode[InodeFile]=srccopy
			else:
				try:
					#print 'creation du ficher '+srccopy+' en lien symbolique avec le fichier '+Inode[InodeFile]
					os.link(Inode[InodeFile],srccopy)
				except:
					#print 'not success'+srccopy+'y existe deja'
					pass

				
copy(FileName,DestName)
