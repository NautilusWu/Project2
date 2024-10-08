"""
SCI 33 Project 2: Customized namedtuple class generator
"""

from keyword import kwlist


def chk_field_names(field_names) -> bool:
    """
    Check if the field names are valid identifiers.
    """
    rtn = False
    if isinstance(field_names, list):
        if all(
                isinstance(name, str)
                and name.isidentifier()
                and (name not in kwlist)
                for name in field_names
        ):
            rtn = True
    if isinstance(field_names, str):
        if "," in field_names:
            field_names_lst = field_names.split(",")
            field_names_lst = [name.strip() for name in field_names_lst]
        else:
            field_names_lst = field_names.split()
        if all(
                isinstance(field_name, str)
                and field_name.isidentifier()
                and field_name not in kwlist
                for field_name in field_names_lst
        ):
            rtn = True
    return rtn


def mynamedtuple(type_name, field_names, mutable=False, defaults=None):
    """
    Generates customized namedtuple classes dynamically.

    Args:
        type_name (str): The name of the class.
        field_names (str or list): A string or a list of strings representing
                                   the field names.
        mutable (bool, optional): Whether the class is mutable or not.
                                  Defaults to False.
        defaults (dict, optional): A dictionary of default values for the
                                   fields. Defaults to {}.

    Returns:
        A customized namedtuple class.
    """
    # print(type_name, field_names, mutable, defaults)

    type_name_check = (
            isinstance(type_name, str)
            and type_name.isidentifier()
            and type_name not in kwlist
    )
    field_names_check = chk_field_names(field_names)
    if defaults is None:
        defaults = {}
        defaults_check = True
    else:
        defaults_check = isinstance(defaults, dict) and all(
            isinstance(key, str) and key.isidentifier()  # Should we allow it?
            for key in defaults.keys()
        )
    if mutable is None:
        mutable = False
    mutable_check = isinstance(mutable, bool)
    # print(type_name_check, field_names_check, defaults_check, mutable_check)
    if not all(
            [type_name_check, field_names_check, defaults_check, mutable_check]
    ):
        raise SyntaxError(
            "Type names, field names and defaults must be valid identifiers"
        )

    if not isinstance(field_names, list):
        if "," in field_names:
            field_names = field_names.split(",")
            field_names = [name.strip() for name in field_names]
        else:
            field_names = field_names.split()
    field_names = sorted(set(field_names), key=field_names.index)
    if not all(key in field_names for key in defaults.keys()):
        raise SyntaxError("Default values must correspond to field names")

    # cls_name = "MyNamedTuple_" + type_name
    cls_name = type_name
    my_code = f"class {cls_name}:\n"
    my_code += f"    _fields = {field_names}\n"
    my_code += f"    _defaults = {defaults}\n"
    my_code += f"    _mutable = {mutable}\n"
    init_lst = []
    for name in field_names:
        if name in defaults.keys():
            if isinstance(defaults[name], str):
                init_lst.append(f"{name}='{defaults[name]}'")
            else:
                init_lst.append(f"{name}={defaults[name]}")
        else:
            init_lst.append(f"{name}")
    init_str = ", ".join(init_lst)
    my_code += f"    def __init__(self, {init_str}):\n"
    for name in field_names:
        my_code += f"        self.{name} = {name}\n"

    my_code += f"    def __repr__(self):\n"
    my_code += f"        lst = [(\n"
    my_code += f"            f'{{k}} = \\'{{v}}\\''\n"
    my_code += f"            if isinstance(v, str)\n"
    my_code += f"            else f'{{k}}={{v}}')\n"
    my_code += f"            for k, v in self.__dict__.items()]\n"
    my_code += f"        str1 =','.join(lst)\n"
    my_code += f"        return f'{cls_name}({{str1}})'\n"

    for attr in field_names:
        my_code += f"    def get_{attr}(self):\n"
        my_code += f"        return self.{attr}\n"

    my_code += f"    def __getitem__(self, index):\n"
    my_code += f"        if index < 0 or index >= len(self._fields):\n"
    my_code += f"            raise IndexError('index out of range')\n"
    my_code += f"        return getattr(self, self._fields[index])\n"

    my_code += f"    def __eq__(self, other):\n"
    my_code += f"        if not isinstance(other, self.__class__):\n"
    my_code += f"            return False\n"
    my_code += f"        if self.__class__!= other.__class__:\n"
    my_code += f"            return False\n"
    my_code += f"        if len(self._fields) != len(other._fields):\n"
    my_code += f"            return False\n"
    my_code += f"        for name in self._fields:\n"
    my_code += f"            if getattr(self, name) != getattr(other, name):\n"
    my_code += f"                return False\n"
    my_code += f"        return True\n"

    my_code += f"    def _asdict(self):\n"
    my_code += (
        f"        return dict({{k: getattr(self, k) for k in self._fields}})\n"
    )

    my_code += f"    def _make(iterable=None):\n"
    my_code += f"        if iterable is None:\n"
    my_code += f"            raise TypeError(f'Argument iterable cannot be empty')\n"
    my_code += f"        if len(iterable) != len({cls_name}._fields):\n"
    my_code += f"            raise TypeError(f'Expected {{len({cls_name}._fields)}} arguments')\n"
    my_code += f"        values = tuple(iterable)\n"
    my_code += f"        return {cls_name}(*values)\n"

    my_code += f"    def _replace(self, **kargs):\n"
    # my_code += f"        print('kargs:', kargs)\n"
    # my_code += f"        print('fields:',self._fields)\n"
    # my_code += f"        print('defaults:', self._defaults)\n"
    # my_code += f"        print('mutable:',self._mutable)\n"
    my_code += (
        f"        if not all(k in self._fields for k in kargs.keys()):\n"
    )
    my_code += f"            raise TypeError('Invalid field names')\n"
    my_code += f"        if self._mutable:\n"
    my_code += f"            for name in kargs.keys():\n"
    my_code += f"                setattr(self, name, kargs[name])\n"
    my_code += f"            return None\n"
    my_code += f"        else:\n"
    my_code += f"           new_args = []\n"
    my_code += f"           for name in self._fields:\n"
    my_code += f"               if name in kargs:\n"
    my_code += f"                   new_args.append(kargs[name])\n"
    my_code += f"               else:\n"
    my_code += f"                   new_args.append(getattr(self, name))\n"
    my_code += f"           return self.__class__(*new_args)\n"

    my_code += f"    def __setattr__(self, name, value):\n"
    my_code += f"        if (\n"
    my_code += f"            not self._mutable\n"
    my_code += f"            and (hasattr(self, name)\n"
    my_code += f"               or name not in self._fields)\n"
    my_code += f"        ):\n"
    my_code += f"            raise AttributeError(f'{cls_name} object is immutable')\n"
    my_code += f"        super().__setattr__(name, value)\n"

    # print(my_code)
    try:
        exec(my_code, locals())
    except Exception as e:
        raise Exception("Unexpected exec() Error") from e
    # print(f'\n--------\n{locals()}\n----------\n')
    return locals()[cls_name]
