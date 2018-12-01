import requests
from bs4 import BeautifulSoup
import datatyper

# Parse the 
def parse_add_refs(base_url, start_page, pages_batch_size):

    car_add_refs = [ ]

    annonser_kvar_att_lasa = True

    page = start_page
    last_page = start_page + pages_batch_size

    ## Läser in alla annonser på "förstasidan"
    while page < last_page:

        allaAnnonser = requests.get(base_url + "&o=" + str(page))
        soup = BeautifulSoup(allaAnnonser.content, 'html.parser')

        annonser = soup.find_all('article', { 'class' : 'item_row' })

        annonser_kvar_att_lasa = len(annonser) > 0

        if (annonser_kvar_att_lasa == False):
            break

        for annons in annonser:
            id = annons.attrs['id']

            linkTag = annons.find('a', { 'class' : 'item_link' })
            prisTag = annons.find('p', { 'class' : 'list_price' })

            pris = 0

            try:
                if prisTag is not None:
                    pris = int(prisTag.text.replace(" ", "").replace("kr", "").strip())
            except ValueError:
                pris = 0

            if (linkTag != None):
                nyAnnons = datatyper.Annons_ref(id = id, link = linkTag.attrs['href'], price = pris)
                car_add_refs.append(nyAnnons)

        page += 1 # Räkna upp sidan

    return car_add_refs


def parse_add(add_ref):

        annonsen = requests.get(add_ref.link)
        soup = BeautifulSoup(annonsen.content, 'html.parser')

        # Fetch all attributes

        # price
        price_tag = soup.find('div', { 'id' : 'vi_price' })
        price = 0

        try:
            if price_tag is not None:
                price = int(price_tag.text.replace(" ", "").replace("kr", "").strip())
        except ValueError:
            price = 0

        # geo location
        geo_tag = soup.find('span', { 'class': 'area_label'})
        if (geo_tag is not None):
            geo = geo_tag.text.replace('(','').replace(')','').strip()
        else:
            geo = ""

        detail_square = soup.find('div', { 'id' : 'item_details' })
        details = detail_square.find_all('dl')

        for detail in details:
            detail_title = detail.find('dt').text
            detail_value = detail.find('dd').find('strong').text

            if (detail_title == "Modellår"):
                model_year = detail_value.strip()

            if (detail_title == "Växellåda"):
                grear = detail_value.strip()

            if (detail_title == "Miltal"):
                milage = detail_value.strip()

            if (detail_title == "Tillverkningsår"):
                make_year = detail_value.strip()

            if (detail_title == "Bränsle"):
                fuel = detail_value.strip()

        # Extra info
        extra_square = soup.find('dl', { 'class' : 'motor-extradata-details' })

        if (extra_square is None):
            return None

        all_title_tags = extra_square.find_all('dt')
        all_value_tags = extra_square.find_all('dd')

        extra_info_dict = {}

        for x in range(len(all_title_tags)):
            extra_info_dict[all_title_tags[x].text] = all_value_tags[x].text

        brand = extra_info_dict["Märke"].strip()
        model = extra_info_dict["Modell"].strip()
        car_type = extra_info_dict["Biltyp"].strip()
        hp = extra_info_dict["Hästkrafter"].replace(' Hk', '').strip()

        add_date = None
        time_tag = soup.find('time')
        if (time_tag is not None):
            add_date = time_tag['datetime'].strip()

        add = datatyper.Car_Add(id = add_ref.id, regnr = "", price = price, brand = brand, model = model, model_year = model_year, make_year = make_year, gear = grear, fuel = fuel, milage = milage, type = car_type, hp = hp, geo = geo, add_date = add_date)

        return add