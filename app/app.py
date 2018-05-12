import requests
from bs4 import BeautifulSoup
import csv


def write_csv(data):
	with open('wildb.csv', 'a') as f:
		writer = csv.writer(f, delimiter=';', lineterminator='\n')
		writer.writerow( (data['brand'], data ['url'], data['price']))


def get_html(url):
	r = requests.get(url)
	return r.text


def contain_data(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = soup.find('div', class_='pageToInsert')
	return pages is not None


def get_page_datda(html):
	s = BeautifulSoup(html,'lxml')
	products = s.find('div', class_='catalog_main_table').find_all('div', class_='dtList')
	for ad in products:
		try:
                        brand = ad.find('div', class_='dtlist-inner-brand-name').find('strong').text.strip()
		except:
			brand=''
		try:
			url = ad.find('a').get('href')
		except:
			url=''
		try:
			price=ad.find('span', class_='price').find('ins').text.strip()
		except:
			price=ad.find('span', class_='price').find('span').text.strip()
		data = {'brand':brand, 'url':url , 'price': price}
		write_csv(data)


def main():
	base_url='https://www.wildberries.ru/catalog/zhenshchinam/odezhda/platya?'
	page_part='page='
	page=1
	while page  < 4:
		total_r=base_url+page_part+str(page)
		req=get_html(total_r)
		if contain_data(req):
			get_page_datda(req)
		else:
			break
		page+=1

	

if __name__ == '__main__':
    main()
