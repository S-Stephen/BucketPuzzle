import pytest;

from bucket import BucketList, Bucket

def test_bucket_valid_transfers():
    """Test the productin of valid transfer bucket lists"""
    bucketList = BucketList([Bucket(10,10),Bucket(5,0),Bucket(2,0)])
    actual = list(map( lambda bl : bl.volumes(), bucketList.valid_transfers())) # list of BucketLists
    
    print(f"actual: {actual}")
    expected = [[5,5,0],[8,0,2]]
    assert len(bucketList) == 3
    assert all([a == b for a, b in zip(actual, expected)])


