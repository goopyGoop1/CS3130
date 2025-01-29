def addNew():
    try:
        valid_input = False
        employee_data = ['1']  # List to store employee data

        while not valid_input:
            empNum = input("Enter the new employee number: ").strip()
            if empNum.isdigit() and int(empNum) > 0 and int(empNum) <= 999999:
                employee_data.append(empNum)  # Add empNum to the list
                valid_input = True
            else:
                print("Invalid input: Please enter a number between 1 and 999999.")

        valid_input = False

        while not valid_input:
            firstName = input("Enter the first name: ").strip()
            if firstName.isalpha():
                employee_data.append(firstName)  # Add firstName to the list
                valid_input = True
            else:
                print("Invalid input: Please only use letters.")

        valid_input = False

        while not valid_input:
            lastName = input("Enter the last name: ").strip()
            if lastName.isalpha():
                employee_data.append(lastName)  # Add lastName to the list
                valid_input = True
            else:
                print("Invalid input: Please only use letters.")

        valid_input = False

        while not valid_input:
            dep = input("Enter the department: ").strip()
            if dep.isalpha():
                employee_data.append(dep)  # Add department to the list
                valid_input = True
            else:
                print("Invalid input: Please only use letters.")

        # Combine the list into a single string with colon-separated values
        employee_record = ":".join(employee_data)

        # Return the list or record if needed elsewhere
        
        return employee_record

    except Exception as e:
        print(f"Unexpected Error: {e}")



def findEmp(): 
    try:
        valid_input = False
        
        while not valid_input:
            empNum = input("Enter the employee number: ").strip()
            if empNum.isdigit() and 0 < int(empNum) <= 999999:
                valid_input = True
            else:
                print("Invalid input: Please enter a valid number between 1 and 999999.")

        return  str('2:' + empNum)

    except Exception as e:
        print(f"Unexpected Error: {e}")



def removeEmp():
    try:

        valid_input = False
        
        while not valid_input:
            empNum = input("Enter the employee number: ").strip()
            if empNum.isdigit() and int(empNum) > 0 and int(empNum) <= 999999:
                valid_input = True
            else:
                print("Invalid input: Please enter a number.")
        
        return("3:" + empNum)

    except Exception as e:
        return f"Unexpected Error: {e}"
    

def printDB():

    try:

        return "4:"

    except Exception as e:
        return f"Unexpected Error: {e}"



def run():
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

    return option