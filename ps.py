import os, sys, pwd
from optparse import OptionParser
import time
#on recupere la largeur du terminal
columns =int(os.popen('stty size', 'r').read().split()[1])
#temps de l'utilisateur
USERCLCK=os.sysconf(os.sysconf_names["SC_CLK_TCK"])

def decoupe(seconde):
    """
    convertir le temps seconde en format heure, min, seconde

    :param seconde: Nombre total de seconde à convertir
    :return: [heure,minute,seconde]
    """
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

def all_pid():
    """
    on recupere les PID de tous les processus
    :return:
    """
    list_pid=[]
    # on recupère le PID de tous les processus
    for i in os.listdir('/proc/'):
        try:
            int(i)
            list_pid+=[i]
        except:
            pass
    return list_pid



def pid_wthout_option():
    """
    on recupere les PID  a afficher quand on lance "ps" sans argument(s)
    :return:
    """
    list_pid = []
    #le PID de la commande et de son parent
    ppid = os.getppid() #ou avec proc/self/stat
    pid = os.getpid()
    list_pid += [ppid,pid]
    return list_pid

def a_pid():
    """
    on recupere les PID pour l'option a
    :return:
    """
    list_pid = []

    # PID des Processus de l'utilisateur et
    # aussi des autres utilisateurs. c'est a
    # dire le PID des process dont le TTY est
    # different de "?"

    for pid in all_pid():
        file = open('/proc/'+str(pid)+'/stat','r')
        parse_file = file.readlines()[0].split()
        file.close()
        tty_nr=int(parse_file[6])
        tty = tty_process(tty_nr)
        if tty[:3] != '?':
            list_pid += [pid]
    return list_pid


def x_pid():
    """
    on recupere les PID pour l'otion x
    :return:
    """
    list_pid = []
    ##########################################
    # PID des processus utilisateur non lance
    # dans un terminal. c'est a dire le PID
    # des process dont le TTY ne contient pas
    # "tty" et l'USER = nom de l'utilisateur
    ##########################################
    for pid in all_pid():

        file = open('/proc/'+str(pid)+'/stat','r')
        parse_file = file.readlines()[0].split()
        file.close()
        tty_nr=int(parse_file[6])
        tty = tty_process(tty_nr)
        file = open('/proc/'+str(pid)+'/status','r')
        parse_file = file.readlines()
        file.close()
        uid = parse_file[6].split()[1]
        if parse_file[6].split()[0] != 'Uid:':
            uid = parse_file[7].split()[1]

        user = pwd.getpwuid(int(uid))[ 0 ]
        if tty[:3]!='tty'  and user == pwd.getpwuid(os.getuid())[ 0 ]:
            list_pid += [pid]
    return list_pid


def u_pid():
    list_pid=[]
    # PID du Processus de la commande lance et
    # parent(bash) de l'utilisateur et aussi
    # ceux des autres utilisateurs. c'est a
    # dire le PID des process dont le TTY
    # commence par "pts"

    for pid in all_pid():
        file=open('/proc/'+ str(pid) +'/stat','r')
        parse_file = file.readlines()[0].split()
        file.close()
        tty_nr=int(parse_file[6])
        tty=tty_process(tty_nr)

        if tty[:3] == 'pts':
            list_pid +=[pid]
    return list_pid


def tty_process(tty_nr):
    """
    Recuperer le TTY d'un processus
    :param tty_nr:
    :return:
    """
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


def MEMOIRE(RSS):
    """
    CALCUL DU %MEM D'UN PROCESSUS
    :param RSS:
    :return:
    """
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

def ESPACE(val):
    """
    REGLAGE DE l'AFFICHAGE PAR RAPPORT AU VALEURS
    :param val:
    :return:
    """
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

def cmd_ps(pid):
    # Valeur du PID, STAT, TIME, CMD
    file=open('/proc/' + str(pid) + '/stat','r')
    parse_file = file.readlines()[0].split()
    file.close()
    stat = parse_file[2]
    time = CPUTIME(str(pid))
    cmd = parse_file[1]
    # Valeur du TTY grace au tty_nr
    tty_nr = int(parse_file[6])
    tty = tty_process(tty_nr)
    # affichage du resultat
    print(str(pid)+ESPACE(str(pid))+tty+ESPACE(tty)+stat+'    '+time+'  '+cmd)

def PSU(pid):
    """
    AFFICHAGE DU PROCESSUS DU PID RENSEIGNE SOUS FORMAT UTILISATEUR: ps -u PID

    :param PID:
    :return:
    """

    with open('/proc/'+str(pid)+'/status','r') as file :
        parse_file = file.readlines()
        uid = parse_file[6].split()[1]
        user  =pwd.getpwuid(int(uid))[0]
        vsz = parse_file[11].split()[1]
        rss = parse_file[15].split()[1]

        try :
            int(vsz)
        except:
            vsz = '0'
        try :
            int(rss)
            if rss[:2] == '00':
                rss ='0'
        except:
            RSS='0'

        MEM = MEMOIRE(int(RSS))
        TIME = CPUTIME(PID)

        with open('/proc/'+ str(pid) +'/stat','r') as file2 :
            parse_file2 = file2.readlines()[0].split()
            cmd = parse_file2[1]
            tty_nr = int(parse_file2[6])
            tty = str(tty_process(tty_nr))
            stat = parse_file2[2]
            start = time.ctime(os.path.getctime('/proc/'+str(pid))).split()[3]
            cpu = '0.0'

            if len(user)>8:
                user = user[:7]



            RESULTS =user +ESPACE(user)+str(pid) +ESPACE(str(pid))+cpu+'  '+ MEM+'  '+vsz+ESPACE(vsz)+rss+ESPACE(rss)+tty+ESPACE(tty)+stat+'     '+start+'  '+time+'  '+cmd
            print(RESULTS[:int(columns)])




