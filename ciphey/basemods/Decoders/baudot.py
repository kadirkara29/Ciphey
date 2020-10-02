import re
from typing import Optional, Dict, FrozenSet

from ciphey.iface import ParamSpec, Config, T, U, Decoder, registry, Translation, Level


@registry.register
class Baudot(Decoder[str]):
    def decode(self, ctext: T) -> Optional[U]:
        ret = ""
        switch_to_digit_map = 0
        if type(ctext) == str:
            if re.search("^[01]{5}$", ctext.split()[0]):
                for i in ctext.split():
                    if i == "11011":
                        switch_to_digit_map = 1
                    if i == "11111":
                        switch_to_digit_map = 0
                    if switch_to_digit_map == 1:
                        ret += self.BAUDOT_DICT["+" + i]
                    if switch_to_digit_map == 0:
                        ret += self.BAUDOT_DICT[i]
                return ret
        else:
            return None

    def __init__(self, config: Config):
        super().__init__(config)
        self.BAUDOT_DICT = config.get_resource(self._params()["dict"], Translation)

    @staticmethod
    def getParams() -> Optional[Dict[str, ParamSpec]]:
        return {
            "dict": ParamSpec(
                desc="The baudot alphabet dictionary to use",
                req=False,
                default="cipheydists::translate::baudot",
            )
        }

    @staticmethod
    def getTags() -> FrozenSet[str]:
        return frozenset({"baudot", "substitution", "telecom"})

    @staticmethod
    def getLevel() -> Level:
        return Level.VeryRare

