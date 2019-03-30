import csv
import os


results_csv = open('referrer_results.csv', 'w', newline = '')
results_write = csv.writer(results_csv)
results_write.writerow(['crm number', 'name', 'organization', 'inside org referral numbers', 'outside org referral numbers', 'name and orgs of people referred....'])

class Reffer():
    def __init__(self):
        self.inside_count = 0
        self.outside_count = 0
        self.tracking_dict = {}



def master_dict_maker():
    master_raw = open('master.csv')
    master_reader = csv.reader(master_raw)
    master_list = list(master_reader)
    output_dict = {row[1] : row[5] for row in master_list}
    return output_dict

def name_dict_maker():
    master_raw = open('master.csv')
    master_reader = csv.reader(master_raw)
    master_list = list(master_reader)
    name_dict = {row[1] : f'{row[2]} {row[3]}' for row in master_list}
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
                        org_name = row[org_num]
                        name = f'{row[first_name_num]} {row[last_name_num]}'
                        if contact_id  in referral_dict:
                            try:
                                if master_dict[contact_id] == org_name:
                                    referral_dict[contact_id].inside_count += 1
                                    referral_dict[contact_id].tracking_dict.update({name : org_name})
                                else:
                                    referral_dict[contact_id].outside_count += 1
                                    referral_dict[contact_id].tracking_dict.update({name : org_name})
                            except Exception as e:
                                print(f'Error in {counting_file} with {contact_id}\n {e}')
                                continue



                        elif contact_id not in referral_dict:
                            try:
                                obj = Reffer()
                                if master_dict[contact_id] == org_name:
                                    referral_dict.update({contact_id : obj})
                                    referral_dict[contact_id].inside_count += 1
                                    referral_dict[contact_id].tracking_dict.update({name : org_name})
                                else:
                                    referral_dict.update({contact_id : obj})
                                    referral_dict[contact_id].outside_count += 1
                                    referral_dict[contact_id].tracking_dict.update({name : org_name})
                            except Exception as e:
                                print(f'Error in {counting_file} with {contact_id}\n {e}')

                                continue                                

    for entry in referral_dict:
            
        output_row = [entry, name_dict[entry], master_dict[entry], referral_dict[entry].inside_count, referral_dict[entry].outside_count,]
        for key in referral_dict[entry].tracking_dict:
            output_row.append(f'{key} at {referral_dict[entry].tracking_dict[key]}')

        results_write.writerow(output_row)







def main():
    master_return = master_dict_maker()
    name_return = name_dict_maker()
    referral_tracker(master_return, name_return)

if __name__ == '__main__':
    main()




#make dictionary of names and CRIDs for testing sheet


# go through each referral, see if the CRM is in the 