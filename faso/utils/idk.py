def string_to_list(string):
    # Remove the brackets and spaces from the string
    string = string.replace("[", "").replace("]", "").replace(" ", "")
    
    # Split the string by commas and convert each element to an integer
    integer_list = [int(x) for x in string.split(",")]
    
    return integer_list
    return converted_list