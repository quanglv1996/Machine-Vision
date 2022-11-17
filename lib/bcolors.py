class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print_ok(text=''):
        print(bcolors.OKGREEN + text + bcolors.ENDC)

    @staticmethod
    def print_fail(text=''):
        print(bcolors.FAIL + text + bcolors.ENDC)

    @staticmethod
    def print_warning(text=''):
        print(bcolors.WARNING + text + bcolors.ENDC)
        
    @staticmethod
    def print_underline(text=''):
        print(bcolors.UNDERLINE + text + bcolors.ENDC)
        
    @staticmethod
    def print_bold(text=''):
        print(bcolors.BOLD + text + bcolors.ENDC)
        
    @staticmethod
    def print_header(text=''):
        print(bcolors.HEADER + text + bcolors.ENDC)
        
def main():
    bcolors.print_ok('OK')
    bcolors.print_fail('Fail')
    bcolors.print_warning('Warning')
    bcolors.print_bold('Bold')
    bcolors.print_header('Header')
    bcolors.print_underline('Under line')
    
if __name__ == '__main__':
    main()