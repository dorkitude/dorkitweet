# stdlib imports:
pass
# third-party imports:
from pycloudapp import cloud
# our imports:
from models.cloud_app import CloudAppAccount




def shorten_urls(text):
    """
    :param text: String.
    :returns: String.
    """

    # Fetch our account model:
    cloud_account = CloudAppAccount.get_default()

    # Configure the pycloud module:
    cloud.URI = cloud_account.URI

    # Create a pycloud client instance:
    cloud_client = cloud.Cloud()

    # Authenticate:
    cloud_client.auth(cloud_account.username, cloud_account.password)
