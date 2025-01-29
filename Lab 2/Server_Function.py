import sys, os
import socket

filename = "empolyee.txt"


def process_message(message, sc):
    
    try:
        # Assume the message is a colon-separated string, e.g., "1:John:Doe:HR"
        message_parts = message.split(":")
        command = message_parts[0]  # First character determines the action

        if command == "1":
            print("Add new employee action detected.\n")
            addNew(message_parts, sc)
        elif command == "2":
            print("Search employee action detected.\n")
            findEmp(message_parts, sc)
        elif command == "3":
            print("Remove employee action detected.\n")
            removeEmp(message_parts, sc)
        elif command == "4":
            print("Display employees action detected.\n")
            printDB(sc)
        elif command == "5":
            print("Exiting Program")
            sys.exit()    
        else:
            print(f"Unknown command: {command}")
            sc.sendall(b"Error: Unknown command\0")

    except Exception as e:
        print(f"Error processing message: {e}")
        sc.sendall(b"Error processing the message\0")


def addNew(data, sc):
    try:
    
        empNum = data[1]
        firstName = data[2]
        lastName = data[3]
        dep = data[4]

        if not (empNum.isdigit() and int(empNum) > 0 and int(empNum) <= 999999):
                sc.sendall(b"Invalid input: Please enter a number.\0")
                return 

        if not (firstName.isalpha()):
            sc.sendall(b"Invalid input: Please only use letters.\0")
            return
        
        if not (lastName.isalpha()):
            sc.sendall(b"Invalid input: Please only use letters.\0")
            return

        if not (dep.isalpha()):
            sc.sendall(b"Invalid input: Please only use letters.\0")
            return

        # Check if the file exists and if the employee number is unique
        empNum_exists = False
        try:
            if os.path.exists(filename):  # Only check if the file exists
                with open(filename, 'r') as db:
                    for line in db:
                        record_empNum = line.split(":")[0]  # Extract empNum from each line
                        if record_empNum == empNum:
                            empNum_exists = True
                            break
        except FileNotFoundError:
            sc.sendall(f"File '{filename}' not found. A new file will be created.\0".encode())
            empNum_exists = False  # Treat as if no duplicates exist because the file doesn't exist

        # If the employee number is not unique, display an error message
        if empNum_exists:
            sc.sendall(f"Employee number {empNum} already exists. Cannot add duplicate.\0".encode())
            return

        # Add new employee record to the file
        with open(filename, 'a') as db:  
            db.write(f"{empNum}:{firstName}:{lastName}:{dep}\n")
            print(f"New employee added: {empNum} - {firstName} {lastName} ({dep})")
            sc.sendall((f"New employee added: {empNum} - {firstName} {lastName} ({dep})\0".encode()))
    except FileNotFoundError as e:
        print(f"Error: {e}. The file could not be found.")
        sc.sendall(f"Error: {e}. The file could not be found.\0".encode())
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sc.sendall(f"Unexpected Error: {e}".encode())



def findEmp(data, sc): 
    try:
        empNum = data[1]
        if not(empNum.isdigit() and 0 < int(empNum) <= 999999):
            sc.sendall(b"Invalid input: Please enter a number.\0")
            return

        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        # Search for the employee in the file
        with open(filename, 'r') as db:
            for line in db:
                record_empNum = line.split(":")[0]  # Extract empNum from the line
                if record_empNum == empNum:
                    print(f"Employee found: {line.strip()}")  # Print the employee details
                    sc.sendall(f"Employee found: {line.strip()}\0".encode())
                    return  # Exit the function after finding the employee

        # If no match is found
        print("Employee not found.")
        sc.sendall(b"Employee not found.\0")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Unexpected Error: {e}")   


def removeEmp(data, sc):
    try:

        empNum = data[1]
        
        
            
        if not(empNum.isdigit() and 0 < int(empNum) <= 999999):
            sc.sendall(b"Invalid input: Please enter a number.\0")
            return
        
        # Check if the file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        # Read all lines from the file
        with open(filename, 'r') as db:
            lines = db.readlines()

        # Clean lines and filter out the one with the specified employee number
        lines = [line.strip() for line in lines]
        updated_lines = [line for line in lines if not line.startswith(empNum)]

        # Check if the employee number was found and removed
        if len(updated_lines) == len(lines):
            print(f"Employee number {empNum} not found.")
            sc.sendall(f"Employee number {empNum} not found.\0".encode())
            return
        
        # Write the updated lines back to the file
        with open(filename, 'w') as db:
            db.write('\n'.join(updated_lines) + '\n')

        
        print("The employee has been successfully removed.")
        sc.sendall(b"The employee has been successfully removed.\0")
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"Unexpected Error: {e}"             
    

def printDB(sc):

    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        
        with open(filename, 'r') as db:
            lines = db.readlines()
            if not any(line.strip() for line in lines):  # Check if any non-empty lines exist
                print(f"The file '{filename}' is empty.")
                sc.sendall(f"The file '{filename}' is empty.\0".encode())
                return
            
            # Print each line
            full_message = "\n".join(line.strip() for line in lines) + "\0"
            print(f"Sending to client:\n{full_message}")
            sc.sendall(full_message.encode())


    except FileNotFoundError as e:
        print(str(e))
        sc.sendall(b'File not found.\0')       
    except Exception as e:
        return f"Unexpected Error: {e}"
    