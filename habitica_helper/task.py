"""
A representation of a Habitica task.
"""

import datetime
from habitica_helper import habrequest


class Task():
    """
    A Habitica task: can be either habit, daily or a todo.
    """

    # Counterparts for variables in Habitica API where the naming differs.
    habitica_keys = {
        "uppable": "up",
        "downable": "down",
        "difficulty": "priority",
    }

    habitica_difficulties = {
        "trivial": 0.1,
        "easy": 1,
        "medium": 1.5,
        "hard": 2,
        }

    def __init__(self, task_data):
        """
        Create a new task instance based on the given data.

        The given task_data dict MUST contain at least the following keys and
        values:
        text: Name of the task (str)
        tasktype: Either "habit", "daily" or "todo".

        The following optional keys are also supported:
        notes: A longer description for the task (str)
        date: A due date for the task. Either a timestamp string in format
              "yyyy-mm-dd" or an instance of date/datetime.
        frequency: How often the streak is reset. Possible values are "daily",
                   "weekly", "monthly" and "yearly"
        difficulty: The difficulty of the task. Values "trivial", "easy",
                    "medium" and "hard" are supported. If no value is given,
                    the task is created as an easy one.
        uppable: Whether the '+' of a habit is active. "true" or "false".
        downable: Whether the '-' of a habit is active. "true" or "false"
        """
        self.text = task_data.get("text", None)
        self.tasktype = task_data.get("tasktype", None)
        self.notes = task_data.get("notes", "")
        self.date = task_data.get("date", None)
        self.frequency = task_data.get("frequency", None)
        self.difficulty = task_data.get("difficulty", "easy")
        self.uppable = task_data.get("uppable", "true")
        self.downable = task_data.get("downable", "false")

    def __eq__(self, obj):
        """
        Two tasks are the same task if they have the same type, text and notes.
        """
        if not isinstance(obj, Task):
            return False
        return (self.tasktype == obj.tasktype and
                self.text == obj.text and
                self.notes == obj.notes)

    def __neq__(self, obj):
        return not self.__eq__(obj)

    def __hash__(self):
        return hash((self.tasktype, self.text, self.notes))

    def __str__(self):
        return "\n".join(["{}: {}".format(key, val) for key, val in
                          self._task_dict().items()])

    def create_to_challenge(self, challenge_id, header):
        """
        Make the given challenge contain this task.

        :challenge_id: The unique identifier of the challenge.
        :header: Habitica API header
        """
        habrequest.post("https://habitica.com/api/v3/tasks/challenge/{}"
                        "".format(challenge_id),
                        headers=header,
                        data=self._task_dict()
                        )

    def add_to_user(self, header):
        """
        Add the current task to personal tasks of the user.

        :header: Habitica API header.
        """
        habrequest.post("https://habitica.com/api/v3/tasks/user",
                        headers=header,
                        data=self._task_dict()
                        )

    def _task_dict(self):
        """
        Return this task in the standard Habitica API form.
        """
        datadict = {"text": self.text, "type": self.tasktype}
        for key in ["notes", "date", "difficulty", "uppable", "downable",
                    "frequency"]:
            if getattr(self, key) not in [None, ""]:
                datadict[self.habitica_keys.get(key, key)] = getattr(self, key)
        return datadict

    @property
    def text(self):
        """
        Task name
        """
        return self._text

    @text.setter
    def text(self, text):
        if not isinstance(text, str):
            raise ValueError("Task name must be a string. Type {} encountered "
                             "instead.".format(type(text)))
        if not text:
            raise ValueError("Task name cannot be empty.")
        self._text = text

    @property
    def notes(self):
        """
        Additional notes
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        if notes is None:
            self._notes = ""
        elif not isinstance(notes, str):
            raise ValueError("Task notes must be a string. Type {} "
                             "encountered instead".format(type(notes)))
        else:
            self._notes = notes

    @property
    def tasktype(self):
        """
        Type of the task.

        Possible values are "todo", "daily" and "habit".
        """
        return self._type

    @tasktype.setter
    def tasktype(self, tasktype):
        if tasktype is None:
            raise ValueError("Task type not provided.")
        if tasktype.lower() not in ["todo", "daily", "habit"]:
            raise ValueError("Illegal task type {}. Supported values are "
                             "'todo', 'daily' and 'habit'.")
        self._type = tasktype

    @property
    def date(self):
        """
        Due date for the task.
        """
        if not self._date:
            return None
        return self._date.strftime("%Y-%m-%d")

    @date.setter
    def date(self, date):
        if date is None:
            self._date = None
        elif type(date) in [datetime.date, datetime.datetime]:
            self._date = date
        elif isinstance(date, str):
            try:
                self._date = datetime.datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Date string {} could not be parsed into "
                                 "a deadline for a task.")
        else:
            raise ValueError("Illegal task deadline type ({}) encountered."
                             "".format(type(date)))

    @property
    def frequency(self):
        """
        How often the streak is reset.

        Possible values are "daily", "weekly", "monthly" or "yearly".
        """
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        if frequency not in ["daily", "weekly", "monthly", "yearly", None]:
            raise ValueError("Illegal frequency value {} encountered."
                             "".format(frequency))
        self._frequency = frequency

    @property
    def difficulty(self):
        """
        Difficulty of the task.

        Allowed input values are "trivial", "easy", "medium" and "hard", or the
        corresponding numeric values 0.1, 1, 1.5 and 2. The value is returned
        as the numeric value.
        """
        return self._difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        if difficulty in self.habitica_difficulties.values():
            self._difficulty = difficulty
        elif difficulty.lower() in self.habitica_difficulties:
            self._difficulty = self.habitica_difficulties[difficulty.lower()]
        else:
            raise ValueError("Illegal task difficulty {} encountered. Allowed "
                             "values are 'trivial', 'easy', 'medium' and "
                             "'hard'".format(difficulty))

    @property
    def uppable(self):
        """
        Whether a habit has the '+' enabled.
        """
        return self._uppable

    @uppable.setter
    def uppable(self, uppable):
        if isinstance(uppable, bool):
            self._uppable = str(uppable).lower()
        elif uppable not in [None, "True", "False", "true", "false"]:
            raise ValueError("Illegal value encountered when setting whether "
                             "a task should have the '+' enabled: must be "
                             "either 'true' or 'false' but {} was encountered."
                             "".format(type(uppable)))
        self._uppable = uppable.lower()

    @property
    def downable(self):
        """
        Whether a habit has the '-' enabled.
        """
        return self._downable

    @downable.setter
    def downable(self, downable):
        if downable not in [None, "True", "False", "true", "false"] and not isinstance(downable, bool):
            raise ValueError("Illegal value encountered when setting whether "
                             "a task should have the '+' enabled: must be a "
                             "boolean but {} was encountered."
                             "".format(type(downable)))
        self._downable = downable.lower()
