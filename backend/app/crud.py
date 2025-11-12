from app.mongo_db import mongo_db as db
from bson.son import SON
import datetime

async def avg_speed_by_road():
    pipeline = [
        {"$match": {"speed_kmph": {"$exists": True}, "road_type": {"$exists": True}}},
        {"$group": {"_id": "$road_type", "avg_speed": {"$avg": "$speed_kmph"}, "count": {"$sum": 1}}},
        {"$project": {"road_type": "$_id", "avg_speed_kmph": {"$round": ["$avg_speed", 2]}, "count": 1, "_id": 0}},
        {"$sort": SON([("avg_speed_kmph", -1)])}
    ]
    return [doc async for doc in db.traffic_events.aggregate(pipeline)]

async def total_vehicle_count_by_type():
    pipeline = [
        {"$group": {"_id": "$vehicle_type", "count": {"$sum": 1}}},
        {"$project": {"vehicle_type": "$_id", "count": 1, "_id": 0}},
        {"$sort": {"count": -1}}
    ]
    return [doc async for doc in db.traffic_events.aggregate(pipeline)]

async def occupancy_trends(hours=24, interval_minutes=60):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(hours=hours)
    pipeline = [
        {"$match": {"timestamp": {"$gte": start, "$lte": end}, "occupancy": {"$exists": True}}},
        {"$addFields": {
            "bucket": {
                "$toLong": {
                    "$subtract": [
                        {"$toLong": {"$toDate": "$timestamp"}},
                        {"$mod": [
                            {"$toLong": {"$toDate": "$timestamp"}}, 1000 * 60 * interval_minutes
                        ]}
                    ]
                }
            }
        }},
        {"$group": {"_id": "$bucket", "avg_occupancy": {"$avg": "$occupancy"}}},
        {"$project": {"timestamp": {"$toDate": "$_id"}, "avg_occupancy": {"$round": ["$avg_occupancy", 2]}, "_id": 0}},
        {"$sort": {"timestamp": 1}}
    ]
    return [doc async for doc in db.traffic_events.aggregate(pipeline)]
