scp -r alequen@c8ni.irit.fr:~/PRIVE/PDDLIsofinder/Results/custom/* .
for dir in */
do 
	python3 make_graphs.py $dir
done
python3 make_overview.py
