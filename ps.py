import os, sys, pwd
from optparse import OptionParser
import time
#on recupere la largeur du terminal
columns =int(os.popen('stty size', 'r').read().split()[1])
#temps de l'utilisateur
USERCLCK=os.sysconf(os.sysconf_names["SC_CLK_TCK"])
#############################################################################################
                                    #convertir le temps seconde en format heure, min, seconde
#############################################################################################
def decoupe(seconde):
    heure = str(seconde/3600)
    if len(heure)==1:
    	heure='0'+heure
    seconde %= 3600
    minute = str(seconde/60)
    if len(minute)==1:
    	minute='0'+minute
    seconde%=60 
    seconde=str(seconde)
    if len(seconde)==1:
    	seconde='0'+seconde
    return [heure,minute,seconde]

#############################################################################################
                                                   #on recupere les PID de tous les processus
#############################################################################################
def ALLPID():
	listPID=[]
	#########################################
	#on recupere le PID de tous les processus
	#########################################
	for i in os.listdir('/proc/'):
		try:
			int(i)
			listPID+=[i]
		except:
			pass
	return listPID

#############################################################################################
                        #on recupere les PID  a afficher quand on lance "ps" sans argument(s)
#############################################################################################
def PID():
	listPID=[]
	#########################################
	#le PID de la commande et de son parent
	#########################################
	PPID=os.getppid() #ou avec proc/self/stat
	PID=os.getpid()
	listPID+=[PPID,PID]
	return listPID

#############################################################################################
                                                          #on recupere les PID pour l'otion a
#############################################################################################
def APID():
	listPID=[]
	##########################################
	# PID des Processus de l'utilisateur et
	# aussi des autres utilisateurs. c'est a 
	# dire le PID des process dont le TTY est 
	# different de "?"
	##########################################
	for PID in ALLPID():
		PID=str(PID)
		File=open('/proc/'+PID+'/stat','r')
		parseFile=File.readlines()[0].split()
		File.close()
		tty_nr=int(parseFile[6])
		TTY=TTYPROCESS(tty_nr)
		if TTY[:3]!='?':
			listPID+=[PID]
	return listPID		

#############################################################################################
                                                          #on recupere les PID pour l'otion x
#############################################################################################
def XPID():
	listPID=[]
	##########################################
	# PID des processus utilisateur non lance
	# dans un terminal. c'est a dire le PID
	# des process dont le TTY ne contient pas
	# "tty" et l'USER = nom de l'utilisateur
	##########################################
	for PID in ALLPID():
		PID=str(PID)
		File=open('/proc/'+PID+'/stat','r')
		parseFile=File.readlines()[0].split()
		File.close()
		tty_nr=int(parseFile[6])
		TTY=TTYPROCESS(tty_nr)
		PID=str(PID)
		File=open('/proc/'+PID+'/status','r')
		parseFile=File.readlines()
		File.close()
		UID=parseFile[6].split()[1]
		if parseFile[6].split()[0]!='Uid:':
			UID=parseFile[7].split()[1]

		USER=pwd.getpwuid(int(UID))[ 0 ]
		if TTY[:3]!='tty'  and USER == pwd.getpwuid(os.getuid())[ 0 ]:
			listPID+=[PID]
	return listPID		

#############################################################################################
                                                          #on recupere les PID pour l'otion u
#############################################################################################
def UPID():
	listPID=[]
	##########################################
	# PID du Processus de la commande lance et 
	# parent(bash) de l'utilisateur et aussi 
	# ceux des autres utilisateurs. c'est a 
	# dire le PID des process dont le TTY  
	# commence par "pts"
	##########################################
	for PID in ALLPID():
		PID=str(PID)
		File=open('/proc/'+PID+'/stat','r')
		parseFile=File.readlines()[0].split()
		File.close()
		tty_nr=int(parseFile[6])
		TTY=TTYPROCESS(tty_nr)

		if TTY[:3]=='pts':
			listPID+=[PID]
	return listPID	

#############################################################################################
                                                             #Recuperer le TTY d'un processus
#############################################################################################
def TTYPROCESS(tty_nr):
	##########################################
	# creation d'un dico contenant pour chaque 
	# device son TTY.  Ayant comme cle
	# le numero du device et comme valeur son
	# TTY. et si le TTY du device ne commence
	# pas par pts ou tty alors il sera egal a 
	# '?'.
	##########################################
	tty={} 
	try:
		for i in os.listdir('/dev/pts'):
			devSRC='/dev/pts/'+i
			tty[os.stat(devSRC).st_rdev]=i
		TTY='pts/'+tty[tty_nr]
	except:
		for i in os.listdir('/dev/'):
			devSRC='/dev/'+i
			tty[os.stat(devSRC).st_rdev]=i
		try:
			TTY='pts/'+tty[tty_nr]
			if TTY[0:3]!='pts':
				TTY='?'
			else:
				TTY=TTY[4:]
		except:
			TTY='?'
	if TTY[0:3]!='pts' and TTY[0:3]!='tty':
		TTY ='?'
	return TTY

