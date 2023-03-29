import weaviate

def populate_query(query_vector, client):
    '''
    ToDo, extend with where etc. 
    '''
    query_str = """
    {
        Get {
            Product (
                nearVector: {
                    vector: %s
                }
            ){
            labelName
            }
        }
    }
    """ % query_vector

    results = client.query.raw(query_str)["data"]["Get"]["Product"]

    image_dict = {}
    for idx, result in enumerate(results):
        image_dict[f"image{idx}"] = "images/" + result["labelName"] + ".jpg"
    # do something
    return image_dict

def get_prod_uuid(labelName, client):
    query_str = """
    {
	Get {
        Product (
            where: {
                path: "labelName"
                operator: Equal
                valueText: "%s"
            }
        ){
		_additional {
            id
          }
        }
      }
    }
    """ % labelName

    results = client.query.raw(query_str)["data"]["Get"]["Product"][0]["_additional"]["id"]
    return results

def get_user_vector_and_clicks(user_id, client):
    query_str = """
    {
    Get {
    User (
        where: {
        path: ["id"]
        operator: Equal
        valueString: "%s"
        }
    ){
        likedItem {
        ... on Product {
            labelName
            }
        }
        _additional {
          vector
        }
    }
    }
    }
    """ % user_id


    results = client.query.raw(query_str)["data"]["Get"]["User"][0]
    user_vector = results["_additional"]["vector"]
    likedItems = results["likedItem"]
    if likedItems == None:
        labelNames_only = []
    else:
        labelNames_only = ["images/"+likedItem["labelName"]+".jpg" for likedItem in likedItems]

    return user_vector, labelNames_only