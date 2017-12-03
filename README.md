zagraj.pl games parser
======================

As of December 2016, zagraj.pl is the only place you can play Polish Scrabble on-line. After each game, a report is sent to the players via e-mail. Below is an example report:

```
Ten list zostal wysłany przez system gier on-line ZAGRAJ PL
Zapis partii SCRABBLE
Data: Thu Aug 03 20:00:13 CEST 2017
Miejsce: Server ZAGRAJ.PL, plansza 9
Typ: turniejowa
Czas: 5 min
Gracz 1: alkamid
Ranking: 103
Gracz 2: amarant53
Ranking: 116
Wynik: 389: 224

    1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
  +-------------------------------+
A | E L           S         M A J |
B | M I           I           L A |
C |   P U C Z     E   G     H   K |
D | O N   E N     W J A Z D Y   Ó |
E | T Y   W A S   Y   Z     R E W |
F | O     Y   Z       D       Ś   |
G | M         A     S Ą D         |
H | A       P Ł A C E             |
I | N       R   L I M             |
J | A     T Ę     Ź   P           |
K |   T   O Ż   G   K I Ć         |
L | H O   R Y C I N O             |
M |   R E F     K O Ń             |
N |   E   U   N I W               |
O |   B           I               |
  +-------------------------------+
alkamid	amarant53
Litery	Ruch	Pkt	Suma	Litery	Ruch	Pkt	Suma
TPCARŁL	PŁAC	16	16	RE_MOIL	LIM/AL/CI	17	17
TRĘURŻL	PRĘŻ	26	42	RE_EOSB	SEM/PŁACE	14	31
TOŹURFL	TORFU/TĘ/OŻ	37	79	RT_EOEB	EF	12	43
IYŹWWCL	CIŹ	12	91	RT_OOEB	TOREB/REF	23	66
IYNWWCL	RYCIN/PRĘŻY	23	114	IH_ZOHW	NOWI	12	78
JZZWWKL	*wymiana* ZJKWL	0	114	_H_ZAHS	HO	7	85
ZGZAWDĄ	GAZDĄ/SĄ	22	136	_E_ZAHS	SZAŁ	8	93
JJZDWAO	WJAZD	18	154	_E_ICHR	HYR/WJAZDY	16	109
ÓJAWŃAO	OŃ/RYCINO/OŃ	38	192	IE_ICŚK	EŚ/RE	18	127
ÓJAWYAK	JAKÓW/REW	54	246	IN_ICĆK	KIĆ/KOŃ	28	155
GNKZYAI	GIK/KOŃ	20	266	EN_ICUM	NIW/GIKI	12	167
LNLZYAI	AL/AJ/LA	16	282	EM_ICUM	MAJ	6	173
ANLZYNI	ZNA/AS	10	292	EA_ICUM	UCZ	12	185
IPLEYNI	LIPNY/PUCZ	24	316	EA_IZPM	EM/EL/MI	21	206
ODTESOI	OTO/ON/TY	12	328	AA_IZPN	OTOMANA	21	227
YDWESEI	CEWY/EN/WAS	19	347	BASIZPŁ	PI	7	234
DY SEI	EW	2	349	BASIZ Ł	*pas*	0	234
DY S I	EWY	4	353	BASIZ Ł	*pas*	0	234
D S I	SIEWY	18	371	BASIZ Ł	*pas*	0	234
D	SĄD	8	379	-	-	0	234
*litery*	10	389	BASIZ Ł	*litery*	-10	224

```

There are two major issues with this report:
1. It doesn't highlight the blanks in any way on the board (they only appear in racks as "_"), so some plays are ambiguous.
2. There is no indication about the position of the moves. We can read it from the board, but if there are duplicate words on the board, again the situation is ambiguous.

The aim of the parser is to resolve these two ambiguities whenever possible and output a report in the [.gcg](http://www.poslfit.com/scrabble/gcg/) format.

Ideally this should be a web service for zagraj.pl players to use, but for now I'll focus on parsing the reports in Python.