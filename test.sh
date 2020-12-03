#!/bin/bash
if test "$1"
then

    if [ $1 = "mycopy.py" ]

    then
    		var=''
    		echo ----------------------------------------------------------
            echo 'CREATION DU DOSSIER "source" CONTENANT DES FICHIERS ET'
            echo "SOUS DOSSIERS DONT CERTAIN PARTAGEANT LE MEME INODE:::"
            echo ----------------------------------------------------------
             read -r -p '"q" POUR QUITTER | TOUCHE "ENTRER" POUR CONTINUER: ' var
            if test "$var"
            then
                if [ $var = "q" ]
                then 
            	   exit -1
       		    
                else
       			echo '

       			'
                fi
       		fi
            mkdir source
            touch source/file1
            touch source/file2
            mkdir source/sousdossier
            mkdir source/sousdossier2
            mkdir source/sousdossier2/sousdossier3
            touch source/sousdossier2/sousdossier3/file3.txt
            ln source/file1 source/sousdossier/hardlink_file1
            echo ----------------------------------------------------------
            ls -Rli source
            echo ----------------------------------------------------------
            echo 'COPIE DU DOSSIER "SOURCE" VERS LE DOSSIER "DESTINATION"'
            echo ----------------------------------------------------------
            read -r -p '"q" POUR QUITTER | TOUCHE "ENTRER" POUR CONTINUER: ' var2
            if test "$var2"
            then
                if [ $var2 = "q" ]
                then 
                   exit -1
                
                else
                echo '

                '
                fi
            fi
            python mycopy.py source destination
            ls -Rli destination
    elif [ $1 = "ps.py" ]
    then
    		echo ----------------------------------------------------------
    		echo "execution de la commande ps puis ps.py "
    		echo ----------------------------------------------------------
            read -r -p '"q" POUR QUITTER | TOUCHE "ENTRER" POUR CONTINUER: ' var3
            echo ''
            if test "$var3"
            then
                if [ $var3 = "q" ]
                then 
                   exit -1
                
                else
                echo '

                '
                fi
            fi
    		ps
            echo '
            
            '
    		python ps.py

    		echo ----------------------------------------------------------
    		echo "execution de la commande ps [pid] puis ps.py [pid] "
            echo "[pid] = 1 2 3 1 2 2 3 3 3 4 1 1 4 5 7 8 9 12 546 1254  "
    		echo ----------------------------------------------------------

            read -r -p '"q" POUR QUITTER | TOUCHE "ENTRER" POUR CONTINUER: ' var4
            echo ''
            if test "$var4"
            then
                if [ $var4 = "q" ]
                then 
                   exit -1
                
                else
                echo '

                '
                fi
            fi
    		ps 1 2 3 1 2 2 3 3 3 4 1 1 4 5 7 8 9 12 546 1254 5646
            echo '
            
            '
    		python ps.py 1 2 3 1 2 2 3 3 3 4 1 1 4 5 7 8 9 12 546 1254 5646


    		echo ----------------------------------------------------------
    		echo "execution de la commande ps x puis ps.py -x "
    		echo ----------------------------------------------------------
            read -r -p '"q" POUR QUITTER | TOUCHE "ENTRER" POUR CONTINUER: ' var5
            echo ''
            if test "$var5"
            then
                if [ $var5 = "q" ]
                then 
                   exit -1
                
                else
                echo '

                '
                fi
            fi
    		ps x 
            echo '
            
            '
    		python ps.py -x 

  		    echo ----------------------------------------------------------
    		echo "execution de la commande ps -x [pid] puis ps.py -x [pid]"
    		echo "[pid] = 1 1 2 2 3 4 5 6 7 8 2 3 "
    		echo ----------------------------------------------------------
            read -r -p '"q" POUR QUITTER | TOUCHE "ENTRER" POUR CONTINUER: ' var6
            echo ''
            if test "$var6"
            then
                if [ $var6 = "q" ]
                then 
                   exit -1
                
                else
                echo '

                '
                fi
            fi


    		ps x 1 1 2 2 3 4 5 6 7 8 2 3 
            echo '
            
            '
    		python ps.py -x 1 1 2 2 3 4 5 6 7 8 2 3
    		echo ''
    		echo ----------------------------------------------------------
    		echo "execution de la commande ps u puis ps.py -u "
    		echo ----------------------------------------------------------
            read -r -p '"q" POUR QUITTER | TOUCHE "ENTRER" POUR CONTINUER: ' var7
            echo ''
            if test "$var7"
            then
                if [ $var7 = "q" ]
                then 
                   exit -1
                
                else
                echo '

                '
                fi
            fi

    		ps u 
            echo '
            
            '
    		python ps.py -u 
    		echo ----------------------------------------------------------
    		echo "execution de la commande ps -u [pid] puis ps.py -u [pid] "
    		echo "[pid] = 1 1 2 2 3 4 5 6 7 8 2 3 "
    		echo ----------------------------------------------------------

            read -r -p '"q" POUR QUITTER | TOUCHE "ENTRER" POUR CONTINUER: ' var8
            echo ''
            if test "$var8"
            then
                if [ $var8 = "q" ]
                then 
                   exit -1
                
                else
                echo '

                '
                fi
            fi
    		ps u 1 1 2 2 3 4 5 6 7 8 2 3
            echo '

            '
    		python ps.py -u 1 1 2 2 3 4 5 6 7 8 2 3


            echo ----------------------------------------------------------
            echo "execution de la commande ps xua [pid] puis ps.py -xua "
            echo ----------------------------------------------------------

            read -r -p '"q" POUR QUITTER | TOUCHE "ENTRER" POUR CONTINUER: ' var9
            echo ''
            if test "$var9"
            then
                if [ $var9 = "q" ]
                then 
                   exit -1
                
                else
                echo '

                '
                fi
            fi
            ps xua 
            echo '
            
            '
            python ps.py -xau 


    else
    		echo "VOUS DEVEZ ENTRER LE SCRIPT A TESTER EN ARGUMENT : [ps.py ou mycopy.py]"

    fi

else
    echo "VOUS DEVEZ ENTRER LE SCRIPT A TESTER EN ARGUMENT : [ps.py ou mycopy.py]"
fi