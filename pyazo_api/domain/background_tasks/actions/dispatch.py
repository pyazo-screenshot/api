from fastapi import BackgroundTasks


class DispatchAction():
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks

    def __call__(self, action: callable, *args, **kwargs):
        self.background_tasks.add_task(action, *args, **kwargs)
