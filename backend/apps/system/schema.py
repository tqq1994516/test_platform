from dataclasses import dataclass


@dataclass
class LoginSchema:
    username: str
    password: str

