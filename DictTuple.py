"""
SCI 33 Project 2: Customized namedtuple class DictTuple
"""


class DictTuple:

    def __init__(self, *args):
        self.dt = list(args)
        if any(not isinstance(x, dict) for x in self.dt):
            raise AssertionError("All input must be dictionaries")

        if (
            any(len(x) == 0 for x in self.dt)
            or len(self.dt) == 0
        ):
            raise AssertionError(
                "All input must be dictionaries with at least one element"
            )

    def __len__(self):
        distinct_keys = {key for item in self.dt for key in item}
        return len(distinct_keys)

    def __bool__(self):
        return len(self.dt) > 1

    def __repr__(self):
        str_01 = (
            f"{self.__class__.__name__}({', '.join(str(x) for x in self.dt)})"
        )
        return str_01

    def __contains__(self, item):
        distinct_keys = {key for item in self.dt for key in item}
        return item in distinct_keys

    def __getitem__(self, key):
        distinct_keys = {key for item in self.dt for key in item}
        if key not in distinct_keys:
            raise KeyError(f"Key '{key}' does not exist")
        latest_dict = [item for item in self.dt if key in item][-1]
        return latest_dict[key]

    def __setitem__(self, key, value):
        # print(self.dt)
        # print(key, value)
        distinct_keys = {key for item in self.dt for key in item}
        if key not in distinct_keys:
            self.dt.append({key: value})
        else:
            max_inx = max(
                inx for inx, item in enumerate(self.dt) if key in item
            )
            self.dt[max_inx][key] = value
        # print('!!!', self.dt)

    def __delitem__(self, key):
        # print(self.dt)
        distinct_keys = {key for item in self.dt for key in item}
        # print(key)
        if key not in distinct_keys:
            raise KeyError(f"Key '{key}' does not exist")
        new_dt = []
        for item in self.dt:
            temp_dict = {}
            for k, v in item.items():
                if k != key:
                    temp_dict[k] = v
            if temp_dict:
                new_dt.append(temp_dict)
        self.dt = new_dt
        # print(self.dt)

    def __call__(self, key):
        distinct_keys = {key for item in self.dt for key in item}
        if key not in distinct_keys:
            return []
        lst_01 = [item.get(key) for item in self.dt if key in item]
        lst_02 = [
            len(item.get(key)._fields) for item in self.dt if key in item
        ]
        # print(lst_01, lst_02)
        return [
            [value[i] for i in range(lst_02[inx])]
            for inx, value in enumerate(lst_01)
        ]

    def __iter__(self):
        # print(self.dt)
        temp_dt = [self.dt[i] for i in range(len(self.dt) - 1, -1, -1)]
        my_iter_02 = []
        for item_dict in temp_dt:
            temp_dict = {}
            for k in sorted(item_dict):
                temp_dict[k] = item_dict[k]
            my_iter_02.append(temp_dict)
        # print("L107", temp_dt)
        keys_list = [key for item in my_iter_02 for key in item]
        # print('L109', keys_list)
        distinct_keys = sorted(set(keys_list), key=keys_list.index)
        # print('L111', distinct_keys)
        return iter(distinct_keys)

    def __eq__(self, other):
        if not isinstance(other, (DictTuple, dict)):
            return False
        if len(self) != len(other):
            return False
        distinct_keys_01 = sorted(
            list({key for item in self.dt for key in item})
        )
        if isinstance(other, DictTuple):
            distinct_keys_02 = sorted(
                list({key for item in other.dt for key in item})
            )
            # print(distinct_keys_01, distinct_keys_02)
            if distinct_keys_01 != distinct_keys_02:
                return False
            # for k in distinct_keys_01:
            #     print(self[k], other[k])
            return all(self[k] == other[k] for k in distinct_keys_01)
        if not isinstance(other, dict):
            return False
        if any(k not in self for k in other.keys()):
            return False
        return all(self[k] == other[k] for k in distinct_keys_01)

    def __add__(self, other):
        if not isinstance(other, (DictTuple, dict)):
            raise TypeError(f"Can not add type '{other.__class__.__name__}'")
        if isinstance(other, DictTuple):
            return DictTuple(*self.dt, *other.dt)
        return DictTuple(*self.dt, other)

    def __radd__(self, other):
        if not isinstance(other, (DictTuple, dict)):
            raise TypeError(f"Can not add type '{other.__class__.__name__}'")
        return DictTuple(other) + self

    def __iadd__(self, other):
        if not isinstance(other, (DictTuple, dict)):
            raise TypeError(f"Can not add type '{other.__class__.__name__}'")
        if isinstance(other, DictTuple):
            self.dt = [*self.dt, *other.dt]
        else:
            self.dt = [*self.dt, other]
        return self

    def __setattr__(self, name, value):
        if (
            not isinstance(value, list)
            or any(not isinstance(x, dict) or len(x) == 0 for x in value)
            or len(value) == 0
        ):
            raise AssertionError(
                "value must be dictionaries with at least one element"
            )
        if name != "dt":
            raise AssertionError("Can not set attribute except 'dt'")
        # if hasattr(self,'dt'):
        #     return DictTuple({name: value})
        return super().__setattr__(name, value)
