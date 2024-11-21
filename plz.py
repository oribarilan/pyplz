from plz.app import plz


@plz.task()
def shoot():
    """
    Shoot the portal gun
    """
    print("Shooting portal gun")


@plz.task()
def load():
    """
    Load the portal gun
    """
    print("Loading portal gun")
