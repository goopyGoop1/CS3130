# CS3130 Lab 1 Chad Norris-White 
import DB_Functions

def main():
    filename = "EmpDB.txt"
    

    run_prg = False

    while not run_prg:
        DB_Functions.run(filename)


# Run the main function
if __name__ == "__main__":
    main()
