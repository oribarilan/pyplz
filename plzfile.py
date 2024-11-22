from plz.app import plz


@plz.task()
def brew_coffee():
    """Brew coffee"""
    plz.log("Brewing coffee")


@plz.task(requires=[brew_coffee])
def check_emails():
    """Check emails"""
    plz.log("Checking emails")


@plz.task()
def take_a_nap():
    """Take a nap"""
    plz.log("Taking a nap")


@plz.task(requires=[check_emails, take_a_nap])
def write_report():
    """Write report"""
    plz.log("Writing report")
