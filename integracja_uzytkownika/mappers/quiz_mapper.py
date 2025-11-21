def map_question_row(row):
    return {
        "id": row[0],
        "tresc": row[1]
    }

def map_answer_row(row):
    return {
        "text": row[0],
        "correct": row[1]
    }
