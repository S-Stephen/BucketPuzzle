from bucket import BucketList, Bucket

bucketList = BucketList((Bucket(24, 24), Bucket(13, 0), Bucket(11, 0), Bucket(5, 0)))

print(bucketList.number_of_nodes(), "nodes")
print(bucketList.find_route_to('8,8,8,0'))

