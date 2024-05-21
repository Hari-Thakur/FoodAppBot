FOOD APP BOT

ABOUT - 

This system is a helpful AI chatbot for food delivery apps , it contains the following components - 

      •	LLM Model ( Here Claude 3.0 - opus-20240229 )
      
      •	Flask interface containing Front-end and Backend
      
      •	Database - sqlLite (foodappbot.db)
      
The function of this chatbot , is to act like an assistant for the user , and guide him by providing details about menu , orders , provide recommendations and also provide personalized output based on user preferences and feedback 
The requirements of this system are - 

      1.	Claude-3 Api key
      
      2.	Python
      
      3.	Web Browser

WORKING - 

  1)	Clone the repository 
  2)	Run the python command ‘pip install -r requirements.txt 
  3)	Add the Claude api in main.py
  4)	Run the Setup_database file as - ‘python setup_database.py’
  5)	Run the main.py script as - ‘python main.py’
  6)	You will be redirected to the local host port in the web browser , where the chatbot is integrated , now you can chat and the system is now working

STEPS OF WORKING -

STEP - 1 (input collection)
The system takes 2 kinds of input , text and voice , user can choose from the input type . The system is built to understand the languages like -> Hindi , English , Telugu or a mixture of these 

STEP - 2 (CRUD OPERATIONS GENERATION)
The System first receives the user input and then has 2 models of Claude-3 

1.	CRUD operation Claude model - This model takes user input and also has the basic structure of the database with it , it analyses the user input and outputs the appropriate SQL query for the user input
   
Some examples include - 

      1)   "User:  'What dishes do you have?' or ‘Khane me kya hai?’ or ‘Tindaniki em-em unai?’
           "SQL:  SELECT dish FROM menu;"
           
      3)   "User: 'How much is Chowmein?'"
       		 "SQL: SELECT price FROM menu WHERE LOWER(dish) LIKE 'chowmein';" 
          
      3)   "User: 'What are my last two orders?'\n"
           "SQL: SELECT * FROM orders WHERE id IN (SELECT previous_orders FROM users WHERE id = 1 ORDER BY id DESC LIMIT 2);\n"
           
      4)   "User: 'How much did my last order cost?'\n"
      	   "SQL: SELECT price FROM orders WHERE id = (SELECT previous_orders FROM users WHERE id = 1 ORDER BY id DESC LIMIT 1);\n"
And many more.

STEP - 3 (SQL Query Execution)

The SQL query generated is then collected as a list and is executed , then the results variable is appended with the output of the execution

STEP - 4 (Output Generation)

The result from the SQL execution along with user input is provided to the second Claude-3 model , this analyzes the user input . It understands the user language and is trained to generate content in the same tone and language of the user .
It is built around to act as a Food Delivery Chatbot Assistant.

It receives the result and then uses the data in it to answer to the user query

Functionalities - 

-	User input Integration

-	Prompt Engineering

-	Front-end and Back End Integration


Requirements - 

Flask==3.0.0
anthropic==0.26.0
SpeechRecognition==3.10.1
pydub==0.25.1

SCREENSHOTS - 

![2](https://github.com/Hari-Thakur/FoodAppBot/assets/157131792/eec61ba3-d7dd-4280-bf60-8d6c9fc89ed6)

![1](https://github.com/Hari-Thakur/FoodAppBot/assets/157131792/e49737d3-9332-403f-89a4-f04ce865f962)

![7](https://github.com/Hari-Thakur/FoodAppBot/assets/157131792/71b068e8-7934-4b25-9750-fcd456a5a456)

![6](https://github.com/Hari-Thakur/FoodAppBot/assets/157131792/16f47b6f-0401-44ea-a31c-864528988333)

![5](https://github.com/Hari-Thakur/FoodAppBot/assets/157131792/a23c781e-783d-4827-87c5-4c5ba3836a13)

![4](https://github.com/Hari-Thakur/FoodAppBot/assets/157131792/8809e3f3-8ebc-4afa-8d23-1fd1ccc49595)

![3](https://github.com/Hari-Thakur/FoodAppBot/assets/157131792/21217018-f8d6-410b-92d0-1f46770d40b1)
