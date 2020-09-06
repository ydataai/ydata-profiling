# import pandas as pd
#
# from pandas_profiling import ProfileReport
# from pandas_profiling.model.messages import MessageType
#
#
# def test_check_date_type_warning():
#     df = pd.DataFrame(["2018-01-01", "2017-02-01", "2018-04-07"], columns=["date"])
#
#     report = ProfileReport(df, vars={"cat": {"coerce_str_to_date": True}})
#     assert any(
#         message.message_type == MessageType.TYPE_DATE
#         for message in report.get_description()["messages"]
#     ), "Date warning should be present"
