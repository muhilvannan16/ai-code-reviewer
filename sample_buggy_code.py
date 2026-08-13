def add_to_cart(item, cart=[]):
    cart.append(item)
    return cart


def get_average_price(prices):
    total = 0
    for i in range(len(prices) - 1):
        total += prices[i]
    return total / len(prices)


def find_user(users, user_id):
    for i in range(len(users)):
        if users[i]["id"] is user_id:
            return users[i]
    return None
