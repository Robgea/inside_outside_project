import csv
import os


results_csv = open('referrer_results.csv', 'w', newline = '')
results_write = csv.writer(results_csv)
results_write.writerow(['crm number', 'First Name', 'Last Name', 'organization', 'inside org referral numbers', 'outside org referral numbers', 'name and orgs of people referred....'])

error_csv = open('error_referrals.csv', 'w', newline = '')
error_write = csv.writer(error_csv)


class Refferal():
    def __init__(self, org_name):
        self.inside_count = 0
        self.outside_count = 0
        self.errors = 0
        self.tracking_set = set()
        self.org_name = org_name
        


class Info():
    def __init__(self, first, last, org):
        self.first = first
        self.last = last
        self.org = org



def master_dict_maker():
    master_raw = open('master.csv')
    master_reader = csv.reader(master_raw)
    master_list = list(master_reader)
    output_dict = {}
    for row in master_list:
        if len(row) > 2:
            obj = Info(row[2], row[3], row[5])
            output_dict.update({row[1] : obj})
    return output_dict

def name_dict_maker():
    master_raw = open('master.csv')
    master_reader = csv.reader(master_raw)
    master_list = list(master_reader)
    name_dict = {f'{row[2]} {row[3]}' : row[1] for row in master_list if (len(row) > 2)}
    return name_dict

def referral_tracker(master_dict, name_dict):
    referral_dict = {}

    for counting_file in os.listdir('.'):
        if not counting_file.endswith('.csv'):
            print(f'Skipping {counting_file}')
            continue
        elif counting_file == 'referrer_results.csv':
            continue
        elif counting_file == 'master.csv':
            continue
        elif counting_file == 'error_referrals.csv':
            continue
        else:
            contact_num = 0
            org_num = 0
            first_name_num = 0
            last_name_num = 0
            no_num = 0
            csv_file_obj = open(counting_file, encoding="utf8")
            file_reader = csv.reader(csv_file_obj)
            file_list = list(file_reader)
            row_count = 0
            print(f'Now doing {counting_file}')
            for row in file_list:
                if (row_count < 2):
                    row_count += 1
                    continue
                elif (row_count == 2):
                    cell_count = 0
                    for cell in row:
                        if cell.startswith('Is this you?'):
                            no_num = cell_count
                        elif cell.startswith('First N'):
                            first_name_num = cell_count
                        elif cell.startswith('Last N'):
                            last_name_num = cell_count
                        elif cell.startswith('Organizat'):
                            org_num = cell_count
                        elif cell.startswith('ContactID'):
                            contact_num = cell_count
                        
                        cell_count += 1

                    if (no_num == 0) or (org_num == 0) or (first_name_num == 0) or (last_name_num == 0) or (contact_num == 0):
                        print(f'Error with {counting_file} header. \n  {no_num}, {org_num}, {first_name_num} {last_name_num}, {contact_num}. {cell_count}')
                    row_count += 1

                else: 
                    #check here against referrer org
                    if row[no_num] == 'No':
                        contact_id = row[contact_num]
                        name = f'{row[first_name_num]} {row[last_name_num]}'
                        # Check to see if the name is in the name dictionary. If it isn't, kick the referral to the error dict.

                        if name not in name_dict:
                            error_write.writerow([counting_file[0:-4], contact_id, name])

                        elif contact_id  in referral_dict:
                            try:
                                referral_dict[contact_id].tracking_set.add(name_dict[name])

                            except Exception as e:
                                print(f'Error in {counting_file} with {contact_id}\n {e}')
                                continue

                        elif contact_id not in referral_dict:
                            try:
                                obj = Refferal(master_dict[contact_id].org, )
                                referral_dict.update({contact_id : obj})
                                referral_dict[contact_id].tracking_set.add(name_dict[name])

                            except Exception as e:
                                print(f'Error in {counting_file} with {contact_id}\n {e}')

                                continue                                

    for entry in referral_dict:
        #go through each entry, update the inside outside count, then...
        for num in referral_dict[entry].tracking_set:
            # if org == entry org then inside count +1 else outside +1
            if master_dict[num].org == referral_dict[entry].org_name:
                referral_dict[entry].inside_count += 1
            elif master_dict[num].org != referral_dict[entry].org_name:
                referral_dict[entry].outside_count += 1




        output_row = [entry, master_dict[entry].first, master_dict[entry].last, master_dict[entry].org, referral_dict[entry].inside_count, referral_dict[entry].outside_count,]
        for pers in referral_dict[entry].tracking_set:
            output_row.append(f'{master_dict[pers].first} {master_dict[pers].last} at {master_dict[pers].org}')

        results_write.writerow(output_row)







def main():
    master_return = master_dict_maker()
    name_return = name_dict_maker()
    referral_tracker(master_return, name_return)

if __name__ == '__main__':
    main()




#make dictionary of names and CRIDs for testing sheet


# go through each referral, see if the CRM is in the 