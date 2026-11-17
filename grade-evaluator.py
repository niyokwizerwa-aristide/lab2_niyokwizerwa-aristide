import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                assignments.append({
                    'assignment': row['assignment'].strip(),
                    'group': row['group'].strip(),
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except ValueError:
        print("Error: Invalid numeric value found in 'score' or 'weight' columns.")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing expected column {e} in the CSV file.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Validates grades and weights, calculates final grade and GPA,
    determines pass/fail status, and identifies resubmission options.
    """
    print("\n--- Processing Grades ---")
    
    if not data:
        print("Error: The CSV file contains no assignment records.")
        sys.exit(1)

    total_weight = 0.0
    formative_weight = 0.0
    summative_weight = 0.0
    
    formative_weighted_score = 0.0
    summative_weighted_score = 0.0
    failed_formative = []

    for item in data:
        name = item['assignment']
        group = item['group'].lower()
        score = item['score']
        weight = item['weight']

        # a) Check if all scores are percentage based (0-100)
        if score < 0 or score > 100:
            print(f"Validation Error: Score for '{name}' ({score}) must be between 0 and 100.")
            sys.exit(1)

        if weight < 0:
            print(f"Validation Error: Weight for '{name}' ({weight}) cannot be negative.")
            sys.exit(1)

        total_weight += weight
        weighted_points = (score / 100.0) * weight

        if group == 'formative':
            formative_weight += weight
            formative_weighted_score += weighted_points
            if score < 50:
                failed_formative.append(item)
        elif group == 'summative':
            summative_weight += weight
            summative_weighted_score += weighted_points
        else:
            print(f"Validation Error: Unknown group '{item['group']}' for '{name}'. Expected 'Formative' or 'Summative'.")
            sys.exit(1)

    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    if round(total_weight, 2) != 100.0:
        print(f"Validation Error: Total weight is {total_weight}, but it must equal 100.")
        sys.exit(1)
    if round(summative_weight, 2) != 40.0:
        print(f"Validation Error: Summative weight is {summative_weight}, but it must equal 40.")
        sys.exit(1)
    if round(formative_weight, 2) != 60.0:
        print(f"Validation Error: Formative weight is {formative_weight}, but it must equal 60.")
        sys.exit(1)

    # c) Calculate the Final Grade and GPA
    total_grade = formative_weighted_score + summative_weighted_score
    gpa = (total_grade / 100.0) * 5.0

    # Calculate category percentages
    formative_pct = (formative_weighted_score / formative_weight) * 100.0
    summative_pct = (summative_weighted_score / summative_weight) * 100.0

    # d) Determine Pass/Fail status (>= 50% in BOTH categories)
    if formative_pct >= 50.0 and summative_pct >= 50.0:
        status = "PASSED"
    else:
        status = "FAILED"

    # e) Check for failed formative assignments (< 50%) with highest weight
    resubmission_options = []
    if failed_formative:
        max_weight = max(item['weight'] for item in failed_formative)
        resubmission_options = [item for item in failed_formative if item['weight'] == max_weight]

    # f) Print the final decision (PASSED / FAILED) and resubmission options
    print("\n================ ALU TRANSCRIPT ================")
    print(f"Formative Category Score : {formative_weighted_score:.2f} / 60.00 ({formative_pct:.2f}%)")
    print(f"Summative Category Score : {summative_weighted_score:.2f} / 40.00 ({summative_pct:.2f}%)")
    print(f"Total Final Grade        : {total_grade:.2f} / 100.00")
    print(f"Final GPA (5.0 Scale)    : {gpa:.2f}")
    print(f"Final Status             : {status}")
    print("------------------------------------------------")
    
    if resubmission_options:
        print("Eligible for Resubmission (Highest Weight Failed Formative):")
        for item in resubmission_options:
            print(f" - {item['assignment']} (Score: {item['score']}%, Weight: {item['weight']}%)")
    else:
        print("Eligible for Resubmission: None")
    print("================================================\n")

if __name__ == "__main__":
    course_data = load_csv_data()
    evaluate_grades(course_data)
