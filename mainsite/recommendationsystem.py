from .models import Product
from orders.models import OrderItem
import pandas as pd
from collections import defaultdict
from random import choice

def recommendation(item_id):
    dataset = []
    #order_item = OrderItem.objects.all()
    order_item = OrderItem.objects.select_related('product').select_related('order').all()
    for i in order_item:
        dataset.append([i.product.id,i.order.user_id])

    usersPeritem = defaultdict(set)
    itemPeruser = defaultdict(set)

    df = pd.DataFrame(dataset, columns = ['item_id','user_id'])

    for index,row in df.iterrows():
        x = [row['user_id'] ,row['item_id']]
        for i in x:
            usersPeritem[x[1]].add(x[0])
            itemPeruser[x[0]].add(x[1])

    def jaccard(s1,s2):
        numer = len(s1.intersection(s2))
        denom = len(s1.union(s2))
        return numer / denom

    def mostsimilar(i):
        similar = []
        users = usersPeritem[i]
        candidateitems = set()
        for u in users:
            candidateitems = candidateitems.union(itemPeruser[u])
        for i2 in candidateitems:
            if i2 == i: continue
            sim = jaccard(users,usersPeritem[i2])
            similar.append((sim,i2))
        similar.sort(reverse=True)
        return similar[:3]
    final_data = mostsimilar(item_id)
    if len(final_data) == 3:
        pass
    else:
        items_left = 3 - len(final_data)
        exc_ids = []
        for x in range(0,len(final_data)):
            exc_ids.append(final_data[x][1])
        for i in range(0,items_left):
            random_items = choice(Product.objects.all().exclude(id__in=exc_ids))
            final_data.append((1.0,random_items.id))
            exc_ids.append(random_items.id)
    return final_data
