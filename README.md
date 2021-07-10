# Greenhouse Bot by \_Counter021_

## `Installing:`

    Need install repository 
        https://github.com/Counter0021/django-react-redux-greenhouse-2

    Run django project

    python -m venv DirectoryVENV
    source DirectoryVENV/bin/activate
    pip install -r requirements.txt
    
    create file "config.env" (how in config.ini):
        TOKEN=<your-token-for-telegram-bot>

    run file "bot.py"

## Commands:

### `User Commands`

    /login - Authorization (only unauthorized users)
    /register - Register a new user (only unauthorized users)
    /reset_password - Send email to reset user's password (only unauthorized users)
    /logout - Logout (authorized users only)
    /profile - User orders (only for authorized users)

### `Cart commands`

    /cart - Cart (for authorized users only)
    /add - Add a product to the cart. This command must be used to reply to the message with the product (only for authorized users)
    /remove - Remove an item from the cart. This command must be used to reply to a message with an item in the cart (only for authorized users)
    /change - Change the number of items in the cart. With this command you need to reply to the message with the item in the cart and write how much you want to change this item (only for authorized users)
    /make - Checkout (for authorized users only)

### `Commands for withdrawing products from the store`

    /categories - Categories
    /products - Products
    /detail - Product details. This command must be used to reply to the message with the product.

### `Testimonial teams`

    /reviews - Reviews
    /new_review - Add a review (only for authorized users)

### `The rest of the teams`

    /help - Help
    /link - Link to our site
    /feedback - Feedback (errors, wishes)
    /dev - Developer information 
