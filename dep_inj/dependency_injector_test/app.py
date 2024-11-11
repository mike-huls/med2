import os
import hashlib


from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from dep_inj.dependency_injector_test.example_services import ApiClientExample, PhotoService, TopicExample


def hash_string(target_string: str, salt_size: int) -> str:
    """Hash a password using SHA-256 (without salt for simplicity)."""
    # Generate a 16-byte salt
    salt = os.urandom(salt_size)

    # Convert the password to bytes and concatenate with the salt
    password_salt_bytes = target_string.encode("utf-8") + salt

    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the concatenated password and salt
    hash_object.update(password_salt_bytes)

    # Get the hexadecimal digest of the hash
    hashed_password = hash_object.hexdigest()

    # Convert the salt to hexadecimal for storage
    # salt_hex = salt.hex()

    # Return the hashed password and salt for storage
    return hashed_password


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    api_client = providers.Singleton(
        ApiClientExample,
        url=config.api.url,
        token=config.api.token,
        timeout=config.api.timeout,
    )

    photo_service = providers.Factory(
        PhotoService,
        api_client=api_client,
    )

    # This service will not be used by the services
    optional_service = providers.Singleton(
        TopicExample,
        url=config.topic.url,
        path=config.topic.path,
        token=config.topic.token,
    )

    # password_hasher = providers.Callable(
    #     hash_string,
    #     target_string='jojo',
    #     salt_size=16,
    # )
    # password_verifier = providers.Callable(passlib.hash.sha256_crypt.verify)


@inject
def main(photo_service: PhotoService = Provide[Container.photo_service]) -> None:
    print("MAIN")
    print(photo_service)


@inject
def get_all(
    api_client: ApiClientExample = Provide[Container.api_client],
    photo_service: PhotoService = Provide[Container.photo_service],
    # password_hasher: providers.Callable = Provide[Container.password_hasher]
):
    print("GET ALL")
    print(api_client)
    print(photo_service)
    # print(f"hasher says: {password_hasher}")
    # print(f"hasher says: {password_hasher(target_string='jojo')}")


@inject
def get_more(api_client: ApiClientExample = Provide[Container.api_client], photo_service: PhotoService = Provide[Container.photo_service]):
    print("GET MORE")
    print(api_client)
    print(photo_service)


@inject
def inject_config(api_timeout: int = Provide[Container.config.api.timeout.as_(int)]):
    print("inject config")
    print(f"{api_timeout=}")


def get_stuff():
    print("api client is from a singleton")
    api_client1 = Container.api_client()
    api_client2 = Container.api_client()
    print(api_client1)
    print(api_client2)

    print("service is from a factory")
    photo_service1 = Container.photo_service()
    photo_service2 = Container.photo_service()
    print(photo_service1)
    print(photo_service2)


def try_user_unregistered_app(topic_listener: TopicExample = Provide[Container.optional_service]):
    print("unregistered topic listener")
    print(topic_listener)


def init_app():
    container = Container()
    os.environ["API_URL"] = "MY_API_URL"
    os.environ["API_TOKEN"] = "MY_API_TOKEN"
    os.environ["API_TIMEOUT"] = "5"

    container.config.api.url.from_env("API_URL", required=True)
    container.config.api.token.from_env("API_TOKEN")
    container.config.api.timeout.from_env("API_TIMEOUT", as_=int, default=5)
    container.wire(modules=[__name__])

    main()  # <-- dependency is injected automatically
    get_all()
    get_more()
    inject_config()
    get_stuff()
    # print(hash_string('jojo', 16))
    # with container.api_client.override(mock.Mock()):
    #     main()  # <-- overridden dependency is injected automatically

    try:
        try_user_unregistered_app()
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    init_app()
