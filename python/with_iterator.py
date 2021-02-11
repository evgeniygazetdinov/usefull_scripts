def all_unique(cat):
    if  '__next__' in dir(cat):
        d = []
        cond = True
        try:
            while cond:
                res = next(cat)
                d.append(res)
        except StopIteration:
            cond = False
            return len(set(d)) == len(d)
    return len(set(cat)) == len(cat)

def test_all_unique():
    assert all_unique(iter([])), "Should work with iterators."
    assert all_unique(iter([1])), (
        "Should handle non-restartable iterators too."
    )
    assert all_unique([])
    assert all_unique("cat")

if __name__ == '__main__':
  test_all_unique()
