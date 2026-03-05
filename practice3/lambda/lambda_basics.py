# 1. Простейший Lambda
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": "Hello, AWS Lambda!"
    }

# 2. Lambda с параметром из event
def greet_handler(event, context):
    name = event.get("name", "World")
    return {
        "statusCode": 200,
        "body": f"Hello, {name}!"
    }

# 3. Lambda с математической операцией
def sum_handler(event, context):
    a = event.get("a", 0)
    b = event.get("b", 0)
    return {
        "statusCode": 200,
        "body": str(a + b)
    }

# 4. Lambda с использованием переменной окружения
import os

def env_handler(event, context):
    stage = os.environ.get("STAGE", "dev")
    return {
        "statusCode": 200,
        "body": f"Stage: {stage}"
    }

# 5. Lambda с обработкой ошибки
def safe_divide_handler(event, context):
    try:
        a = event.get("a", 1)
        b = event.get("b", 1)
        result = a / b
        return {"statusCode": 200, "body": str(result)}
    except ZeroDivisionError:
        return {"statusCode": 400, "body": "Division by zero error"}