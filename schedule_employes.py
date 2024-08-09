import pandas as pd

# Output the file of the reports
# Function to read the file in python 
def load_data_file(filename):
    df= pd.read_csv(filename,index_col=0)
    return df

# rules for validation

def validate_one_shift_per_day(data):
    violations = []
    groups = data.groupby(['EmployeeID', 'Day'])
    for name, group in groups:
        if len(group) > 1:
            violations.append(f"EmployeeID: {name[0]}, worked more than one shift on {name[1]}.")
    return violations

def validate_max_five_days_per_week(data):
    violations = []
    groups = data.groupby(['EmployeeID'])
    for name, group in groups:
        if group['Day'].nunique() > 5:
            violations.append(f"EmployeeID: {name}, worked more than 5 days in the week.")
    return violations


def validate_consistent_names(data):
    violations = []
    groups = data.groupby(['EmployeeID'])
    for name, group in groups:
        if group['Name'].nunique() > 1:
            violations.append(f"EmployeeID: {name}, has inconsistent Name values.")
    return violations

def generate_report(violations, output_file):
    with open(output_file, 'w') as f:
        if not violations:
            f.write("No violations found.\n")
        else:
            for violation in violations:
                f.write(violation + "\n")

def validate_no_consecutive_night_shifts(data):
    violations = []
    
    night_shifts = data[data['Shift'] == 'Night']
    night_shifts = night_shifts.sort_values(by=['EmployeeID', 'Day'])
    
    night_shifts['PreviousDay'] = night_shifts.groupby('EmployeeID')['Day'].shift(1)
    
    consecutive_nights = night_shifts[
        (pd.to_datetime(night_shifts['Day'], format='%A') - pd.to_datetime(night_shifts['PreviousDay'], format='%A')).dt.days == 1
    ]
    
    for _, row in consecutive_nights.iterrows():
        violations.append(f"EmployeeID: {row['EmployeeID']}, worked the night shift on both {row['PreviousDay']} and {row['Day']}.")
    
    return violations

def main():
    file_path = 'schedules_large.csv'
    data = load_data_file(file_path)
    
    if data is not None:
        violations = []
        violations.extend(validate_one_shift_per_day(data))
        violations.extend(validate_max_five_days_per_week(data))
        violations.extend(validate_no_consecutive_night_shifts(data))
        violations.extend(validate_consistent_names(data))
        
        generate_report(violations, 'validation_report.txt')
        print("Validation report generated: validation_report.txt")

if __name__ == "__main__":
    main()