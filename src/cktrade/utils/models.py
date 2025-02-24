from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator


class CustomInputBase(BaseModel):
    title: str
    timeout: int = 0
    popup: Optional[str] = None


class NewTradeCustomInputs(CustomInputBase):
    type: Literal["option"] | Literal["bool"]
    options: Optional[list[CustomInputBase]] = None

    @model_validator(mode="after")
    def validate_timeout(self):
        if self.type == "option":
            if self.popup:
                raise ValueError(
                    "Popup is not supported globally for option type. Kindly use popup in individual options"
                )
            if self.timeout:
                raise ValueError(
                    "Timeout is not supported globally for option type. Kindly use timeout in individual options"
                )
            if not self.options or len(self.options) == 0:
                raise ValueError("No options were given.")
        return self


class NewTradeConfig(BaseModel):
    customInputs: list[NewTradeCustomInputs] = Field(alias="custom_inputs")
    checklist: list[str] = Field(alias="checklist")


class AppConfig(BaseModel):
    newTradeConfig: NewTradeConfig = Field(alias="new_trade")


if __name__ == "__main__":
    import yaml

    a = AppConfig(
        **yaml.safe_load(
            open("config/config.yaml"),
        )
    )
