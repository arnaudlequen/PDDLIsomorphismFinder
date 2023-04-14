for dir in */; do
	cd $dir
	echo $dir
	grep -r ": FOUND" | wc -l
	grep -r "NOT FOUND" | wc -l
	cd ..
done
