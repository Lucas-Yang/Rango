import app.bin.model as model
import app.bin.dao as sql
import app.common.db as db

""" 为接口生产数据
"""
class TaggingDao():
    """
    """
    filters = model.DetailsQueryIn(sessionid=sessionid,
                                   similarity=similarity,
                                   result=result,
                                   casename=casename
                                   )
    details = await sql.query_details_by_sessionid(db, filters)
    print(details)


class EvluationDao():
    """
    """