test.sh : permet de faire le test de mycopy.py ou de ps.py
    execution:
              - lancer le terminal
              - se placer dans ce dossier avec cd 
              - depuis le terminal faire: bash test.sh script_à_tester
              - script_à_tester: soit mycopy.py, soit ps.py

***********************************************************************************************************

mycopy.py : permet de faire la copie recursif et intelligente du contenu du dossier from vers le dossier to
    execution:
              - lancer le terminal
              - se placer dans ce dossier avec cd 
              - depuis le terminal faire: python mycopy.py from to

***********************************************************************************************************

ps.py: permet de faire la meme chose que la commande shell ps 
       c'est à dire d'afficher les informations sur les processus
       il contient les options -u -x -e -a
       ps.py -x [PID] permet d'afficher les processus qui n'ont pas de terminal de contrôle.
       ps.py -a [PID] permet d'afficher en plus les processus des autres utilisateurs
       ps.py -u [PID] permet d'afficher les processus sous un autre format présentant le nom de l'utilisateur et l'heure de lancement.
       ps.py -e [PID] permet d'afficher tout les processus.
       IL est aussi possible de combiner plusieur option: ps [-][auxe] [PID] 
       
    execution:
              - lancer le terminal
              - se placer dans ce dossier avec cd 
              - depuis le terminal faire: bash test.sh ps.py [-][auxe] [PID]

***********************************************************************************************************
           

