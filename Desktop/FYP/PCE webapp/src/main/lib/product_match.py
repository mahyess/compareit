from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from .scraper import main as scraper

def product_match(base_title, base_price, query_title, query_price):
	return bool(title_match(base_title, query_title) * price_match(base_price, query_price))

def title_match(bt, qt):
	pt = fuzz.token_set_ratio(bt, qt)
	pr = True if pt >= 90 else False
	return pr

def price_match(bp, qp):
	bh = bp + 0.1 * bp
	bl = bp - 0.1 * bl
	br = True if bl <= qp <= bh else False
	qh = qp + 0.1 * qp
	ql = qp - 0.1 * qp
	qr = True if ql <= bp <= qh else False
	return bool(br * qr)

def df_title(dt, nt):
	return dt if len(dt) < len(nt) else nt

def max_df_price(dp, np):
	return dp if dp > np else np

def min_df_price(dp, np):
	return dp if dp < np else np

cleaned_scrap_data = []

def clean_scrap_data(scrap):
	for idx, item in enumerate(scrap):
		check = False
		for listed_item in cleaned_scrap_data:
			print('hi')
			check = product_match(scrap['details']['title'], listed_item['options']['title'])
			if check:
				# print('\n------------------\n')
				cleaned_scrap_data[idx]['options'].append({
					'origin': scrap['details']['origin'],
					'url': scrap['details']['url'],
					'title': scrap['details']['title'],
					'image': scrap['details']['image'],
					'price': {
						'marking_price': scrap['details']['marking_price'],
						'selling_price': scrap['details']['selling_price']
						}
					})
				# for update of title, if valid
				cleaned_scrap_data[idx]['title'] = df_title(cleaned_scrap_data[idx]['title'], scrap['details']['title'])
				# for update of outside prices
				if scrap['details']['price']['marking_price'] is not None:
					# for max price, if marking price exists in scraped data
					cleaned_scrap_data[idx]['price']['max_price'] = max_df_price(cleaned_scrap_data[idx]['price']['max_price'], scrap['details']['price']['marking_price'])
				else:
					# for max price, if marking price doesn't exist in scraped data
					cleaned_scrap_data[idx]['price']['max_price'] = max_df_price(cleaned_scrap_data[idx]['price']['max_price'], scrap['details']['price']['selling_price'])
				# for min price
				cleaned_scrap_data[idx]['price']['min_price'] = min_df_price(cleaned_scrap_data[idx]['price']['min_price'], scrap['details']['price']['selling_price'])
				break

		if not check:
			cleaned_scrap_data.append({
				'id': idx,
				'title': scrap['details']['title'],
				'price': {
					'max_price': scrap['details']['marking_price'],
					'min_price': scrap['details']['selling_price']
					},
				'options': [{
					'origin': scrap['details']['origin'],
					'url': scrap['details']['url'],
					'title': scrap['details']['title'],
					'image': scrap['details']['image'],
					'price': {
						'marking_price': scrap['details']['marking_price'],
						'selling_price': scrap['details']['selling_price']
						}
					}]
				})

		# print(item)

def main(query):
	return clean_scrap_data(scraper(query))

if __name__ == '__main__':
	main()