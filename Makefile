
run:
	./news-scraper.py -y

install:
	pip3 install -r requirements.txt

clean:
	rm results/*.csv
