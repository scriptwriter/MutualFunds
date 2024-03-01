from lambda_function import lambda_handler

# Simulate an empty event and context
event = {}
context = {}

# Call the lambda_handler function
response = lambda_handler(event, context)

# Print the response to see the output
print(response)
