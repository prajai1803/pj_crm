class ColorPrintUtils:

    def error_print(value):
        print(f"\033[91m {value} \033[0m")
    
    def success_print(value):
        print(f"\033[92m {value} \033[0m")
    
    def warning_print(value):
        print(f"\033[93m {value} \033[0m")