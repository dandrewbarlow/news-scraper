
run:
	python3 news-scraper.py

install:
	pip3 install -r requirements.txt

clean:
	rm results/*.csv
