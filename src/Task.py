from datetime import datetime

class Task:
    def __init__(self,
                    id: int,
                    description="",
                    completed="incomplete",
                    creation_date= datetime.now().isoformat(),
                    last_modified_date = datetime.now().isoformat(),
                ):
        self.id = id
        self.description = description
        self.completed = completed
        self.creation_date = creation_date
        self.last_modified_date = last_modified_date

    def mark_as_completed(self):
        self.completed = "completed"
        self.update_last_modified()

    def mark_as_incomplete(self):
        self.completed = "incomplete"
        self.update_last_modified()
    
    def mark_as_inprogress(self):
        self.completed = "in progress"
        self.update_last_modified()
    
    def update(self, description=None):
        self.description = description
        self.update_last_modified()
    
    def update_last_modified(self):
        self.last_modified_date = datetime.now().isoformat()

    def __str__(self):
        if self.completed == "completed":
            completed = "[x]"
        elif self.completed == "inprogress":
            completed = "[/]"
        else:
            completed = "[ ]"

        return f"{self.id}.) {completed} {self.description}"

    def __json__(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        if ("id" not in data or
            "description" not in data or
            "completed" not in data or
            "creation_date" not in data or
            "last_modified_date" not in data):
            raise Exception("Failed to parse dictionary")

        return cls(
            id=data["id"],
            description=data["description"],
            completed=data["completed"],
            creation_date=data["creation_date"],
            last_modified_date=data["last_modified_date"]
        )