#creation des option avec optparse
parser = OptionParser()
parser.add_option('-e', dest="e", help="affiche tout les processus",
    action='store_true' )
parser.add_option('-u', dest="u", action='store_true', 
   help="affichage sous format utilisateur/[sans arg]affiche les process des autres users ",)
parser.add_option('-a', dest="a",  action='store_true',
    help="Affiche aussi les process (lance dans un terminal) des autres users",)
parser.add_option('-x', dest="x",  action='store_true',
    help="Afficher les processus de l'utilisateur qui ne sont pas dans un terminal", )

option, argument = parser.parse_args()


# gestion de l'execution de la commande
NONEFORMAT='PID      TTY      STAT     TIME  COMMAND'
USERFORMAT="USER     PID      %CPU %MEM VSZ      RSS      TTY      STAT  START     TIME      COMMAND"

#option -aux ou option -eu
if (option.e and option.u)or (option.a and option.u and option.x):
    print(USERFORMAT[:columns])
    for pid in all_pid():         #on affiche tous les Processus
        PSU(pid)

# option ax ou option e
elif option.e or (option.a and option.x):
    print(NONEFORMAT[:columns])
    # on affiche tous les Processus
    for pid in all_pid():
        cmd_ps(pid)
###############################################################
                                                    #option -ua
###############################################################
elif option.u and option.a:
    print(USERFORMAT[:columns])
    # le cas d'ajout d'autres PID
    if len(sys.argv) > 2:
        i=0
        list_pid = []   #permet d'eviter les affichages  en double
        while i < len(sys.argv):
            try:
                int(sys.argv[i])
                pid = sys.argv[i]
                if pid not in list_pid:
                    PSU(pid)
                list_pid+=[pid]
            except:
                pass
            i+=1
    #on affiche les resultats de l'otion
    for pid in a_pid():
        PSU(pid)

#option -ux
elif option.u and option.x:
    print(USERFORMAT[:columns])
    if len(sys.argv) > 2:          #le cas d'ajout d'autres PID
        i=0
        list_pid = []   #permet d'eviter les affichages  en double
        while i < len(sys.argv):
            try:
                int(sys.argv[i])
                pid = sys.argv[i]
                if pid not in list_pid:
                    PSU(pid)
                list_pid += [pid]
            except:
                pass
            i+=1
    for pid in x_pid():     #on affiche les resultats de l'otion
        PSU(pid)
###############################################################
                                                     #option -a
###############################################################
elif option.a:
    print(NONEFORMAT[:columns])

    if len(sys.argv) > 2:          #le cas d'ajout d'autres PID
        i = 0

        list_pid=[]   #permet d'eviter les affichages  en double
        while i < len(sys.argv):
            try:
                int(sys.argv[i])
                pid = sys.argv[i]
                if pid not in list_pid:
                    cmd_ps(pid)
                list_pid += [pid]
            except:
                pass
            i += 1
    for pid in a_pid():     #on affiche les resultats de l'otion
        cmd_ps(pid)
###############################################################
                                                     #option -u
###############################################################
elif option.u:
    i=0
    print(USERFORMAT[:columns])
    if len(sys.argv) > 2:          #le cas d'ajout d'autres PID
        i=0
        list_pid = []    #permet d'eviter les affichage  en double
        while i < len(sys.argv):
            try:
                int(sys.argv[i])
                PID=sys.argv[i]
                if PID not in list_pid:
                    PSU(PID)
                list_pid+=[PID]
            except:
                pass
            i+=1
    else:          # sinon on affiche les resultats de l'otion
        for pid in u_pid():
            PSU(pid)
###############################################################
                                                     #option -x
###############################################################		
elif option.x:
    print(NONEFORMAT[:columns])

    if len(sys.argv) > 2:         #le cas d'ajout d'autres PID
        i=0

        list_pid = []  #permet d'eviter les affichages  en double
        while i < len(sys.argv):
            try:
                int(sys.argv[i])
                pid = sys.argv[i]
                if pid not in list_pid:
                    cmd_ps(pid)
                list_pid += [pid]
            except:
                pass
            i+=1
    for pid in x_pid():     #on affiche les resultats de l'otion
        cmd_ps(pid)


# sans option
elif len(sys.argv) >= 2:
    i = 0
    # permet d'eviter les affichage  en double
    list_pid = []
    print(NONEFORMAT[:columns])
    while i < len(sys.argv):
        if i=='-a':
            cmd_ps(os.getpid())
        try:
            int(sys.argv[i])
            pid = sys.argv[i]
            if pid not in list_pid:
                cmd_ps(pid)
            list_pid += [pid]
        except:
            if i==(len(sys.argv)):
                print("aucun pid renseigne existant")
        i+=1
else:              # sinon on affiche les resultats de l'otion
    print(NONEFORMAT[:columns])
    for pid in pid_wthout_option():
        cmd_ps(pid)


