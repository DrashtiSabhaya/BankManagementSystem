import mysql.connector;
import datetime;

mydb=mysql.connector.connect(host="localhost",user="root",passwd="",database="banksystem");
mycursor = mydb.cursor();
            
class Bank:
      rois=0;
      roic=0;
      mycursor.execute("Select * from intrest order by date desc limit 1");
      for i in mycursor:
            rois=i[1];
            roic=i[2];
            
      def __init__(self):
            self.acno=0;
            self.acnm='';
            self.actype=0;
            self.balance=0;
            self.mbno=0;
            self.adrs=0;

      @classmethod
      def setROIS(cls):
            cls.rois=float(input("Enter Rate of Interest for Saving Accounts = "));
            str="update intrest set rois='%f' where id=1";
            args=(cls.rois);
            try:
                  mycursor.execute(str % args);
                  mydb.commit();
            except:
                  mydb.rollback();
                  print("\nError : intrest is not update");

      @classmethod
      def setROIC(cls):
            cls.roic=float(input("Enter Rate of Interest for Current Accounts = "));
            str="update intrest set roic='%f' where id=1";
            args=(cls.roic);
            try:
                  mycursor.execute(str % args);
                  mydb.commit();
            except:
                  mydb.rollback();
                  print("\nError : intrest is not update");
            
      def createAccount(self):
            print("\n------ Enter Details for Create a New Account ------");
            self.acno=int(input("\nEnter Account No = "));
            self.acnm=input("Enter Account Holder Name = ");
            print("\n------- Type of Account --------");
            print("1. Saving Account\n2. Current Account");
            self.actype=int(input("Enter type of Account = "));
            while self.balance==0:
                  self.balance=float(input("Enter Account Balance = "));
                  if self.balance < 1000:
                        print("\nError : Account Blance Is not Sufficient");
                        print("It Must be greater than 1000 INR\n");
                        self.balance=0;
            self.mbno=int(input("Enter Mobile no = "));
            self.adrs=input("Enter address = ");

            str="Insert into accounts values('%d','%s','%d','%f','%d','%s')";
            args=(self.acno,self.acnm,self.actype,self.balance,self.mbno,self.adrs);
            str1="Insert into transactionlog(id,trans,mtrans) values ('%d','%d','%f')";
            args1=(self.acno,1,self.balance);
            try:
                  mycursor.execute(str % args);
                  mycursor.execute(str1 % args1);
                  mydb.commit();
                  print("\n******** Account Created ********\n");
            except:
                  mydb.rollback();
                  print("\nError : Account creation Failed.");
            
      def display(self):
            print("--------- Account Details ---------");
            print("Account No = ",self.acno);
            print("Account Holder Name = ",self.acnm);
            if self.actype==1 :
                  print("Account type = Saving");
            elif self.actype==2 :
                  print("Account type = Current");
            print("Account Balance = ",self.balance);
            print("Mobile no = ",self.mbno);
            print("Address = ",self.adrs);
                  
def newAccount():
      n=Bank();
      n.createAccount();
      n.display();

def setInterest():
      n=Bank();
      print("\n---- Current Rate of Interest ----");
      print("Savings Account = ",n.rois);
      print("Current Account = ",n.roic);
      print("\n1. Saving Account\n2. Current Account");
      i=int(input("Enter type of Account = "));
      if i==1:
            n.setROIS();
      elif i==2:
            n.setROIC();
      else:
            print("Error : Invalid Choice");

def deposite():
      acno=int(input("\nEnter Account number = "));
      x=0;
      mycursor.execute("select * from accounts where acno='%d'"%(acno));
      for i in mycursor:
            print(i);
            x=i[3];
      amt=float(input("\nEnter amount for deposite = "));
      x=x+amt;
      try:
            mycursor.execute("update accounts set balance='%f' where acno='%d'"%(x,acno));
            str1="Insert into transactionlog(id,trans,mtrans) values ('%d','%d','%f')";
            args1=(acno,1,amt);
            mycursor.execute(str1 % args1);
            mydb.commit();
            print("*** Account Updated Successfully. ***");
      except:
            mydb.rollback();
     
def withdraw():
      acno=int(input("\nEnter Account number = "));
      x=0;
      mycursor.execute("select * from accounts where acno='%d'"%(acno));
      for i in mycursor:
            print(i);
            x=i[3];
      amt=float(input("Enter amount for withdraw = "));
      x=x-amt;
      if x>100:
            try:
                  mycursor.execute("update accounts set balance='%f' where acno='%d'"%(x,acno));
                  str1="Insert into transactionlog(id,trans,mtrans) values ('%d','%d','%f')";
                  args1=(acno,0,amt);
                  mycursor.execute(str1 % args1);
                  mydb.commit();
                  print("*** Account Updated Successfully. ***");
            except:
                  mydb.rollback();
      else:
            print("Error : Account Balance is insufficient\nMoney Withdraw Denied.");

