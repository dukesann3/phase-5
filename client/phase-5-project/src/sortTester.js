

function updatedAtComparator(a,b){
    const aDate = new Date(a.updated_at)
    const bDate = new Date(b.updated_at)
    if(aDate > bDate) return -1
    else if(aDate < bDate) return 1
    return 0
}

const json = [
    {
        "_image_src": "/images/1_folder/1_posts_folder/1_3.jpg",
        "caption": "a",
        "comments": [],
        "created_at": "2024-05-08 13:48:24",
        "id": 3,
        "location": "aasdasd",
        "post_like_notifications": [],
        "post_likes": [],
        "updated_at": "2024-05-08 13:48:24",
        "user_id": 1
      },
      {
        "_image_src": "/images/1_folder/1_posts_folder/1_4.jpg",
        "caption": "a",
        "comments": [],
        "created_at": "2024-05-08 13:48:24",
        "id": 4,
        "location": "aasdasd",
        "post_like_notifications": [],
        "post_likes": [],
        "updated_at": "2024-05-08 13:48:24",
        "user_id": 1
      },
      {
        "_image_src": "/images/1_folder/1_posts_folder/1_5.jpg",
        "caption": "a",
        "comments": [],
        "created_at": "2024-05-08 13:49:23",
        "id": 5,
        "location": "aasdasd",
        "post_like_notifications": [],
        "post_likes": [],
        "updated_at": "2024-05-08 13:49:23",
        "user_id": 1
      },
      {
        "_image_src": "/images/1_folder/1_posts_folder/1_6.jpg",
        "caption": "a",
        "comments": [],
        "created_at": "2024-05-08 13:50:02",
        "id": 6,
        "location": "aasdasd",
        "post_like_notifications": [],
        "post_likes": [],
        "updated_at": "2024-05-08 13:50:02",
        "user_id": 1
      },
      {
        "_image_src": "/images/1_folder/1_posts_folder/1_7.jpg",
        "caption": "a",
        "comments": [],
        "created_at": "2024-05-08 13:51:14",
        "id": 7,
        "location": "aasdasd",
        "post_like_notifications": [],
        "post_likes": [],
        "updated_at": "2024-05-08 13:51:14",
        "user_id": 1
      }
]


console.log(json.sort(updatedAtComparator))