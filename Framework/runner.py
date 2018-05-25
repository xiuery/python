from task.Drop_Ship_PO_Process.Task_Handler import TaskHandler


class Runner(object):
    def __init__(self):

        self.task_handler = TaskHandler()

    def setup(self):
        self.task_handler.start()

    def teardown(self):
        self.task_handler.stop()


if __name__ == '__main__':
    task = Runner()
    task.setup()
    task.teardown()
