import typing

if typing.TYPE_CHECKING:
    # This is lying to the type checker
    # so that modin is treated exactly the same as pandas
    from pandas import DataFrame, Series, cut, qcut
else:
    try:
        from modin.pandas import DataFrame, Series, cut, qcut
    except ImportError:

        class DataFrame:
            "A fake modin dataframe. Any isinstance checks should fail."

        class Series:
            "A fake modin. Any isinstance checks should fail."

        cut = qcut = lambda *args, **kwargs: None
