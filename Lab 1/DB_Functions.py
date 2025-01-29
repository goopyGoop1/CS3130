import os.path
import sys

def sortFile(filename):
    try:
        # Check if the file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        
        # Read all lines from the file
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        # Filter out empty or invalid lines
        valid_lines = [line for line in lines if line.strip() and ':' in line]
        
        # Sort lines based on the number at the beginning
        sorted_lines = sorted(valid_lines, key=lambda line: int(line.split(':')[0].strip()))
        
        # Write the sorted lines back to the file
        with open(filename, 'w') as file:
            for line in sorted_lines:
                file.write(line.strip() + '\n')  # Ensure proper formatting when writing
        
        
    except FileNotFoundError as e:
        print(str(e))
    except ValueError:
        print("One or more lines do not start with a valid number or have invalid format.")
    except Exception as e:
        print(f"Unexpected Error: {e}")

def run(filename):
    valid_input = False
    print("--\n")

    print("Employees:\n\n")


    print("Select one of the following:\n\n")
    print("1) Add a new employee\n")
    print("2) Search for an employee\n")
    print("3) Remove an employee\n")
    print("4) Display employees\n")
    print("5) Exit\n\n")


    while not valid_input:
        option = input("Enter Your Option: ").strip()
        print()
        if option.isdigit() and int(option) in [1, 2, 3, 4, 5]:
            valid_input = True
        else: print("Invalid input. Please Selelct 1-5") 

    option = int(option)
    if option == 1:
        addNew(filename)
        sortFile(filename)
    elif option == 2:
        findEmp(filename)
    elif option == 3:
        removeEmp(filename)
        sortFile(filename)
    elif option == 4:
        printDB(filename)
    else:
        exitPrg()

def addNew(filename):
    try:
        valid_input = False

        while not valid_input:
            empNum = input("Enter the new employee number: ").strip()
            if empNum.isdigit() and int(empNum) > 0 and int(empNum) <= 999999:
                empNum = int(empNum)
                valid_input = True
            else:
                print("Invalid input: Please enter a number.")

        valid_input = False

        while not valid_input:
            firstName = input("Enter the first name: ").strip()
            if firstName.isalpha():
                valid_input = True
            else:
                print("Invalid input: Please only use letters.")

        valid_input = False

        while not valid_input:
            lastName = input("Enter the last name: ").strip()
            if lastName.isalpha():
                valid_input = True
            else:
                print("Invalid input: Please only use letters.")

        valid_input = False

        while not valid_input:
            dep = input("Enter the department: ").strip()
            if dep.isalpha():
                valid_input = True
            else:
                print("Invalid input: Please only use letters.")

        # Check if the file exists and if the employee number is unique
        empNum_exists = False
        try:
            if os.path.exists(filename):  # Only check if the file exists
                with open(filename, 'r') as db:
                    for line in db:
                        record_empNum = int(line.split(":")[0])  # Extract empNum from each line
                        if record_empNum == empNum:
                            empNum_exists = True
                            break
        except FileNotFoundError:
            print(f"File '{filename}' not found. A new file will be created.")
            empNum_exists = False  # Treat as if no duplicates exist because the file doesn't exist

        # If the employee number is not unique, display an error message
        if empNum_exists:
            print(f"Employee number {empNum} already exists. Cannot add duplicate.")
            return

        # Add new employee record to the file
        with open(filename, 'a') as db:  
            db.write(f"{empNum}:{firstName}:{lastName}:{dep}\n")
            print(f"New employee added: {empNum} - {firstName} {lastName} ({dep})")

    except FileNotFoundError as e:
        print(f"Error: {e}. The file could not be found.")
    except Exception as e:
        print(f"Unexpected Error: {e}")



def findEmp(filename): 
    try:
        valid_input = False
        
        while not valid_input:
            empNum = input("Enter the employee number: ").strip()
            if empNum.isdigit() and 0 < int(empNum) <= 999999:
                empNum = int(empNum)
                valid_input = True
            else:
                print("Invalid input: Please enter a valid number between 1 and 999999.")

        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        # Search for the employee in the file
        with open(filename, 'r') as db:
            for line in db:
                record_empNum = int(line.split(":")[0])  # Extract empNum from the line
                if record_empNum == empNum:
                    print(f"Employee found: {line.strip()}")  # Print the employee details
                    return  # Exit the function after finding the employee

        # If no match is found
        print("Employee not found.")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Unexpected Error: {e}")
    


def removeEmp(filename):
    try:

        valid_input = False
        
        while not valid_input:
            empNum = input("Enter the employee number: ").strip()
            if empNum.isdigit() and int(empNum) > 0 and int(empNum) <= 999999:
                empNum = int(empNum)
                valid_input = True
            else:
                print("Invalid input: Please enter a number.")
        
        # Check if the file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        # Read all lines from the file
        with open(filename, 'r') as db:
            lines = db.readlines()

        # Clean lines and filter out the one with the specified employee number
        lines = [line.strip() for line in lines]
        updated_lines = [line for line in lines if not line.startswith(str(empNum))]

        # Check if the employee number was found and removed
        if len(updated_lines) == len(lines):
            return f"Employee number {empNum} not found."

        # Write the updated lines back to the file
        with open(filename, 'w') as db:
            db.write('\n'.join(updated_lines) + '\n')

        
        print("The employee has been successfully removed.")

    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Unexpected Error: {e}"
    


def printDB(filename):

    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        
        with open(filename, 'r') as db:
            lines = db.readlines()
            if not any(line.strip() for line in lines):  # Check if any non-empty lines exist
                print(f"The file '{filename}' is empty.")
                return
            
            # Print each line
            for line in lines:
                print(line.strip())


    except FileNotFoundError as e:
        print(str(e))       
    except Exception as e:
        return f"Unexpected Error: {e}"
    
    


def exitPrg():
    print ("Are you sure you want to exit the program?  (Y or N)\n")
    
    while True:
        
        anwser = input().strip()
        if anwser in ['y', 'Y']:
            print("Exiting program")
            sys.exit(0)

        elif anwser in ['n', 'N']:
            print("Returning to program")
            break    

        else:
            print("Invalid entry. Please enter Y or N.")   