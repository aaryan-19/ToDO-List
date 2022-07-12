from logging import captureWarnings
from os import name
import mysql.connector
from mysql.connector import Error
from random import randint
from datetime import date

# First class for users
class User():

    # function for signing in
    def sign_in(self):
        """Sign-in"""
        email_id = input("Email :- ")
        password = input("Password :- ")
        
        # verify details from the database
        res = runQuery("Select user_id,email_id,password,name from user where email_id = '" + str(email_id) + "' and password = '" + str(password) + "';")
        # print(res)
        
        object_to_do = To_do_tasks()
        for i in res:
            if email_id == i[1] and password == i[2]:
                print("Welcome :- ",i[3])
                s = input()
                object_to_do.menu(i[0])

        else:
            print("Wrong Credentials..")
        

    # function for signing up
    def sign_up(self):
        """Sign-Up"""
        username = input("Enter new username : ")
        password = input("Enter new password : ")
        email_id = input("Enter your email id : ")
        res = runQuery("Select email_id from user;")
        flag = 1
        
        # loop to check if the email_id already exist or not
        for id in res:
            if ( email_id == id):
                print("Account already exist!!")
                flag = 0
                break

        if (flag != 0):
            
            # first generate distinct user id
            user_id = 0
            res = None

            while res != []:
                user_id = randint(0, 2147483646)
                res = runQuery("SELECT user_id FROM user WHERE user_id = "+str(user_id))
            
            res = runQuery("INSERT INTO user (user_id, name, password, email_id) VALUES(" + str(user_id) +",'" + str(username) + "','" + str(password) + "','" + str(email_id) + "');")
            
            if res == 'No result set to fetch from':
                print("User successfully added..")

            else:
                print(res)

