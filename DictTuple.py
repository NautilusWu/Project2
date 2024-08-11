"""
SCI 33 Project 2: Customized namedtuple class DictTuple
"""

from mynamedtuple import mynamedtuple


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
        distinct_keys = {key for item in self.dt for key in item}
        if key not in distinct_keys:
            self.dt.append({key: value})
        else:
            max_inx = max(
                inx for inx, item in enumerate(self.dt) if key in item
            )
            self.dt[max_inx][key] = value

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

    # def __iter__(self):
    #     keys_list = [key for item in self.dt for key in item]
    #     distinct_keys = sorted(set(keys_list), key=keys_list.index)
    #     my_iter_01 = []
    #     for k in distinct_keys:
    #         my_iter_01.append([item for item in self.dt if k in item][-1])
    #     my_iter_02 = []
    #     for item_dict in my_iter_01:
    #         temp_dict = {}
    #         for k in sorted(item_dict):
    #             temp_dict[k] = item_dict[k]
    #         my_iter_02.append(temp_dict)
    #     # print(distinct_keys)
    #     # print(my_iter_02)
    #     return iter(my_iter_02)

    def __iter__(self):
        keys_list = [key for item in self.dt for key in item]
        # distinct_keys = sorted(set(keys_list), key=keys_list.index)
        distinct_keys = sorted(set(keys_list))
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


# Testing the DictTuple class
def main():
    coordinate = mynamedtuple("coordinate", "x y")
    # d = DictTuple({"c1": coordinate(1, 2)}, {"c1": coordinate(3, 4)})
    d = DictTuple(1)
    # d = DictTuple({"c1": "AAA"}, {"c1": "BBB"}, {"c2": "CCC"}, {"c1": "DDD"})
    # d = DictTuple({'c1': 'AAA'})
    # d = DictTuple(1)
    print(len(d))
    print(d.dt)
    print(bool(d))
    print(d)
    print("c1" in d)
    print("c2" in d)
    print(d["c1"])
    # print(d["c3"])
    d["c1"] = "FFFF"
    print(d["c1"])
    print(d.dt)
    d["c3"] = "GGGG"
    print(d.dt)
    del d["c1"]
    print(d.dt)
    # del d["c1"]
    e = DictTuple(
        {"f1": coordinate(1, 2), "c5": coordinate(7, 8)},
        {"c1": coordinate(3, 4), "c2": coordinate(9, 10)},
        {"c1": coordinate("AAA", "BBB")},
    )
    print(f"e.dt: {e.dt}")
    print(f"e('c1'): {e('c1')}")
    print(f"e('c2'): {e('c2')}")
    print(f"e['c1']: {e['c1']}")
    print(f"e['c2']: {e['c2']}")
    print("===== iter =====")
    for i, item in enumerate(e):
        print(i, item)
    e2 = DictTuple(
        {"c1": coordinate(3, 4), "c2": coordinate(9, 10)},
        {"f1": coordinate(1, 2), "c5": coordinate(7, 8)},
        {"c1": coordinate("AAA", "BBB")},
    )
    print("==============")
    print(f"e == e2: {e == e2}")
    dict_01 = {
        "c2": coordinate(9, 10),
        "f1": coordinate(1, 2),
        "c5": coordinate(7, 8),
        "c1": coordinate("AAA", "BBB"),
        # "c3": "GGGG",
    }
    print("==============")
    print(f"e == dict_01: {e == dict_01}")
    print(f"e2 == dict_01: {e2 == dict_01}")
    print(f"e2 == 'ABCD': {e2 == 'ABCD'}")

    print("========= + =========")
    d1 = DictTuple({"c1": coordinate(1, 2)}, {"c1": coordinate(3, 4)})
    d2 = DictTuple({"c2": coordinate(1, 2)}, {"c3": coordinate(3, 4)})
    d3 = d1 + d2
    print(d3.dt)
    d4 = d2 + d1
    print(d4.dt)
    adt = DictTuple({"c1": coordinate(1, 2)}, {"c1": coordinate(3, 4)})
    adict = {"c3": coordinate(3, 4)}
    print(adt + adict)
    print(adict + adt)
    # print(adt + 'ABCD')
    print("========= += =========")
    d1 = DictTuple({"c1": coordinate(1, 2)}, {"c1": coordinate(3, 4)})
    d2 = DictTuple({"c2": coordinate(1, 2)}, {"c3": coordinate(3, 4)})
    adict = {"c3": coordinate(3, 4)}
    d1 += d2
    print(d1)
    d1 += adict
    print(d1)
    # d1 += 'ABCD'
    print(d1.dt)
    # setattr(d1, "dt", [{'ss' : coordinate(50, 60)}])
    setattr(d1, "dt", [{"s": "s"}])
    print(d1)


if __name__ == "__main__":
    main()
