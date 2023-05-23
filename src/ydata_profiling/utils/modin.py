import typing

if typing.TYPE_CHECKING:
    # This is lying to the type checker
    # so that modin is treated exactly the same as pandas
    from pandas import DataFrame, Series
else:
    try:
        from modin.pandas import DataFrame, Series
    except ImportError:

        class DataFrame:
            "A fake modin dataframe. Any isinstance checks should fail."

        class Series:
            "A fake modin. Any isinstance checks should fail."
