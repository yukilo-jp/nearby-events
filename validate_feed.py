"""Validate the public feed without network calls or third-party packages."""
import datetime as dt
import json
import math
import sys
from urllib.parse import urlparse

def day(value):
    if not isinstance(value,str) or dt.date.fromisoformat(value).isoformat()!=value:
        raise ValueError('Date must be yyyy-MM-dd')
    return value

def url(value):
    x=urlparse(value)
    assert x.scheme in ('http','https') and x.hostname and not x.username,'Invalid public URL'

def validate(path):
    data=open(path,'rb').read()
    assert len(data)<=2*1024*1024,'Feed exceeds app size limit'
    f=json.loads(data)
    assert f['schema_version']==1,'Unsupported schema'
    day(f['generated_on'])
    assert len(f['events'])<=3000,'Too many events'
    ids=set()
    for e in f['events']:
        for k in ('id','title','source_name','source_url','checked_on','start_date','end_date'):
            assert isinstance(e[k],str) and e[k].strip(),k
        assert e['id'] not in ids,'Duplicate id'
        ids.add(e['id'])
        assert day(e['start_date'])<=day(e['end_date']),'Reversed dates'
        day(e['checked_on']);url(e['source_url'])
        if e.get('official_url'):url(e['official_url'])
        for k in ('start_time','end_time'):
            if e.get(k): assert dt.datetime.strptime(e[k],'%H:%M').strftime('%H:%M')==e[k],'Invalid time'
        lat,lon=e.get('latitude'),e.get('longitude')
        assert (lat is None)==(lon is None),'Coordinates must be a pair'
        if lat is not None:
            assert isinstance(lat,(int,float)) and isinstance(lon,(int,float))
            assert math.isfinite(lat) and math.isfinite(lon) and -90<=lat<=90 and -180<=lon<=180
            assert e.get('coordinate_source_url'),'Coordinate source missing'
            url(e['coordinate_source_url'])
        for d in e.get('excluded_dates',[]):day(d)
    for d in f.get('holiday_dates',[]):day(d)
    return len(ids)
if __name__=='__main__':
    print(f'Valid feed: {validate(sys.argv[1] if len(sys.argv)>1 else "events.json")} events')
