from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Create the database file
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# Create a model class that describes the table in the database
# All model classes should inherit from the DeclarativeMeta class that is returned by declarative_base()
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# Create the table described, in the database
Base.metadata.create_all(engine)

# Create a session to access and store data in the database
Session = sessionmaker(bind=engine)
session = Session()

while 1:
    print("\n1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")

    userChoice = int(input())

    if userChoice == 1:
        # Show today's tasks
        today = datetime.today()
        print("Today " + str(today.day) + " " + today.strftime('%b'))

        # Retrieve all today's tasks from database
        tasks = session.query(Table).filter(Table.deadline == today.date()).all()

        if len(tasks) > 0:
            for t in tasks:
                print(str(t.id)+". "+t.task)
        else:
            print("Nothing to do!")
    elif userChoice == 2:
        # Week's tasks
        today = datetime.today()

        for i in range(0, 7):
            current_day_date = today + timedelta(days=i)
            current_week_day = current_day_date.weekday()
            current_day_tasks = session.query(Table).filter(Table.deadline == current_day_date.date()).order_by(
                Table.deadline).all()
            if current_week_day == 0:
                print("\nMonday " + str(current_day_date.day) + " " + current_day_date.strftime('%b') + ":")
            elif current_week_day == 1:
                print("\nTuesday " + str(current_day_date.day) + " " + current_day_date.strftime('%b') + ":")
            elif current_week_day == 2:
                print("\nWednesday " + str(current_day_date.day) + " " + current_day_date.strftime('%b') + ":")
            elif current_week_day == 3:
                print("\nThursday " + str(current_day_date.day) + " " + current_day_date.strftime('%b') + ":")
            elif current_week_day == 4:
                print("\nFriday " + str(current_day_date.day) + " " + current_day_date.strftime('%b') + ":")
            elif current_week_day == 5:
                print("\nSaturday " + str(current_day_date.day) + " " + current_day_date.strftime('%b') + ":")
            elif current_week_day == 6:
                print("\nSunday " + str(current_day_date.day) + " " + current_day_date.strftime('%b') + ":")
            if len(current_day_tasks) > 0:
                for t in current_day_tasks:
                    print(str(t.id) + ". " + t.task)
            else:
                print("Nothing to do!")
    elif userChoice == 3:
        # Show all tasks
        print("All tasks:")

        tasks = session.query(Table).order_by(Table.deadline).all()

        if len(tasks) > 0:
            for t in tasks:
                print(str(t.id) + ". " + t.task + ". " + str(t.deadline.day) + " " + t.deadline.strftime('%b'))

    elif userChoice == 4:
        # Missed Tasks

        # Retrieve all tasks with deadline before today
        today = datetime.today()
        earlier_tasks = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()

        if len(earlier_tasks) > 0:
            for t in earlier_tasks:
                print(str(t.id) + ". " + t.task + ". " + str(t.deadline.day) + " " + t.deadline.strftime('%b'))
        else:
            print("Nothing is missed!")
    elif userChoice == 5:
        # Add task
        task_name = input("Enter task")
        task_deadline = datetime.strptime(input("Enter deadline"), '%Y-%m-%d')

        # Retrieve all today's tasks and select the last one
        tasks = session.query(Table).all()

        new_id = 1
        if len(tasks) > 0:
            last_task = tasks[len(tasks)-1]
            new_id = last_task.id+1

        new_task = Table(id=new_id,
                         task=task_name,
                         deadline=task_deadline)
        session.add(new_task)
        session.commit()
        print("The task has been added!")
    elif userChoice == 6:
        # Delete specific task
        print("Choose the number of the task you want to delete:")
        tasks = session.query(Table).order_by(Table.deadline).all()

        if len(tasks) > 0:
            for t in tasks:
                print(str(t.id) + ". " + t.task + ". " + str(t.deadline.day) + " " + t.deadline.strftime('%b'))
        else:
            print("Nothing to delete")

        task_to_delete = int(input())

        if len(tasks) > 0:
            for i in range(0, len(tasks)):
                if tasks[i].id == task_to_delete:
                    specific_task = tasks[i]
                    session.delete(specific_task)
                    session.commit()
                    print("The task has been deleted!")
    elif userChoice == 0:
        print("Bye!")
        exit()
