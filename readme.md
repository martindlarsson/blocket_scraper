Installera python

skapa en virtuell miljö (detta är redan gjort):
https://docs.python.org/3/tutorial/venv.html
1. python3 -m venv blocket-env
2. source blocket-env/bin/activate

Kör scrape_blocket.se

På maxplexserver (192.168.1.10):
Filerna synkas via Google Drive till Blockbuster (192.168.1.13)
Filerna är mountade via NFS till (maxplexserver) /mnt/Blocket där mappen AI/Python/Kod är mappad till Kod (1) under /mnt/Blocket. Vet inte varför den fick (1).

Kopierade filen scrape_blocket till /home/martin på maxplexserver och skapade ett cron jobb som körs varje dag kl 03:00
För att redigera kör crontab -e som martin på maxplexserver
Raden ser ut såhär:
0 3 * * * /home/martin/scrape_blocket.sh > /home/martin/cronlog.txt 2>&1

Den skriver en logg från cronjobbet till /home/martin/cronlog.txt

För att titta i databasen kör
sqlite3 car_add_database.db eller sqlite3 logg.db
Alla SQL kommandon avslutas med ;
Lista tabeller med .tables

Få ut CSV fil från databasen:
>sqlite3 car_add_database.db
.headers on
.mode csv
.output annonser.csv
SELECT * FROM car_adds;
.quit