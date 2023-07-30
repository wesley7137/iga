class Env:
    def __init__(
        self,
        states: dict = {},
        current: int = 0
    ):
        self.states = states
        self.current = current

    def get_current_state(self):
        return self.states[self.current]

    def get_previous_state(self):
        if self.current>0:
            return self.states[self.current -1]
        else:
            return None
        
