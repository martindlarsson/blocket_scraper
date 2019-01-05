import database
import datatyper
import parser
import logg

# ver 1.3

## Koppla upp oss mot databasen eller skapa en ny fil om den inte finns
database.init()

logg.save(message = u'Startar skrapning av blocket')

add_refs_read = 0
add_refs_saved = 0

batch_size_db = 1000


# Parse all adds on "first page"
start_page = 1
page_batch_size = 20
adds_left_to_parse = True
while adds_left_to_parse:
    try:
        car_add_refs = parser.parse_add_refs("https://www.blocket.se/hela_sverige?q=&cg=1020&w=3&st=s&mys=2000&fu=&pl=0&ca=7&is=1&l=0&md=th", start_page, page_batch_size)

        if len(car_add_refs) == 0:
            # Logga att vi skrapat klart
            logg.save(message = u'Läst in alla annonser referenser')
            adds_left_to_parse = False
            break

        ## Debugging
        # if (add_refs_saved >= 5000):
        #     break

        add_refs_read += len(car_add_refs)

        # Save all adds in the staging tabel
        no_inserted_add_refs = database.insert_car_add_refs(car_add_refs)

        # Incement adds saved counter
        add_refs_saved += no_inserted_add_refs

        # Log
        logg.save(message = u'Sparat ' + str(no_inserted_add_refs) + ' annonser i staging-tabellen av ' + str(len(car_add_refs)) + '. ' + str(add_refs_saved) + ' annonser sparade totalt')

        # increment the start page
        start_page += page_batch_size
    except Exception as exec:
        # Log
        logg.save(message = u'Fick ett fel vid skrapning av blockets förstasida. Sida: ' + str(start_page) + ', fel: ' + str(exec))

        # increment the start page
        start_page += page_batch_size


# Fetch all new add refs
new_add_refs = database.get_all_new_adds()

# Log
logg.save(message = str(len(new_add_refs)) + ' nya annonser att skrapa')

new_adds_to_save = []
adds_saved = 0
adds_not_parsed = 0
# Parse the new adds
for add_ref in new_add_refs:
    try:
        add = parser.parse_add(add_ref)

        if (add is not None):
            new_adds_to_save.append(add)
        else:
            adds_not_parsed += 1

        # Save adds when batch is more than 100
        if (len(new_adds_to_save) >= batch_size_db):
            # Save them
            row_count = database.insert_car_adds(new_adds_to_save)
            adds_saved += row_count
            # Log
            logg.save(message = 'Sparat ' + str(row_count) + ' nya annonser. Totalt ' + str(adds_saved))
            # Clear the list
            new_adds_to_save = []

    except Exception as exc:
        logg.save(message = 'Fel vid parsning eller sparande av annons. Error: ' + str(exc))


# Save the remaining adds
if (len(new_adds_to_save) > 0):
    try:
        row_count = database.insert_car_adds(new_adds_to_save)
        adds_saved += row_count
        # Log
        logg.save(message = 'Sparat de sista ' + str(row_count) + ' nya annonserna. Totalt ' + str(adds_saved))
    except Exception as exc:
        logg.save(message = 'Fel vid sparande av annons. Error: ' + str(exc))


new_adds_saved = adds_saved
logg.save(message = 'Klar med att skrapa nya annonser. ' + str(adds_not_parsed) + ' av ' + str(len(new_add_refs)) + ' nya annonser kunde inte skrapas.')

# Update adds with new prices
updated_add_refs = database.get_all_updated_adds()

logg.save(message = str(len(updated_add_refs)) + ' annonser att uppdatera. Påbörjar skrapning.')

updated_adds = []
adds_saved = 0
adds_not_parsed = 0
# Parse the updated adds
for add_ref in updated_add_refs:
    try:
        add = parser.parse_add(add_ref)

        if (add is not None):
            updated_adds.append(add)
        else:
            adds_not_parsed += 1

        # Save adds when batch is more than 100
        if (len(updated_adds) >= batch_size_db):
            # Save them
            database.update_car_adds(updated_adds)
            adds_saved += len(updated_adds)
            # Log
            logg.save(message = 'Uppdaterat ' + str(len(updated_adds)) + ' annonser. Totalt ' + str(adds_saved))
            # Clear the list
            updated_adds = []

    except Exception as exc:
        logg.save(message = 'Fel vid parsning eller uppdatering av annons. Error: ' + str(exc))

# Update the remaining adds
try:
    if (len(updated_adds) > 0):
        # Save them
        database.update_car_adds(updated_adds)
        adds_saved += len(updated_adds)
        # Log
        logg.save(message = 'Uppdaterat ' + str(len(updated_adds)) + ' annonser. Totalt ' + str(adds_saved))
        # Clear the list
        updated_adds = []

except Exception as exc:
    logg.save(message = 'Fel vid uppdatering av annons. Error: ' + str(exc))


logg.save(message = 'Klar med att skrapa uppdaterade annonser. ' + str(adds_not_parsed) + ' av ' + str(len(updated_add_refs)) + ' uppdaterade annonser kunde inte skrapas.')

# touch the rest of the adds with the last_seen date
no_updated_adds = database.update_all_seen_adds()

# Log
logg.save(message = 'Uppdaterat ' + str(no_updated_adds) + ' annonser med last_seen-datum')


# clean staging table
database.finish_up()


# Log
logg.save(message = 'Klar! ' + str(new_adds_saved) + ' nya annonser sparade och ' + str(adds_saved) + ' annonser uppdaterades med nytt pris.')

