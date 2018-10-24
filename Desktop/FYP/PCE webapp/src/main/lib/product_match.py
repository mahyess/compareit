from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from .scraper import main as scraper

def product_match(base_title, base_price, query_title, query_price):
	return bool(title_match(base_title, query_title) * price_match(base_price, query_price))

def title_match(bt, qt):
	pt = fuzz.token_set_ratio(bt, qt)
	pr = True if pt >= 80 else False
	return pr

def price_match(bp, qp):
	bh = bp + 0.1 * bp
	bl = bp - 0.1 * bp
	br = True if bl <= qp <= bh else False
	qh = qp + 0.1 * qp
	ql = qp - 0.1 * qp
	qr = True if ql <= bp <= qh else False
	return bool(br + qr)

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
		for idy, listed_item in enumerate(cleaned_scrap_data):
			check = False
			# print(idx, ' - ', idy)
			check = product_match(listed_item['title'], listed_item['price']['min_price'], scrap[idx]['details']['title'], scrap[idx]['details']['price']['selling_price'])
			if check:
				# print('\n------------------\n')
				cleaned_scrap_data[idy]['options'].append({
					'origin': scrap[idx]['details']['origin'],
					'url': scrap[idx]['details']['url'],
					'title': scrap[idx]['details']['title'],
					'image': scrap[idx]['details']['image'],
					'price': {
						'marking_price': scrap[idx]['details']['price']['marking_price'],
						'selling_price': scrap[idx]['details']['price']['selling_price']
					}
				})
				# for update of title, if valid
				cleaned_scrap_data[idy]['title'] = df_title(cleaned_scrap_data[idy]['title'], scrap[idx]['details']['title'])
				# for update of outside prices
				if scrap[idx]['details']['price']['marking_price'] is None:
					# for max price, if marking price exists in scraped data
					cleaned_scrap_data[idy]['price']['max_price'] = max_df_price(cleaned_scrap_data[idy]['price']['max_price'], scrap[idx]['details']['price']['selling_price'])

				else:
					cleaned_scrap_data[idy]['price']['max_price'] = max_df_price(cleaned_scrap_data[idy]['price']['max_price'], scrap[idx]['details']['price']['marking_price'])
					# for max price, if marking price doesn't exist in scraped data
				# for min price
				cleaned_scrap_data[idy]['price']['min_price'] = min_df_price(cleaned_scrap_data[idy]['price']['min_price'], scrap[idx]['details']['price']['selling_price'])
				break

		if not check:
			cleaned_scrap_data.append({
				'id': len(cleaned_scrap_data),
				'title': scrap[idx]['details']['title'],
				'price': {
					'max_price': scrap[idx]['details']['price']['marking_price'] if bool(scrap[idx]['details']['price']['marking_price']) else scrap[idx]['details']['price']['selling_price'],
					'min_price': scrap[idx]['details']['price']['selling_price']
					},
				'image': scrap[idx]['details']['image'],
				'options': [{
					'origin': scrap[idx]['details']['origin'],
					'url': scrap[idx]['details']['url'],
					'title': scrap[idx]['details']['title'],
					'image': scrap[idx]['details']['image'],
					'price': {
						'marking_price': scrap[idx]['details']['price']['marking_price'],
						'selling_price': scrap[idx]['details']['price']['selling_price']
						}
					}]
				})

		# print(item)

def main(query):
	cleaned_scrap_data.clear()
	clean_scrap_data(scraper(query))
	data = cleaned_scrap_data
	# print(data)
	return data

if __name__ == '__main__':
	main(query)