def balanceInq():
      acno=int(input("\nEnter Account number = "));
      mycursor.execute("select * from accounts where acno='%d'"%(acno));
      for i in mycursor:
            print("Account Name = ",i[1]);
            print("Current Balance = ",i[3]);

def displayAccounts():
      mycursor.execute("Select * from accounts");
      print("\n Acno\t\tAcName\t\tActype\t\tBalance\t\t Mobileno\t\tAddress");
      print("-"*100);
      for row in mycursor:
            print(" ",row[0],"\t",row[1],end="");
            if row[2]==1 :
                  print("\t\tSaving",end="");
            elif row[2]==2 :
                  print("\t\tCurrent",end="");
            print("\t\t",row[3],"\t",row[4],"\t\t",row[5],end="");
            print();

def closeAccount():
      acno=int(input("\nEnter Account number = "));
      mycursor.execute("select * from accounts where acno='%d'"%(acno));
      for i in mycursor:
            print(i);
      ch=input("Do you want to delete account(y/n) = ");
      if ch=='y' or ch=='Y':
            try:
                  mycursor.execute("delete from accounts where acno='%d'"%(acno));
                  mydb.commit();
                  print("**** Account Deleted ****");
            except:
                  mydb.rollback();

def updateAccount():
      acno=int(input("\nEnter Account number = "));
      mycursor.execute("select * from accounts where acno='%d'"%(acno));
      name=mbno=adrs=0;
      for i in mycursor:
            name=i[1];
            mbno=i[4];
            adrs=i[5];
            
      printModify();
      ch=getChoice();
      while ch!=4:
            if ch==1:
                  print("Name = ",name);
                  nnm=input("Enter name for Update = ");
                  try:
                        mycursor.execute("update accounts set acnm='%s' where acno='%d'"%(nnm,acno));
                        mydb.commit();
                        print("*** Name Updated Successfully. ***");
                  except:
                        mydb.rollback();
                  
            elif ch==2:
                  print("Address = ",adrs);
                  nadrs=input("Enter New Address = ");
                  try:
                        mycursor.execute("update accounts set adrs='%s' where acno='%d'"%(nadrs,acno));
                        mydb.commit();
                        print("*** Address Updated Successfully. ***");
                  except:
                        mydb.rollback();

            elif ch==3:
                  print("Mobile no = ",mbno);
                  nmbno=int(input("Enter new mobile no = "));
                  try:
                        mycursor.execute("update accounts set mbno='%d' where acno='%d'"%(nmbno,acno));
                        mydb.commit();
                        print("*** Mobile no Updated Successfully. ***");
                  except:
                        mydb.rollback();
                        
            else :
                  break;
            printModify();
            ch=getChoice();

def viewTransaction():
      print("\n----------Transaction History-----------");
      print("\t1. All time");
      print("\t2. All Credit Records");
      print("\t3. All Debit Records");
      print("\t4. User's Transaction ");
      print("\t0. Exit");
      print("----------------------------------------");   
      ch=getChoice();
      if ch==1:
            print("\nID\tTransaction\t  Amount\t\tDate Time");
            print("-"*65);
            mycursor.execute("Select * from transactionlog");
            for row in mycursor:
                  if row[1]==1:
                        tr='Credit'
                  else:
                        tr='Debit '
                  print(row[0],"\t",tr,"\t",row[2]," \t ",row[3]);
      elif ch==2:
            print("\nID\tTransaction\t  Amount\t\tDate Time");
            print("-"*65);
            mycursor.execute("Select * from transactionlog where trans=1");
            for row in mycursor:
                  tr='Credit'
                  print(row[0],"\t",tr,"\t",row[2]," \t ",row[3]);
      elif ch==3:
            print("\nID\tTransaction\t  Amount\t\tDate Time");
            print("-"*65);
            mycursor.execute("Select * from transactionlog where trans=0");
            for row in mycursor:
                  tr='Debit '
                  print(row[0],"\t",tr,"\t",row[2]," \t ",row[3]);
      elif ch==4:
            acno=int(input("\nEnter Account Number = "));
            print("\nID\tTransaction\t  Amount\t\tDate Time");
            print("-"*65);
            mycursor.execute("select * from transactionlog where id='%d'"%(acno));
            for row in mycursor:
                  if row[1]==1:
                        tr='Credit'
                  else:
                        tr='Debit '
                  print(row[0],"\t",tr,"\t",row[2]," \t ",row[3]);

