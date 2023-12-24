from math import ceil

# return the product produced
# increment the operation index after calling this function
# received products is a list of tuples 
# where first element is the pid of the child
# and second element is the product recieved 
def produce(received_products, operation):

    # every machine should start with an add operation
    received_products = sorted(received_products)
    received_products = [tup[1] for tup in received_products]
    product = ""
    for rec_prod in received_products:
        product += rec_prod
    
    if operation == "enhance":
        product = product[0] + product + product[-1]

    if operation == "reverse":
        product = product[-1::-1]

    if operation == "chop":
        if len(product) > 1:
            product = product[0:-1]

    if operation == "trim":
        if len(product) > 2:
            product = product[1:-1]

    if operation == "split":
        product = product[:ceil(len(product)/2)]

    return product


