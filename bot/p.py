import requests

# Здесь вставьте URL вашего API и параметры запроса, если они необходимы
api_url = "https://rubaru.bz/stock_csv.php?id=pakaloco&code=IpvaPLnSEl6Iq*J8"
params = {
    "param1": "value1",
    "param2": "value2",
}

# Выполните запрос к API
response = requests.get(api_url, params=params)
print()
lines = response.text.strip().split('\n')

# Проход по строкам и форматирование в нужный вид
for line in lines:
    parts = line.split(';')
    print(parts)
    # Проверка, есть ли достаточно элементов в строке
    if len(parts) >= 10:
        ie_xml_id = parts[0].split('#')[0]
        ie_name = parts[1].strip('"')
        ip_prop1249 = parts[2].strip('"')
        ip_prop1250 = parts[3].strip('"')
        ic_group0 = parts[4].strip('"')
        ic_group1 = parts[5].strip('"')
        ic_group2 = parts[6].strip('"')
        ip_prop1446 = parts[7].strip('"')
        cp_quantity = parts[8].strip('"')
        cv_price_12 = parts[9].strip()
    
        formatted_line = f"{ie_xml_id};{ie_name};{ip_prop1249};{ip_prop1250};" \
                        f"{ic_group0};{ic_group1};{ic_group2};" \
                        f"{ip_prop1446};{cp_quantity};{cv_price_12}"
    
        print(formatted_line)
        
    else:
        print("Недостаточно данных в строке.")