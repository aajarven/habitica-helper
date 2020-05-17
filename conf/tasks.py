"""
Dictionaries for representing some often-needed tasks.
"""

# Sharing Weekend challenge habit for sharing positive things
WEEKLY_POSITIVE = {
    "text": "Share something positive in party chat",
    "notes": "a success, a quote, a cute or funny picture or link, or "
             "anything else positive",
    "type": "habit",
    "up": "true",
    "down": "false",
    "frequency": "weekly",
    "priority": 2,
    }

# Sharing Weekend challenge task for sharing a success from the previous week
WEEKLY_SUCCESS = {
    "text": "Share a success from the week in party chat",
    "notes": "Let's celebrate our wins together, small, large, or in-between",
    "type": "todo",
    "priority": 2,
#    "date": due_date,
    }


# Sharing Weekend challenge task for setting a goal for the next week
WEEKLY_GOAL = {
    "text": "Share a goal for the upcoming week in party chat",
    "notes": "What do you want/need to work on that can be accomplished "
             "in the short-term? Try to make your goals challenging but also "
             "attainable",
    "type": "todo",
    "priority": 2,
#    "date": due_date,
    }

WEEKLY_QUESTION = {
#    "text": weekly_question,
#    "notes": weekly_question_notes,
    "type": "todo",
    "priority": 2,
#    "date": due_date,
    },
