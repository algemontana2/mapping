def parse_output_file(file_path):
    individual_data = []
    current_individual = {}

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('Individual:'):
                # If we've already collected data for an individual, add it to our list
                if current_individual:
                    individual_data.append(current_individual)
                # Start a new dictionary for the next individual
                current_individual = {'Individual': line}
            elif line.startswith('Birth:'):
                current_individual['Birth'] = line
            elif line.startswith('Death:'):
                current_individual['Death'] = line
            elif line.startswith('Residence:'):
                if 'Residences' in current_individual:
                    current_individual['Residences'].append(line)
                else:
                    current_individual['Residences'] = [line]

    # Don't forget to add the last individual's data
    if current_individual:
        individual_data.append(current_individual)

    return individual_data

def print_individual_data(individual_data):
    for individual in individual_data:
        print(individual)

def main():
    file_path = 'output.txt'
    individual_data = parse_output_file(file_path)
    print_individual_data(individual_data)

if __name__ == '__main__':
    main()
