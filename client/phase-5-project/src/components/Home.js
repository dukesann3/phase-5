import NotificationList from "./notification/NotificationList";
import UserList from "./user/UserList";
import PostList from "./post/PostList";

function Home(){
    return(
        <>
            <span>Home?</span>
            <NotificationList />
            <UserList />
            <PostList />
        </>
    )
}

export default Home;