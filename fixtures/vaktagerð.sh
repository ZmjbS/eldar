#!/bin/bash

outfile='vaktir.xml'

echo '<?xml version="1.0" encoding="utf-8"?>' > $outfile
echo '<django-objects version="1.0">' >> $outfile

vakt=1
tmp=1
for ((stod=1;$stod<=7;stod++)); do
	for ((timabil=1;$timabil<=34;timabil++)); do
		lagmark=2
		hamark=4
		case $timabil in
			'1'|'2'|'3'|'4'|'5'|'6'|'7') tegund=1;; # Undirbúningur
			'12'|'18'|'24'|'30') tegund=3; lagmark=1; hamark='' ;;	# Næturvakt
			'13'|'19'|'25'|'31') tegund=4 ;;			# Stuðningur
			*) tegund=2 ;;						# Söluvakt
		esac
		echo '<object model="vaktir.vakt" pk="'$vakt'"><field rel="ManyToOneRel" name="timabil" to="vaktir.timabil">'$timabil'</field><field rel="ManyToOneRel" name="starfsstod" to="vaktir.starfsstod">'$stod'</field><field name="lagmark" type="SmallIntegerField">2</field> <field name="hamark" type="SmallIntegerField">4</field><field rel="ManyToOneRel" name="tegund" to="vaktir.tegund">'$tegund'</field></object>' >> $outfile; vakt=$(($vakt+1))
	done
done

# Akstur og Stjórnstöð eru stuðningsvaktir
tegund=4

stod=8
lagmark=2
hamark=3
for ((timabil=1;$timabil<=34;timabil++)); do
	case $timabil in
		'12'|'18'|'24'|'30') ;; # Ekki neitt á næturvöktum í stjórnstöð
		*) echo '<object model="vaktir.vakt" pk="'$vakt'"><field rel="ManyToOneRel" name="timabil" to="vaktir.timabil">'$timabil'</field><field rel="ManyToOneRel" name="starfsstod" to="vaktir.starfsstod">'$stod'</field><field name="lagmark" type="SmallIntegerField">2</field> <field name="hamark" type="SmallIntegerField">4</field><field rel="ManyToOneRel" name="tegund" to="vaktir.tegund">'$tegund'</field></object>' >> $outfile; vakt=$(($vakt+1)) ;;
	esac
done

stod=9
lagmark=2
hamark=2
for ((timabil=1;$timabil<=34;timabil++)); do
	case $timabil in
		'12'|'18'|'24'|'30') ;; # Ekki neitt á næturvöktum í akstri
		*) echo '<object model="vaktir.vakt" pk="'$vakt'"><field rel="ManyToOneRel" name="timabil" to="vaktir.timabil">'$timabil'</field><field rel="ManyToOneRel" name="starfsstod" to="vaktir.starfsstod">'$stod'</field><field name="lagmark" type="SmallIntegerField">2</field> <field name="hamark" type="SmallIntegerField">4</field><field rel="ManyToOneRel" name="tegund" to="vaktir.tegund">'$tegund'</field></object>' >> $outfile; vakt=$(($vakt+1)) ;;
	esac
done

echo '</django-objects>' >> $outfile
