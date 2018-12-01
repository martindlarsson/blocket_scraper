import parser
import datatyper



## test
add_ref = datatyper.Annons_ref(id = '', link = 'https://www.blocket.se/malmo/Mercedes_Benz_C_200_d_Kombi_Fleet_82465052.htm?ca=7&w=3', price = 10)
add = parser.parse_add(add_ref)

print(add)