def tabulate(s : str, tabs : int = 1, split_char : str = "\n", start : bool = True) -> str:
    """
    Adds tabulations after each occurrence of the split character.

    :param s: The string in which tabs are added.
    :param tabs: The number of tabs to add.
    :param split_char: The split character to use, \\n by default.
    :param start: If True, tabulations will be added at the start of the string.

    :returns: The newly tabulated string.
    """
    s = s.split(split_char)
    if start: s[0] = "\t" * tabs + s[0]
    return (split_char + "\t" * tabs).join(s)