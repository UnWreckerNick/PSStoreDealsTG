import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
from config import BASE_URL


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}


def get_html(base_url):
	response = requests.get(base_url, headers=HEADERS)
	response.raise_for_status()
	return response.text


def safe_get_text(element, default="N/A"):
	return element.text.strip() if element is not None else default


def format_price(price_str):
	if price_str == "N/A":
		return price_str
	price_str = price_str.replace('\xa0', '').replace('TL', '').strip()
	parts = price_str.split(',')
	if len(parts) == 2:
		whole = parts[0].replace('.', '')
		decimal = parts[1]
		return f"{whole},{decimal}TL"
	return f"{price_str.replace('.', '')}"


def format_date(date_str):
	if date_str == "N/A":
		return "N/A"

	pattern1 = r"Offer ends (\d{1,2})/(\d{1,2})/(\d{4}) (\d{1,2}:\d{2} [AP]M) (UTC|GMT[+-]\d{1,2})"
	pattern2 = r"Offer ends (\d{1,2})/(\d{1,2})/(\d{4}) (\d{1,2}:\d{2} [AP]M) GMT([+-]\d{1,2})"

	match = re.search(pattern1, date_str)
	if match:
		day, month, year, time_str, offset_str = match.groups()
		time_obj = datetime.strptime(time_str, "%I:%M %p")
		time_24h = time_obj.strftime("%H:%M")

		if offset_str == "UTC":
			date_time_str = f"{day}/{month}/{year} {time_24h} +0000"
		else:
			if offset_str.startswith('GMT'):
				offset_match = re.search(r'GMT([+-]\d{1,2})', offset_str)
				if offset_match:
					offset_num = offset_match.group(1)
					if not offset_num.startswith('+'):
						offset_num = f"+{offset_num}"
					offset_str = f"{offset_num:0>3}00"
			date_time_str = f"{day}/{month}/{year} {time_24h} {offset_str}"

		try:
			date_time_obj = datetime.strptime(date_time_str, "%d/%m/%Y %H:%M %z")
			return date_time_obj.isoformat()
		except ValueError as e:
			print(f"Failed to parse date string format 1: {date_str} - Error: {e}")
			return "N/A"

	match2 = re.search(pattern2, date_str)
	if match2:
		day, month, year, time_str, offset = match2.groups()
		time_obj = datetime.strptime(time_str, "%I:%M %p")
		time_24h = time_obj.strftime("%H:%M")

		if not offset.startswith(('+', '-')):
			offset = f"+{offset}"

		date_time_str = f"{day}/{month}/{year} {time_24h} {offset:0>3}00"

		try:
			date_time_obj = datetime.strptime(date_time_str, "%d/%m/%Y %H:%M %z")
			return date_time_obj.isoformat()
		except ValueError as e:
			print(f"Failed to parse date string format 2: {date_str} - Error: {e}")
			return "N/A"

	print(f"No matching pattern found for date string: {date_str}")
	return "N/A"


def parse_offer_end_date(game_url):
	try:
		html = get_html(''.join(["https://store.playstation.com", game_url]))
		soup = BeautifulSoup(html, "html.parser")

		selectors = [
			'span[data-qa$="#discountDescriptor"]',
			'span[data-qa$="mfeCtaMainOffer1#discountDescriptor"]',
			'span[class*="psw-c-t-2"]'
		]

		for selector in selectors:
			date_elements = soup.select(selector)
			for date_element in date_elements:
				raw_date = safe_get_text(date_element, default="N/A")
				if "Offer ends" in raw_date:
					offer_end_date = format_date(raw_date)
					if offer_end_date != "N/A":
						return offer_end_date

		return "N/A"

	except Exception as e:
		print(f"Error parsing game details page {game_url}: {e}")
		return "N/A"


def parse_deals(html):
	soup = BeautifulSoup(html, "html.parser")
	games = []

	for game_card in soup.select("a.psw-link.psw-content-link"):
		try:
			name_element = game_card.select_one("[data-qa$='#product-name']")
			if not name_element:
				print("Skipping game card - no name found")
				continue

			name = safe_get_text(name_element)

			discount_price = safe_get_text(game_card.select_one("[data-qa$='#price#display-price']"))
			base_price = safe_get_text(game_card.select_one("[data-qa$='#price#price-strikethrough']"))
			discount_percent = safe_get_text(game_card.select_one("[data-qa$='#discount-badge#text']"))

			formatted_discount_price = format_price(discount_price)
			formatted_base_price = format_price(base_price)

			link = game_card.get("href", "")
			if not link:
				print(f"Warning: No URL found for game {name}")

			if discount_price != "N/A":
				offer_end_date = parse_offer_end_date(link)

				print(f"Title: {name}")
				print(f"Discount price: {formatted_discount_price} TL")
				print(f"Original price: {formatted_base_price} TL")
				print(f"Discount: {discount_percent}")
				print(f"Link: {link}")
				print(f"Offer end date: {offer_end_date}")
				print("---")

				games.append({
					"name": name,
					"base_price": formatted_base_price,
					"discount_price": formatted_discount_price,
					"discount_percent": discount_percent,
					"url": link,
					"offer_end_date": offer_end_date
				})
			else:
				print(f"Skipping game {name} - no valid price found")

		except Exception as e:
			print(f"Error during game processing: {str(e)}")
			continue

	return games


def get_last_page(base_url):
	html = get_html(base_url + "1")
	soup = BeautifulSoup(html, "html.parser")

	page_buttons = soup.select('button[data-qa^="ems-sdk-grid#ems-sdk-top-paginator-root#page"]')
	if not page_buttons:
		print("Warning: Could not find last page button, assuming single page.")
		return 1

	last_page_button = page_buttons[-1]
	last_page_number_str = last_page_button.get('data-qa').split('page')[-1]
	try:
		return int(last_page_number_str)
	except:
		print("Warning: Could not parse last page number, assuming single page")
		return 1


def save_to_json(data, filename="psn_deals_full.json"):
	with open(filename, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=4)
	print(f"The data has been successfully saved to a file {filename}")


if __name__ == "__main__":
	try:
		last_page = get_last_page(BASE_URL)
		all_deals = []
		for i in range(1, last_page):
			url = f"{BASE_URL}{i}"
			print (f"Fetching data from {url}")
			html_content = get_html(url)
			deals = parse_deals(html_content)
			all_deals.extend(deals)
		save_to_json(all_deals)
	except Exception as e:
		print(f"Error occurred: {e}")