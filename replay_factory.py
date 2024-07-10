from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        current_question_id = 0

    success, error = record_current_answer(message, current_question_id, session)
    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)
    if next_question_id != -1:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses

def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question ID."

    # Validate answer - assuming a simple non-empty validation for demonstration
    if not answer:
        return False, "Answer cannot be empty."

    # Store the answer in the session
    session[f"answer_{current_question_id}"] = answer
    return True, ""

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id = current_question_id + 1
    if next_question_id < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_question_id], next_question_id
    else:
        return None, -1

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question_id in range(total_questions):
        answer = session.get(f"answer_{question_id}")
        if answer and validate_answer(answer, question_id):
            score += 1

    result_message = f"You've completed the quiz! Your score is {score}/{total_questions}."
    return result_message

def validate_answer(answer, question_id):
    '''
    Validates the user's answer based on the question.
    This is a placeholder for actual validation logic.
    '''
    # Implement actual validation logic here
    # For now, assume all non-empty answers are valid
    return bool(answer)
