for dir in */
do 
	python3 make_graphs.py $dir
done
python3 make_overview.py
