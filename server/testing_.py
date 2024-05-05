

post_list = [{"updated_at": "2024-04-25 14:16:22.364264",
              "poop": "69"},{"updated_at": "2024-05-02 19:41:36.468253",
                             "poop": "900"}]

sorted_post_list = sorted(post_list, key=lambda post: post["updated_at"])

print(sorted_post_list)