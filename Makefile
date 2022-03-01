
main:
	make satsolver
	make touistparse
	cd ./ANTLR && ./build.sh
	mkdir solvedata
	mkdir tmp

satsolver:
	cd ./Solvers/Sources/MapleLCMDistChronoBT/sources/simp && make rs
	mv ./Solvers/Sources/MapleLCMDistChronoBT/sources/simp/glucose_static Solvers/Bin/glucose_static_maplelcmd

touistparse:
	cd ./Solvers/Sources/touistplan/ && make
	mv ./Solvers/Sources/touistplan/touistparse ./Solvers/
