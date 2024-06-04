FOOD APP BOT

ABOUT - 

This system is a helpful AI chatbot for food delivery apps , it contains the following components - 

      •	LLM Model ( Here Open - AI 3.5 Turbo )
      
      •	Python codes for categroies of user input
      
      •	Database - sqlLite (food1.db)
      
The function of this chatbot , is to act like an assistant for the user , and guide him by providing details about menu , orders , provide recommendations and also provide personalized output based on user preferences and feedback 
The requirements of this system are - 

      1.	Open - AI
      
      2.	Python
      
      3.	Command Prompt

WORKING - 

  1)	Clone the repository 
  2)	Run the python command ‘pip install -r requirements.txt 
  3)	Add the open api in main.py
  4)	Run the Setup_database file as - ‘python database.py’
  5)	Now , repeat the following steps for each input
  6)	Firt run the category.py file to determine the category of user input
  7)	Based on the output , do the following -
  8)	if output = 1 , then run the generate_sql.py file
  9)	if output = 2 , then run the confirm_payment.py file
  10)	if output = 3 , then run the current_order.py file
  11)	if output = 4 , then run the invalid.py file
  12)	if output = 5 , then run the feedback.py file

STEPS OF WORKING -

STEP - 1 ( user input categorization )
The file category.py takes the user input and categorises the input into one of 5 categories

process ----->


5 models 


1st model --->4 outputs --> 1 , 2 , 3 , 4 , 5 

1 --> normal retrival then --> goes to model 2 ( sql command generation ) ---> goes to model 3 ( response generation ) ---> output

2 --> payment / confirmation --> direct output

3 --> current order --> goes to model 3 --> output

4 --> other --> direct output

5 --> feedback --> goes to model 4 ( feedback sql generation ) ---> goes to model 5 ( response generation ) --> output


1 --> normal sql , like price , menu , normal info , current order info , previous order info

2 --> confirming order , just confirmation and payment stuff

3 --> setting current order , adding items into cart

4 --> who prime minister , all other invalid inputs , how's the weather today

5 --> the taste of my food was not nice , feedback related stuff


2nd model---> sql generation --> goes to 3rd model


3rd model---> output generation --> output


4th model ---> feedback sql generation --> goes to 5th model


5th model ---> output generation --> output


5 codes - 

a --> generate_sql.py --> takes category 1 input and generates sql command and outputs , the response based on the result of sql execution

b --> confirm_payment.py --> extract dishes from current order , calculate price and generate qr and wait for payment confirmation 

c --> current_order.py --> extracts info related to order from the user input and updates current_order cart based on that 

d --> invalid.py --> responds with a static message for the input which is out of scope for the food delivery system 

e --> feedback.py --> deals with 5th category input , takes input about feedback and generates sql command and responds to the user's feedback


Functionalities - 

-	User input Integration

-	Prompt Engineering

-	Front-end and Back End Integration


Requirements - 

Flask==3.0.0
anthropic==0.26.0
SpeechRecognition==3.10.1
pydub==0.25.1
openai