#############################################################################################
                                                                #CALCUL DU CPU D'UN PROCESSUS
#############################################################################################
def CPUTIME(PID):
	##########################################
	# on recupere l'UTIME dans /proc/pid/stat
	# ainsi que le STIME
	# on fait le rapport(UTIME+STIME)/USERCLCK
	# on decoupe en heure sec min
	# on met sous format hh:mm:ss
	##########################################
	File=open('/proc/'+PID+'/stat','r')
	parseFile=File.readlines()[0].split()
	File.close()
	UTIME=int(parseFile[13])
	STIME=int(parseFile[14])
	
	TIME=int((UTIME+STIME)/USERCLCK)
	TIME=decoupe(TIME)
	return TIME[0]+':'+TIME[1]+':'+TIME[2]

#############################################################################################
                                                               #CALCUL DU %MEM D'UN PROCESSUS
#############################################################################################
def MEMOIRE(RSS):
	##########################################
	# on recupere MEMTOTAL dans /proc/meminfo
	# on fait le rapport RSS*100/MEMTOTAL
	# on regle la valeur afficher format X.X
	##########################################
	File=open('/proc/meminfo','r')
	parseFile=File.readlines()[0].split()
	MEMTOTAL=parseFile[1]
	MEM=RSS*100/int(MEMTOTAL)
	MEM=str(MEM)
	if len(MEM)==1:
		MEM='0.'+MEM
	elif len(MEM)==2:
		MEM=MEM[0]+'.'+MEM[1]
	else:
		MEM='0.0'
	return MEM

#############################################################################################
                                               #REGLAGE DE l'AFFICHAGE PAR RAPPORT AU VALEURS 
#############################################################################################
def ESPACE(val):
	val=len(val)
	if val==8:
		espace=' '
	elif val==7:
		espace='  '
	elif val==6:
		espace='   '	
	elif val==5:
		espace='    '	
	elif val==4: 
		espace='     '
	elif val==3:
		espace='      '
	elif val==2:
		espace='       '
	elif val==1:
		espace='        '
	else:
		espace='   '
	return espace

def PS(PID):
	######## Valeur du PID, STAT, TIME, CMD ########
	PID=str(PID)
	File=open('/proc/'+PID+'/stat','r')
	parseFile=File.readlines()[0].split()
	File.close()
	STAT=parseFile[2]
	TIME=CPUTIME(PID)
	CMD=parseFile[1]
	######## Valeur du TTY grace au tty_nr ##########
	tty_nr=int(parseFile[6])
	TTY=TTYPROCESS(tty_nr)
	############## affichage du resultat ###############
	print PID+ESPACE(PID)+TTY+ESPACE(TTY)+STAT+'    '+TIME+'  '+CMD

#############################################################################################
                  #AFFICHAGE DU PROCESSUS DU PID RENSEIGNE SOUS FORMAT UTILISATEUR: ps -u PID
#############################################################################################
def PSU(PID):
	PID=str(PID)

	File=open('/proc/'+PID+'/status','r')
	parseFile=File.readlines()
	UID=parseFile[6].split()[1]
	USER=pwd.getpwuid(int(UID))[0]
	VSZ=parseFile[11].split()[1]
	RSS=parseFile[15].split()[1]
	
	try :
		int(VSZ)
	except:
		VSZ='0'
	try :
		int(RSS)
		if RSS[:2]=='00':
			RSS='0'
	except:
		RSS='0'

	MEM=MEMOIRE(int(RSS))
	TIME=CPUTIME(PID)
	File.close()
	File2=open('/proc/'+PID+'/stat','r')
	parseFile2=File2.readlines()[0].split()
	CMD=parseFile2[1]
	tty_nr=int(parseFile2[6])
	TTY=str(TTYPROCESS(tty_nr))
	STAT=parseFile2[2]
	START=time.ctime(os.path.getctime('/proc/'+PID)).split()[3]	
	CPU = '0.0'

	if len(USER)>8:
		USER=USER[:7]



	RESULTS =USER+ESPACE(USER)+PID+ESPACE(PID)+CPU+'  '+ MEM+'  '+VSZ+ESPACE(VSZ)+RSS+ESPACE(RSS)+TTY+ESPACE(TTY)+STAT+'     '+START+'  '+TIME+'  '+CMD
	print RESULTS[:int(columns)]
	

#############################################################################################
                                                           #creation des option avec optparse
#############################################################################################

parser = OptionParser()
parser.add_option('-e', dest="e", help="affiche tout les processus",
	action='store_true' )
parser.add_option('-u', dest="u", action='store_true', 
   help="affichage sous format utilisateur/[sans arg]affiche les process des autres users ",)
