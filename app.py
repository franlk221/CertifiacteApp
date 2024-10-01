import json
import argparse
import datetime as dt


#default args
FISCAL_YEAR_TRAININGS = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
FISCAL_YEAR = 2024
EXPIRED_TRAININGS_DATE = dt.date(2023, 10, 1)#october 1st 2023
SOON_TO_EXPIRE_DATE = EXPIRED_TRAININGS_DATE + dt.timedelta(days=31)


#part 1 trainings count 
def certificate_counts(data):
    training_counts = {}
    for person in data:
        dupes = []
        for cert in person['completions']:
            cert_name = cert['name']
            if cert_name not in training_counts:
                training_counts[cert_name] = 1
            elif cert_name not in dupes:
                training_counts[cert_name] += 1
            dupes.append(cert_name)

    with open('complete_trainings_count.json', 'w') as file1:
        json.dump(training_counts, file1, indent=2, sort_keys=True)
    
    
#part 2 fiscal year list
def fiscal_year_certificates(data, year):
    fiscal_start = dt.date(FISCAL_YEAR - 1, 7, 1)
    fiscal_end = dt.date(FISCAL_YEAR, 6, 30)
    certs_to_people = {cert: [] for cert in FISCAL_YEAR_TRAININGS}
    for person in data:
        for cert in person['completions']:
            cert_name = cert['name']
            try:
                cert_date = dt.datetime.strptime(cert['timestamp'], '%m/%d/%Y').date()
            except:
                continue
                
            if cert_name in FISCAL_YEAR_TRAININGS and fiscal_start <= cert_date <= fiscal_end \
                and person['name'] not in certs_to_people[cert_name]:
                certs_to_people[cert_name].append(person['name'])

    with open(f'certs_obtained_fiscal_{year}.json', 'w') as file2:
        json.dump(certs_to_people, file2, indent=2, sort_keys=True)

#part 3 expired and soon to expire(within a month) trainings
def expired_certificates(data):
    expired_certs = {}

    for person in data:
        certs = []
        non_dupes = {}
        for cert in person['completions']:
            cert_name = cert['name']
            try:
                expire_date = dt.datetime.strptime(cert['expires'], '%m/%d/%Y').date()
            except:
                continue
                
            if cert_name not in non_dupes:
                non_dupes[cert_name] = expire_date
            else:    
                old_date = non_dupes[cert_name]
                if old_date < expire_date:
                    non_dupes[cert_name] = expire_date
            
            
        for cert in non_dupes:
            expire_date = non_dupes[cert]
            if expire_date < EXPIRED_TRAININGS_DATE:
                certs.append({'certificate': cert, 'status': 'expired'})
            elif expire_date >= EXPIRED_TRAININGS_DATE and expire_date < SOON_TO_EXPIRE_DATE:
                certs.append({'certificate': cert, 'status': 'expires soon'})
        if certs:
            expired_certs[person['name']] = certs

    with open(f'expired_certs_{EXPIRED_TRAININGS_DATE}.json', 'w') as file3:
        json.dump(expired_certs, file3, indent=2, sort_keys=True)

if __name__ == '__main__':
    

        
    parser = argparse.ArgumentParser(prog='app', description='outputs data from completed trainings json')
    parser.add_argument('-i','--input', type=str, default='trainings.txt')
    parser.add_argument('-y', '--year', type=int, default=FISCAL_YEAR)
    args = parser.parse_args()
    
    inpt = args.input
    with open(inpt, 'r') as file:
        data = json.load(file)
        
    certificate_counts(data)
    fiscal_year_certificates(data, args.year)
    expired_certificates(data)
    