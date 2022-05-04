import os
from json import dumps
from sys import argv

from yconverter.client import YConverter


class AlfredResponse:
    """Alfred results

    title: the title displayed on the Alfred dropdown
    subtitle: the subtitle displayed on the Alfred dropdown
    icon: the icon displayed on the Alfred dropdown
    autocomplete: the tab completion when pressing tab
    arg: the tab completion when pressing tab

    Examples:
        {
            "uid": "desktop",
            "type": "file",
            "title": "Desktop",
            "subtitle": "~/Desktop",
            "arg": "~/Desktop",
            "autocomplete": "Desktop",
            "icon": {
                "type": "fileicon",
                "path": "~/Desktop"
            }
        }

    References:
        https://www.alfredapp.com/help/workflows/inputs/script-filter/json/
    """

    @staticmethod
    def build(alfred_results):
        return dumps({"items": alfred_results}, default=lambda x: x.dictify())

    @staticmethod
    def write(title: str, subtitle: str, icon_path=None, arg=None):
        dict_object = {"title": title, "subtitle": subtitle}
        if icon_path:
            dict_object["icon"] = {"path": "icons/" + icon_path}  # type: ignore
        if arg:
            dict_object["arg"] = arg
        print(dumps({"items": [dict_object]}))


def main():
    amount = float(argv[1])
    if len(argv) == 2:
        AlfredResponse.write("Waiting...", f"{amount} source destination")
        return

    source = argv[2].upper()
    if len(argv) == 3:
        AlfredResponse.write("Waiting...", f"{amount} {source} destination")
        return
    if not 3 <= len(source) <= 4 and len(argv) == 4:
        AlfredResponse.write("Source symbol is wrong!", f"{source} symbol must be in [3, 4] chars", icon_path="warning.png")
        return

    destination = argv[3].upper()
    if not 3 <= len(destination) <= 4:
        AlfredResponse.write("Waiting...", f"{amount} {source} {destination}")
        return

    try:
        key = os.environ["api_key"]
        converter = YConverter(key)
        value = converter.convert(amount, source, destination)
        AlfredResponse.write(f"{value:,.8}", f"1 {source} = {value / amount:,.8} {destination}", arg=f"{value:,.8}")
    except ValueError as e:
        AlfredResponse.write("Value Error", str(e))


if __name__ == "__main__":
    main()