# class for to_do _tasks
class To_do_tasks():

    # function for menu
    def menu(self,user_id):
        """Menu Function"""
        continue_choice = "Yes"

        while(continue_choice.lower() == "yes"):

            print("\nMenu :- ")
            print("1. Enter task\n2. Check Status of a task\n3. Enter Completion Date for a task\n4. Input Category for a task")
            print("5. Delete a task\n6. View A Task\n7. Update A Task\n8. Exit")
            choice = int(input("Enter your choice :- "))

            # input task
            if(choice == 1):
                self.input_task(user_id)
                
            # check status
            elif(choice == 2):
                self.check_status(user_id)

            # input completion date for a task
            elif(choice == 3):
                self.input_completion_date(user_id)

            # input category for a task
            elif(choice == 4):
                self.input_category(user_id)

            # delete a task
            elif(choice == 5):
                self.delete_task(user_id)

            # view a task
            elif(choice == 6):
                self.view_task(user_id)

            # update a task
            elif(choice == 7):
                self.update_task(user_id)

            # exit
            elif(choice == 8):
                print("Thank You..!!")
                exit()

            else:
                print("Wrong Choice Entered.")


        else:
            print("Thank You..!!")
            exit()


    # function to enter task details
    def input_task(self,user_id):
        """"Input Task"""
        
        print("Input Neccessary Details")
        task_name = input("Task :- ")
        # category_choice = input("Do you want to add category Yes/No :- ")

        # optional entries
        category = input("Category(optional) :- ")
        date_of_completion = input("Target Date for Completion(Optional) yyyy-mm-dd :- ")

        task_id = 0
        res = None

        while res != []:
            task_id = randint(0, 2147483646)
            res = runQuery("SELECT task_id FROM to_do_tasks WHERE task_id = "+str(task_id))

        # running insert query on database
        if (category == '' and date_of_completion == ''):
            
            res = runQuery("INSERT INTO to_do_tasks (user_id, task_id, task_name,date_of_entry) VALUES(" + str(user_id) +",'" + str(task_id) + "','" + str(task_name) + "','" + str(date.today()) + "');")

        elif (category == '' and date_of_completion != ''):

            res = runQuery("INSERT INTO to_do_tasks (user_id, task_id, task_name,date_of_entry,date_of_completion) VALUES(" + str(user_id) +",'" + str(task_id) + "','" + str(task_name) + "','" + str(date.today()) + "','" + str(date_of_completion) + "');")

        elif (category != ''  and date_of_completion == ''):

            res = runQuery("INSERT INTO to_do_tasks (user_id, task_id, task_name,date_of_entry,category) VALUES(" + str(user_id) +",'" + str(task_id) + "','" + str(task_name) + "','" + str(date.today()) + "','" + str(category) + "');")

        elif(category != '' and date_of_completion != ''):

            res = runQuery("INSERT INTO to_do_tasks (user_id, task_id, task_name,date_of_entry,date_of_completion,category) VALUES(" + str(user_id) +",'" + str(task_id) + "','" + str(task_name) + "','" + str(date.today()) + "','" + str(date_of_completion) + "','" + str(category) + "');") 

        if res == 'No result set to fetch from':
            print("User successfully added..")

        else:
            print(res)


    # function to check status of tasks for a user
    def check_status(self,user_id):
        """"Checking status"""

        res = runQuery("Select * from to_do_tasks where user_id = '" + str(user_id) + "';")

        # display all information
        for i in res:
            print("Task id : ",i[0])
            print("Task Details : ",i[2])
            print("Status : ",i[3])
            print()
            
        s = input()
    

    # function to enter completion date
    def input_completion_date(self,user_id):
        """Completion Date"""

        self.check_status(user_id)

        task_id = input("Enter the task id you want to input  completion date for :- ")
        date_of_completion = input("Target Date yyyy-mm-dd :- ")

        res = runQuery("Update to_do_tasks set date_of_completion = '" + str(date_of_completion) + "' where task_id = '" + str(task_id) + "';")

        if res == 'No result set to fetch from':
            print("Date successfully added..") 

        else:
            print(res)
        s = input()


    # function to input category for a task
    def input_category(self,user_id):
        """Input category"""

        self.check_status(user_id)

        task_id = input("Enter the task id you want to input category for :- ")
        category = input("Category :- ")

        res = runQuery("Update to_do_tasks set category = '" + str(category) + "' where task_id = '" + str(task_id) + "';")

        if res == 'No result set to fetch from':
            print("Category successfully added..")

        else:
            print(res)
        s = input()


    # function to delete a task
    def delete_task(self,user_id):
        """Delete"""

        self.check_status(user_id)
        task_id = input("Enter the task id you want to delete :- ")

        res = runQuery("delete from to_do_tasks where task_id = '" + str(task_id) + "';")

        if res == 'No result set to fetch from':
            print("Task successfully deleted..")

        else:
            print(res)
        s = input()


    # function to view task
    def view_task(self,user_id):
        """View Task"""
        print("\nDifferent View Option :- ")
        print("\n1. Category Wise \n2. Entry Date Wise\n3. Completion Wise")
        choice = int(input("Your choice :- "))

        # category wise
        if(choice == 1):
            self.view_acc_cateogry(user_id)
            
        # Entry Date wise
        elif(choice == 2):
            self.view_acc_entry_date(user_id)

        # completion wise
        elif(choice == 3):
            self.view_acc_completion(user_id)

        else:
            print("Invalid Choice Selected")

    
    # function to view category wise
    def view_acc_cateogry(self,user_id):
        """View Category Wise"""
        res = runQuery("Select task_id,task_name,category from to_do_tasks where user_id = '" + str(user_id) + "'order by category;")
        # print(res)
        for i in res:
            print("Task id :- ",i[0])
            print("Task Name :- ",i[1])
            print("Category :- ",i[2])
            print()

        s = input()


    # function to view date wise
    def view_acc_entry_date(self,user_id):
        """View date Wise"""
        res = runQuery("Select task_id,task_name,date_of_entry from to_do_tasks where user_id = '" + str(user_id) + "' order by date_of_entry;")
        # print(res)
        for i in res:
            print("Task id :- ",i[0])
            print("Task Name :- ",i[1])
            print("Date of Entry :- ",i[2])
            print()

        else:
            print("No tasks available")

        s = input()

    # function to view completion wise
    def view_acc_completion(self,user_id):
        """View Completion wise"""
        res = runQuery("Select task_id,task_name,status from to_do_tasks where user_id = '" + str(user_id) + "' order by status;")
        # print(res)
        for i in res:
            print("Task id :- ",i[0])
            print("Task Name :- ",i[1])
            print("Stauts :- ",i[2])
            print()

        else:
            print("No tasks available")

        s = input()


    # function to update a task
    def update_task(self,user_id):
        """Update task"""
        print("Different Update Option :- ")
        print("1. Completion Time\n2. Category\n3. Status")
        choice = int(input("Your Choice :- "))

        # completion time
        if(choice == 1):
            self.upate_completion_time(user_id)

        # category
        elif(choice == 2):
            self.update_category(user_id)

        # status
        elif(choice == 3):
            self.update_status(user_id)

        else:
            print("Wrong Choice Entered.")

    
    # function to update completion time
    def upate_completion_time(self,user_id):
        """Update Completion Time"""
        self.check_status(user_id)

        task_id = input("Enter the task id you want to update completion date for :- ")
        new_completion_date = input("Target Date yyyy-mm-dd :- ")

        res = runQuery("Update to_do_tasks set date_of_completion = '" + str(new_completion_date) + "' where task_id = '" + str(task_id) + "';")

        if res == 'No result set to fetch from':
            print("Date successfully Updated..")
            
        else:
            print(res)
        s = input()


    # update category
    def update_category(self,user_id):
        """Update Category"""
        self.check_status(user_id)

        task_id = input("Enter the task id you want to update category for :- ")
        Category = input("Category :- ")

        res = runQuery("Update to_do_tasks set category = '" + str(Category) + "' where task_id = '" + str(task_id) + "';")

        if res == 'No result set to fetch from':
            print("Cateogry successfully Updated..")
            
        else:
            print(res)
        s = input()


    # function to update status
    def update_status(self,user_id):
        """Update Status"""
        self.check_status(user_id)

        task_id = input("Enter the task id you want to update status for :- ")
        status = input("Status :- ")

        res = runQuery("Update to_do_tasks set status = '" + str(status) + "' where task_id = '" + str(task_id) + "';")

        if res == 'No result set to fetch from':
            print("Status successfully Updated..")
            
        else:
            print(res)
        s = input()

    
# query run fucntion
def runQuery(query):
	try:
		db = mysql.connector.connect(
			host='localhost',
			database='to_do_list',
			user='theatre_user',
			password='password')

		if db.is_connected():
			cursor = db.cursor(buffered = True)
			cursor.execute(query)
			db.commit()
			return cursor.fetchall()

	except Error as e:
		#Some error occured
		return e.args[1] 

	finally:
		db.close()

    #Couldn't connect to MySQL
	return None

# main function
def main():
    # menu
    object_user = User()

    print("1. Sign-in\n2. Sign-Up\n3. Exit")
    choice = int(input("Enter your choice : "))

    if (choice == 1):
        object_user.sign_in()

    elif (choice == 2):
        object_user.sign_up()

    elif (choice == 3):
        exit()

    else:
        print("Wroing choice Entered\nBye..!!")
        exit()

if __name__=="__main__":
    main()
