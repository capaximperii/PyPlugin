"""
Runs a task as an asynchronous thread with callback handler for database update.

"""
from threading import Thread
from functools import partial

class TaskRunner(Thread):
    """
    Defines class task runner that runs an asynchronous task and registers callbacks.

    """
    def __init__(self, obj, run_function, **kwargs):
        """
        Builds the task runner object.

        """
        #Assign all kwargs to the member variables.
        # self.__dict__.update(kwargs)
        # for (key, val) in kwargs.items():
        #     setattr(self, key, val)
        self.task_arguments = kwargs
        # UGLY: The object that owns the function needs to be called in the context of that object.
        self.obj = obj
        self.run_function = run_function
        super(TaskRunner, self).__init__()
        print("Initialized the task")

    def run(self):
        """
        Run the task.

        """
        try:
            func = self.run_function
            func(self=self.obj)
            self.success_callback()
        except BaseException as exp:
            print(str(exp))
            self.failure_callback()


    def success_callback(self):
        """
        Handle success.

        """
        print("Finished success called with ", self.task_arguments, " finished with ")

    def failure_callback(self):
        """
        Handle exception.

        """
        print("Finished failure called with ", self.task_arguments, " finished with ")