def calcIntrest():
      acno=int(input("\nEnter Account number = "));
      n=float(input("Enter Time period(in years) = "));
      mycursor.execute("select * from accounts where acno='%d'"%(acno));
      actype=roi=balance=0;
      for i in mycursor:
            print("\nAccount Holder name = "+i[1]);
            actype=i[2];
            balance=i[3];
      if actype==1:
            print("Account Type = Saving");
            print("Rate of Intrest = ",Bank.rois);
            roi=(balance*Bank.rois*n)/100.0;
      else:
            print("Account Type = Current");
            print("Rate of Intrest = ",Bank.roic);
            roi=(balance*Bank.roic*n)/100.0;
            
      print("Account Balance = ",balance);
      print("Total Intrest Amount = ",roi);
      print("Total Amount = ",roi+balance);
      
      
def about(): 
      print("\t\t-----------------------------------");
      print("\t\t****** BANK MANAGEMENT SYSTEM ******");
      print("\t\t-----------------------------------\n\n");

def getDivision():
      print("\n----------------------------------------");
      print("\t\tLOGIN AS");
      print("----------------------------------------");
      print("\t1. BANK ADMIN");
      print("\t2. BANK MANAGER");
      print("\t3. EXIT");
      print("----------------------------------------");
      d=int(input("\tEnter Your Choice = "));
      return d;
       
def printMenu():
      print("\n----------------------------------------");
      print("\t\tMAIN MENU");
      print("----------------------------------------");
      print("\t1.  NEW ACCOUNT");
      print("\t2.  DEPOSIT AMOUNT");
      print("\t3.  WITHDRAW AMOUNT");
      print("\t4.  BALANCE ENQUIRY");
      print("\t5.  ALL ACCOUNT HOLDER LIST");
      print("\t6.  CLOSE AN ACCOUNT");
      print("\t7.  MODIFY AN ACCOUNT");
      print("\t8.  TRANSACTION HISTORY")
      print("\t9.  CALCULATE INTREST");
      print("\t10. EXIT")
      print("----------------------------------------");
     
def printMenuAdmin():
      print("\n----------------------------------------");
      print("\t\tMAIN MENU");
      print("----------------------------------------");
      print("\t1. VIEW ACCOUNT DETAILS");
      print("\t2. SET RATE OF INTREST");
      print("\t3. EXIT");    
      print("----------------------------------------");

def printModify():
      print("""\n----------------------------------------
                1. UPDATE NAME
                2. UPDATE ADDRESS
                3. UPDATE MOBILE NO
                4. EXIT
----------------------------------------""");
                        
def getChoice():
      ch=int(input("\tEnter Your Choice = "));
      return ch;

about();
d=0;
d=getDivision();

while d:
      if d==1:
            print("\n\t\tLog in");
            print("----------------------------------------");
            unm=input("\tEnter User Name = ");
            pswd=input("\tEnter Password = ");
            mycursor.execute("Select * from admin");
            for row in mycursor:
                  if unm==row[1] and pswd==row[2]:
                        printMenuAdmin();
                        ch=getChoice();
                        while ch!='3':
                              if ch==1:
                                    displayAccounts();
                              elif ch==2:
                                    setInterest();
                              elif ch==3:
                                    print("\n------Thank you. Have a nice Day!-------\n");
                                    d=getDivision();
                                    break;
                              else :
                                    print("\n**** Error : Invalid Choice ****\n\t");
                              printMenuAdmin();
                              ch=getChoice();
                  else:
                        print("\nError : Invalid UserName or Password\n");
                        d=getDivision();
                  
      elif d==2:
            print("\n\t\tLog in");
            print("----------------------------------------");
            unm=input("\tEnter User Name = ");
            pswd=input("\tEnter Password = ");
            if unm=="manager" and pswd=="manager":
                  printMenu();
                  ch=getChoice();

                  while ch!= '10' :
                        if ch==1 :
                              newAccount();
                        elif ch==2 :
                              deposite();
                        elif ch==3 :
                              withdraw();
                        elif ch==4 :
                              balanceInq();
                        elif ch==5 :
                              displayAccounts();
                        elif ch==6 :
                              closeAccount();
                        elif ch==7 :
                              updateAccount();
                        elif ch==8 :
                              viewTransaction();
                        elif ch==9:
                              calcIntrest();
                        elif ch==10 :
                              print("\n------Thank you. Have a nice Day!-------\n");
                              d=getDivision();
                              break;
                        else :
                              print("\n**** Error : Invalid Choice ****\n\t");
                        printMenu();
                        ch=getChoice();
            else:
                  print("\nError : Invalid UserName or Password\n");
                  d=getDivision();
                  
      elif d==3:
            print("\n------Thank you. Have a nice Day!-------\n");
            d=0;
            break;
      else :
            print("Error : Enter Valid Choice");
            d=getDivision();

mycursor.close();
mydb.close();
