import { useSelector, useDispatch } from "react-redux";
import PostBlock from "../post/PostBlock";
import { useState } from "react";
import UserProfileEditMode from "./UserProfileEditMode";
import UserProfile from "./UserProfile";
import { CardGroup } from "semantic-ui-react";

function UserProfilePage(){

    const [editMode, setEditMode] = useState(false)

    const openEditMode = () => {
        setEditMode(true)
        console.log("clicked")
    }
    const closeEditMode = () => setEditMode(false)

    const loggedInUser = useSelector((store) => store.user)
    const postsSlice = useSelector((store) => store.allPost)

    const userValues = loggedInUser.value
    const posts = postsSlice.value

    const post_info = () => {
        let user_posts = []
        for(const post of posts){
            if(post.user_id == userValues.id){
                user_posts.push(post)
            }
        }
        return user_posts
    }

    return(
        <>
            {
                editMode ?
                <>
                    <UserProfileEditMode user={userValues} close={closeEditMode}/>
                    {
                        post_info()?
                        post_info().map((post) => {
                            return <PostBlock key={post.id} post={post}/>
                        })
                        :
                        null
                    }
                </>
                :
                <>
                    <UserProfile user={userValues} open={openEditMode}/>
                    <CardGroup itemsPerRow={1}>
                        {
                            post_info()?
                            post_info().map((post) => {
                                return <PostBlock key={post.id} post={post}/>
                            })
                            :
                            null
                        }
                    </CardGroup>
                </>
            }
        </>
    )
}

export default UserProfilePage;