parser.add_option('-a', dest="a",  action='store_true',
	help="Affiche aussi les process (lance dans un terminal) des autres users",)
parser.add_option('-x', dest="x",  action='store_true',
	help="Afficher les processus de l'utilisateur qui ne sont pas dans un terminal", )

option,argument=parser.parse_args()
#############################################################################################
                                                       #gestion de l'execution de la commande
#############################################################################################
NONEFORMAT='PID      TTY      STAT     TIME  COMMAND'
USERFORMAT="USER     PID      %CPU %MEM VSZ      RSS      TTY      STAT  START     TIME      COMMAND"
###############################################################
									 #option -aux ou option -eu
###############################################################
if (option.e and option.u)or (option.a and option.u and option.x):
	print USERFORMAT[:columns] 
	for PID in ALLPID():         #on affiche tous les Processus
		PSU(PID)
###############################################################
										 #option ax ou option e
###############################################################
elif option.e or (option.a and option.x):
	print NONEFORMAT[:columns] 
	#on affiche tous les Processus
	for PID in ALLPID():
		PS(PID)
###############################################################
								                    #option -ua 
###############################################################
elif option.u and option.a:
	print USERFORMAT[:columns] 
	if len(sys.argv) > 2:          #le cas d'ajout d'autres PID
		i=0
		listPID=[]   #permet d'eviter les affichages  en double
		while i < len(sys.argv):
			try:
			 	int(sys.argv[i])
			 	PID=sys.argv[i]
			 	if PID not in listPID:
			 		PSU(PID)
			 	listPID+=[PID]
			except:
				pass
			i+=1
	#on affiche les resultats de l'otion
	for PID in APID():
		PSU(PID)
###############################################################
								                    #option -ux 
###############################################################
elif option.u and option.x:
	print USERFORMAT[:columns] 
	if len(sys.argv) > 2:          #le cas d'ajout d'autres PID
		i=0
		listPID=[]   #permet d'eviter les affichages  en double
		while i < len(sys.argv): 
			try:
			 	int(sys.argv[i])
			 	PID=sys.argv[i]
			 	if PID not in listPID:
			 		PSU(PID)
			 	listPID+=[PID]
			except:
				pass
			i+=1
	for PID in XPID():     #on affiche les resultats de l'otion
		PSU(PID)
###############################################################
								                     #option -a 
###############################################################
elif option.a:
	print NONEFORMAT[:columns] 
	
	if len(sys.argv) > 2:          #le cas d'ajout d'autres PID
		i=0
		
		listPID=[]   #permet d'eviter les affichages  en double
		while i < len(sys.argv):
			try:
			 	int(sys.argv[i])
			 	PID=sys.argv[i]
			 	if PID not in listPID:
			 		PS(PID)
			 	listPID+=[PID]
			except:
				pass
			i+=1
	for PID in APID():     #on affiche les resultats de l'otion
		PS(PID)
###############################################################
								                     #option -u 
###############################################################
elif option.u:
	i=0
	print USERFORMAT[:columns] 
	if len(sys.argv) > 2:          #le cas d'ajout d'autres PID
		i=0
		listPID=[]    #permet d'eviter les affichage  en double
		while i < len(sys.argv):
			try:
			 	int(sys.argv[i])
			 	PID=sys.argv[i]
			 	if PID not in listPID:
			 		PSU(PID)
			 	listPID+=[PID]
			except:
				pass
			i+=1
	else:          # sinon on affiche les resultats de l'otion
		for PID in UPID():
			PSU(PID)
###############################################################
								                     #option -x 
###############################################################		
elif option.x:
	print NONEFORMAT[:columns] 
	
	if len(sys.argv) > 2:         #le cas d'ajout d'autres PID
		i=0
		
		listPID=[]  #permet d'eviter les affichages  en double
		while i < len(sys.argv):
			try:
			 	int(sys.argv[i])
			 	PID=sys.argv[i]
			 	if PID not in listPID:
			 		PS(PID)
			 	listPID+=[PID]
			except:
				pass
			i+=1
	for PID in XPID():     #on affiche les resultats de l'otion
		PS(PID)
###############################################################
								                   #sans option 
###############################################################	
elif len(sys.argv) >= 2:
	i=0
	listPID=[]        #permet d'eviter les affichage  en double
	print NONEFORMAT[:columns] 
	while i < len(sys.argv):
		if i=='-a':
			PS(os.getpid())
		try:
		 	int(sys.argv[i])
		 	PID=sys.argv[i]
		 	if PID not in listPID:
		 		PS(PID)
		 	listPID+=[PID]
		except:
			if i==(len(sys.argv)):
				print "aucun pid renseigne existant"
		i+=1
else:              # sinon on affiche les resultats de l'otion
	print NONEFORMAT[:columns] 
	for PID in PID():
		PS(PID)


