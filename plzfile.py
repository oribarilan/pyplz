from plz.app import plz


@plz.task()
def brew_coffee():
    """
    Brew coffee
    """
    plz.log("Brewing coffee")


@plz.task()
def check_emails():
    """
    Check emails
    """
    plz.log("Checking emails")


@plz.task()
def take_a_nap():
    """
    Take a nap
    """
    plz.log("Taking a nap")
