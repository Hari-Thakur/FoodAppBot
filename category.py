import openai

openai.api_key = "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"

def classify_input(user_input):
    prompt = (
        "You are a helpful assistant. Your task is to categorize the user query into one of the following categories:\n"
        "1: Normal retrieval (e.g., asking about menu items or prices)\n"
        "2: Payment/confirmation (e.g., confirming the order, generating payment)\n"
        "3: Adding order to cart / Wanting to order something (e.g., updating or querying the current order)\n"
        "4: Out-of-scope queries (e.g., questions unrelated to food delivery)\n"
        "5: Feedback/support (e.g., complaints, feedback, contact support)\n"
        "The user may ask in Hindi, English, Telugu, or a mix of these languages. Respond with the category number only.\n"
        "Example interactions:\n"
        "User: 'I want to order 1 plate noodles'\n"
        "Category: 3\n"
        "User: 'I would like to confirm my order.'\n"
        "Category: 2\n"
        "User: 'What is my current order?'\n"
        "Category: 1\n"
        "User: 'Who is the prime minister of India?'\n"
        "Category: 4\n"
        "User: 'Mere biryani ka taste acha nahi tha'\n"
        "Category: 5\n"
        "User: 'Tindaniki em em unai?'\n"
        "Category: 1\n"
        "User: 'What dishes do you have?'\n"
        "Category: 1\n"
        "User: 'Khane me kya kya hai?'\n"
        "Category: 1\n"
        "User: 'What is the price of noodles?'\n"
        "Category: 1\n"
        "User: 'How much is Chowmein?'\n"
        "Category: 1\n"
        "User: 'Add one plate biryani'\n"
        "Category: 3\n"
        "User: 'I would like to pay for my order.'\n"
        "Category: 2\n"
        "User: 'Confirm my order please.'\n"
        "Category: 2\n"
        "User: 'Tell me about The Great Wall restaurant.'\n"
        "Category: 1\n"
        "User: 'I would like to update my current order.'\n"
        "Category: 3\n"
        "User: 'What is my previous order?'\n"
        "Category: 1\n"
        "User: 'What is the capital of France?'\n"
        "Category: 4\n"
        "User: 'How's the weather today?'\n"
        "Category: 4\n"
        "User: 'Mujhe menu dikhaiye.'\n"
        "Category: 1\n"
        "User: 'Kya tum mere order ka status bata sakte ho?'\n"
        "Category: 1\n"
        "User: 'Order ka price kitna hai?'\n"
        "Category: 2\n"
        "User: 'I want to give feedback about my order.'\n"
        "Category: 5\n"
        "User: 'I need to talk to support.'\n"
        "Category: 5\n"
        "User: 'There was a problem with my order.'\n"
        "Category: 5\n"
        "User: " + user_input + "\n"
        "Category:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful food-delivery app assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=5,
        temperature=0
    )

    category = response['choices'][0]['message']['content'].strip()
    
    return int(category)

# Example usage
user_input = input("Enter query:")
category = classify_input(user_input)
print(f"Category: {category}")
