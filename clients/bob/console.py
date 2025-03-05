from os import system, name

class Console:
    @staticmethod
    def clear_screen():
        if name == 'nt':       # for windows
            _ = system('cls')
        else:                  # for posix (i.e. mac and linux)
            _ = system('clear')

    @staticmethod
    def title(title, underline='-'):
        print(title)
        print(underline * len(title))    

    @staticmethod
    def select_from_menu(prompt, number_of_items):
        range = f'[1-{number_of_items}]'

        while True:
            choice = input(f'{prompt} {range} (q to quit, c to cancel): ')
            if choice.lower() == 'q':
                quit(1)
            if choice.lower() == 'c':
                return
            try:
                rtn = int(choice)
            except ValueError:
                rtn = 0

            if 1 <= rtn <= number_of_items:
                return rtn - 1

            print('Invalid choice, please try again.')

    @staticmethod
    def input_with_quit_or_cancel(prompt):
        entry = input(f'{prompt} (q to quit, c to cancel): ')
        if entry.lower() == 'c':
            return
        if entry.lower() == 'q':
            quit(1)
        return entry

    @staticmethod
    def prompt_for_fields(prompts):
        responses = {}
        for key, prompt in prompts.items():
            response = input_with_quit_or_cancel(prompt)
            if response is None:
                return None
            responses[key] = response
        return responses
