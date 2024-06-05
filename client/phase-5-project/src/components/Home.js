import NotificationList from "./notification/NotificationList";
import UserList from "./user/UserList";
import PostList from "./post/PostList";
import "../CSS/home.css"
import { useDispatch, useSelector } from "react-redux";
import { getFriends } from "../features/friend-slice/friend";
import { getPosts } from "../features/post-slice/allPosts";
import { useEffect } from "react";

function Home(){

    const dispatch = useDispatch()

    useEffect(()=>{
        dispatch(getPosts())
    },[])

    // const testUserList = useSelector((state) => state.userList)
    // const testPostList = useSelector((state) => state.allPost)

    return(
        <>
            <div className="home-grid-container">
                <div className="grid-home-item-left">
                    <UserList className="home-grid-item-left-top"/>
                    <PostList className="home-grid-item-left-bottom"/>
                </div>
                <NotificationList className="grid-home-item-right"/>
            </div>
        </>
    )
}

export default Home;